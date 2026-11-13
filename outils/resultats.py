#!/usr/bin/env python3
"""
Calcule et insère automatiquement les « résultats attendus » dans les fichiers Markdown du cours.

Pourquoi ? Les résultats affichés dans le cours doivent correspondre exactement aux données
de la base. Comme la base évolue, on régénère les résultats au lieu de les recopier à la main.

Fonctionnement :
  - la base db/essais_cliniques.sql est chargée dans une base SQLite en mémoire
    (avec quelques traductions MySQL → SQLite et des fonctions MySQL émulées) ;
  - dans chaque fichier .md, chaque bloc ```sql suivi de la ligne  <!-- resultat -->
    est exécuté, et son résultat est inséré (ou remplacé) juste en dessous ;
  - un bloc ```sql précédé de la ligne  <!-- exec -->  est exécuté sans afficher de résultat
    (utile pour CREATE VIEW, INSERT… dont on a besoin plus loin) ;
  - <!-- resultat:30 --> affiche jusqu'à 30 lignes (12 par défaut) ;
  - chaque fichier repart d'une base neuve ; les blocs d'un même fichier s'enchaînent.

Usage :
    python3 outils/resultats.py              # traite cours/, exercices/
    python3 outils/resultats.py fichier.md   # un seul fichier

Limites : SQLite n'est pas MySQL. Les requêtes propres à MySQL non émulées doivent être
laissées sans marqueur. L'affichage des décimales peut différer légèrement de DBeaver.
"""

import datetime as dt
import pathlib
import re
import sqlite3
import sys
import unicodedata

RACINE = pathlib.Path(__file__).resolve().parent.parent
BASE = RACINE / "db" / "essais_cliniques.sql"

# ---------------------------------------------------------------------------
#  Fonctions MySQL émulées
# ---------------------------------------------------------------------------


def _date(v):
    if v is None:
        return None
    return dt.date.fromisoformat(str(v)[:10])


def f_year(v):
    v = _date(v)
    return v.year if v else None


def f_month(v):
    v = _date(v)
    return v.month if v else None


def f_day(v):
    v = _date(v)
    return v.day if v else None


def f_datediff(a, b):
    a, b = _date(a), _date(b)
    return (a - b).days if a and b else None


def f_concat(*args):
    if any(a is None for a in args):
        return None
    return "".join(_txt(a) for a in args)


def f_concat_ws(sep, *args):
    return sep.join(_txt(a) for a in args if a is not None)


def _txt(a):
    if isinstance(a, float) and a.is_integer():
        return str(int(a))
    return str(a)


def _ajoute(v, qte, unite):
    v = _date(v)
    if v is None:
        return None
    unite = unite.upper()
    if unite == "DAY":
        return (v + dt.timedelta(days=qte)).isoformat()
    if unite == "WEEK":
        return (v + dt.timedelta(days=7 * qte)).isoformat()
    mois = qte * (12 if unite == "YEAR" else 1)
    m = v.month - 1 + mois
    an, m = v.year + m // 12, m % 12 + 1
    import calendar
    jour = min(v.day, calendar.monthrange(an, m)[1])
    return dt.date(an, m, jour).isoformat()


def f_date_add(v, intervalle):
    qte, unite = intervalle.split()
    return _ajoute(v, int(qte), unite)


def f_date_sub(v, intervalle):
    qte, unite = intervalle.split()
    return _ajoute(v, -int(qte), unite)


def f_timestampdiff(unite, a, b):
    a, b = _date(a), _date(b)
    if not a or not b:
        return None
    unite = unite.upper()
    if unite == "DAY":
        return (b - a).days
    mois = (b.year - a.year) * 12 + (b.month - a.month)
    if b.day < a.day:
        mois -= 1 if mois > 0 else 0
    if unite == "MONTH":
        return mois
    if unite == "YEAR":
        return int(mois / 12)
    raise ValueError(unite)


def f_extract(unite, v):
    return {"YEAR": f_year, "MONTH": f_month, "DAY": f_day}[unite.upper()](v)


def f_date_format(v, fmt):
    v = _date(v)
    if v is None:
        return None
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
            "septembre", "octobre", "novembre", "décembre"]
    return (fmt.replace("%Y", f"{v.year:04d}").replace("%m", f"{v.month:02d}")
            .replace("%d", f"{v.day:02d}").replace("%M", mois[v.month - 1]))


def f_left(s, n):
    return None if s is None else str(s)[:n]


def f_right(s, n):
    return None if s is None else str(s)[-n:] if n else ""


def f_lpad(s, n, c):
    return None if s is None else str(s).rjust(n, c)[:n]


def f_if(c, a, b):
    return a if c else b


FONCTIONS = [
    ("YEAR", 1, f_year), ("MONTH", 1, f_month), ("DAY", 1, f_day),
    ("DATEDIFF", 2, f_datediff), ("CONCAT", -1, f_concat), ("CONCAT_WS", -1, f_concat_ws),
    ("DATE_ADD", 2, f_date_add), ("DATE_SUB", 2, f_date_sub), ("TIMESTAMPDIFF", 3, f_timestampdiff),
    ("EXTRACT_", 2, f_extract), ("DATE_FORMAT", 2, f_date_format),
    ("UPPER", 1, lambda s: None if s is None else str(s).upper()),
    ("LOWER", 1, lambda s: None if s is None else str(s).lower()),
    ("CHAR_LENGTH", 1, lambda s: None if s is None else len(str(s))),
    ("LEFT", 2, f_left), ("RIGHT", 2, f_right), ("LPAD", 3, f_lpad), ("IF", 3, f_if),
]

# ---------------------------------------------------------------------------
#  Traduction MySQL → SQLite
# ---------------------------------------------------------------------------


def cle_mysql(t):
    """Clé de comparaison imitant la collation MySQL utf8mb4_0900_ai_ci (sans casse ni accents)."""
    t = t.replace("œ", "oe").replace("Œ", "OE").replace("æ", "ae").replace("Æ", "AE")
    t = "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))
    return t.casefold()


def collation_mysql(a, b):
    a, b = cle_mysql(a), cle_mysql(b)
    return (a > b) - (a < b)


def round_entier(sql):
    """ROUND(x) sans 2e argument → entier (comme MySQL, qui n'affiche pas de décimale)."""
    out, i = [], 0
    while True:
        m = re.compile(r"\bROUND\(", re.I).search(sql, i)
        if not m:
            out.append(sql[i:])
            return "".join(out)
        depth, j, virgule = 1, m.end(), False
        while depth:
            c = sql[j]
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            elif c == "," and depth == 1:
                virgule = True
            j += 1
        interieur = round_entier(sql[m.end():j - 1])
        out.append(sql[i:m.start()])
        if virgule:
            out.append("ROUND(" + interieur + ")")
        else:
            out.append("CAST(ROUND(" + interieur + ") AS INTEGER)")
        i = j


def auto_increment(sql):
    """INT … AUTO_INCREMENT → INTEGER PRIMARY KEY (équivalent SQLite)."""
    if not re.search(r"AUTO_INCREMENT", sql, re.I):
        return sql
    sql = re.sub(r"(\w+)\s+INT\s+NOT\s+NULL\s+AUTO_INCREMENT", r"\1 INTEGER PRIMARY KEY", sql, flags=re.I)
    sql = re.sub(r",\s*CONSTRAINT\s+\w+\s+PRIMARY\s+KEY\s*\(\s*\w+\s*\)", "", sql, flags=re.I)
    return sql


def traduit(sql):
    sql = auto_increment(sql)
    sql = round_entier(sql)
    sql = re.sub(r"TIMESTAMPDIFF\(\s*(\w+)\s*,", r"TIMESTAMPDIFF('\1',", sql, flags=re.I)
    sql = re.sub(r"INTERVAL\s+(-?\d+)\s+(DAY|WEEK|MONTH|YEAR)", r"'\1 \2'", sql, flags=re.I)
    sql = re.sub(r"EXTRACT\(\s*(\w+)\s+FROM\s+", r"EXTRACT_('\1', ", sql, flags=re.I)
    sql = re.sub(r"GROUP_CONCAT\((.+?)(\s+ORDER BY\s+[^)]*?)?\s+SEPARATOR\s+('[^']*')\)",
                 r"GROUP_CONCAT(\1, \3\2)", sql, flags=re.I)
    sql = re.sub(r"CREATE\s+OR\s+REPLACE\s+VIEW\s+(\w+)", r"DROP VIEW IF EXISTS \1; CREATE VIEW \1", sql, flags=re.I)
    sql = re.sub(r"START\s+TRANSACTION", "BEGIN", sql, flags=re.I)
    sql = re.sub(r"TRUNCATE\s+TABLE", "DELETE FROM", sql, flags=re.I)
    sql = re.sub(r"\bCURRENT_DATE\b|CURDATE\(\)", "'2026-06-30'", sql, flags=re.I)
    # division décimale comme en MySQL (et non entière comme en SQLite)
    sql = sql.replace(" / ", " * 1.0 / ")
    return sql


def decoupe(sql):
    """Découpe un script en instructions (sur les ';' hors chaînes)."""
    out, cur, dans_chaine = [], [], False
    # retire les commentaires « -- … » (hors chaînes) pour ne pas être gêné par leurs apostrophes
    propre = []
    for ligne in sql.split("\n"):
        q, res = False, []
        i = 0
        while i < len(ligne):
            c = ligne[i]
            if c == "'":
                q = not q
            if not q and ligne[i:i + 2] == "--":
                break
            res.append(c)
            i += 1
        propre.append("".join(res))
    sql = "\n".join(propre)
    for ch in sql:
        if ch == "'":
            dans_chaine = not dans_chaine
        if ch == ";" and not dans_chaine:
            s = "".join(cur).strip()
            if s:
                out.append(s)
            cur = []
        else:
            cur.append(ch)
    s = "".join(cur).strip()
    if s and not all(l.strip().startswith("--") or not l.strip() for l in s.splitlines()):
        out.append(s)
    return out


def nouvelle_base():
    con = sqlite3.connect(":memory:", isolation_level=None)
    con.create_collation("MYSQLCI", collation_mysql)
    for nom, n, f in FONCTIONS:
        con.create_function(nom, n, f, deterministic=True)
    con.execute("PRAGMA foreign_keys = ON")
    script = BASE.read_text(encoding="utf-8")
    for stmt in decoupe(script):
        tete = re.sub(r"^(\s*--[^\n]*\n)*", "", stmt).strip().upper()
        if tete.startswith(("DROP DATABASE", "CREATE DATABASE", "USE ")):
            continue
        stmt = auto_increment(stmt)
        stmt = re.sub(r"(\bVARCHAR\(\d+\)|\bCHAR\(\d+\))", r"\1 COLLATE MYSQLCI", stmt)
        con.execute(stmt)
    return con


# ---------------------------------------------------------------------------
#  Affichage
# ---------------------------------------------------------------------------


def fmt(v):
    if v is None:
        return "NULL"
    if isinstance(v, float):
        return repr(round(v, 4))
    return str(v)


def tableau(colonnes, lignes, max_lignes):
    total = len(lignes)
    lignes = lignes[:max_lignes]
    cellules = [[fmt(v) for v in l] for l in lignes]
    larg = [max([len(c)] + [len(l[i]) for l in cellules]) for i, c in enumerate(colonnes)]
    sep = "+" + "+".join("-" * (w + 2) for w in larg) + "+"
    out = [sep, "| " + " | ".join(c.ljust(w) for c, w in zip(colonnes, larg)) + " |", sep]
    for l in cellules:
        out.append("| " + " | ".join(v.ljust(w) for v, w in zip(l, larg)) + " |")
    out.append(sep)
    if total > max_lignes:
        out.append(f"… {total} lignes au total ({max_lignes} affichées)")
    else:
        out.append(f"{total} ligne{'s' if total > 1 else ''}")
    return "\n".join(out)


def execute(con, sql):
    """Exécute un bloc ; renvoie le texte du résultat de la dernière instruction."""
    texte = None
    for stmt in decoupe(sql):
        for s in decoupe(traduit(stmt)):
            cur = con.execute(s)
            if cur.description:
                cols = [c[0] for c in cur.description]
                texte = (cols, cur.fetchall())
            else:
                texte = ("ok", con.total_changes)
    return texte


# ---------------------------------------------------------------------------
#  Traitement des fichiers Markdown
# ---------------------------------------------------------------------------

BLOC = re.compile(
    r"(?P<avant><!-- exec -->\n)?```sql\n(?P<sql>.*?)```\n"
    r"(?P<marque><!-- resultat(?::(?P<n>\d+))? -->\n(?:```text\n.*?```\n<!-- /resultat -->\n)?)?",
    re.S,
)


def traite(chemin):
    texte = chemin.read_text(encoding="utf-8")
    if "<!-- resultat" not in texte and "<!-- exec -->" not in texte:
        return 0
    con = nouvelle_base()
    erreurs = 0
    total_avant = con.total_changes

    def remplace(m):
        nonlocal erreurs
        if not m.group("avant") and not m.group("marque"):
            return m.group(0)
        sql = m.group("sql")
        try:
            avant = con.total_changes
            res = execute(con, sql)
            if res and res[0] == "ok":
                n = con.total_changes - avant
                rendu = f"Requête OK, {n} ligne{'s' if n > 1 else ''} affectée{'s' if n > 1 else ''}"
            elif res:
                rendu = tableau(res[0], res[1], int(m.group("n") or 12))
            else:
                rendu = "(aucun résultat)"
        except Exception as e:  # noqa
            erreurs += 1
            print(f"  ✗ {chemin.name}: {e}\n    {sql.strip()[:200]}")
            rendu = f"ERREUR DE GÉNÉRATION : {e}"
        bloc = (m.group("avant") or "") + "```sql\n" + sql + "```\n"
        if m.group("marque"):
            n = m.group("n")
            bloc += f"<!-- resultat{':' + n if n else ''} -->\n```text\n{rendu}\n```\n<!-- /resultat -->\n"
        return bloc

    nouveau = BLOC.sub(remplace, texte)
    if nouveau != texte:
        chemin.write_text(nouveau, encoding="utf-8")
    _ = total_avant
    return erreurs


def main():
    if len(sys.argv) > 1:
        fichiers = [pathlib.Path(a) for a in sys.argv[1:]]
    else:
        fichiers = sorted((RACINE / "cours").glob("*.md")) + sorted((RACINE / "exercices").rglob("*.md"))
    erreurs = 0
    for f in fichiers:
        e = traite(f)
        erreurs += e
        print(f"{'✓' if not e else '✗'} {f.relative_to(RACINE) if f.is_absolute() else f}")
    sys.exit(1 if erreurs else 0)


if __name__ == "__main__":
    main()
