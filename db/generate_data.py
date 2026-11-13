#!/usr/bin/env python3
"""
Générateur déterministe des données de la base `essais_cliniques`.

Usage :
    python3 db/generate_data.py

Produit :
    db/02_data.sql          → uniquement les INSERT
    db/essais_cliniques.sql → schéma + données (LE fichier à charger dans DBeaver)

La graine aléatoire est fixe : chaque exécution produit exactement les mêmes données.
Toute modification de ce script doit être notée dans db/CHANGELOG.md.
"""

import datetime as dt
import pathlib
import random
import unicodedata

R = random.Random(2026)
REF = dt.date(2026, 6, 30)  # « aujourd'hui » dans la base
HERE = pathlib.Path(__file__).resolve().parent


def d(s):
    return dt.date.fromisoformat(s) if s else None


def plus(date, days):
    return date + dt.timedelta(days=days)


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return s.lower().replace(" ", "-").replace("'", "")


# ---------------------------------------------------------------------------
#  Données de référence (écrites à la main)
# ---------------------------------------------------------------------------

ETUDES = [
    # id, code, titre, phase, aire, promoteur, debut, fin_prevue, objectif, statut
    (1, "CARDIO-01", "Effet de la molécule KX-12 sur l'hypertension artérielle", "III",
     "Cardiologie", "Laboratoires Alvéa", "2024-03-01", "2026-12-31", 120, "suivi"),
    (2, "DIAB-02", "Contrôle glycémique par GL-7 chez le diabétique de type 2", "II",
     "Diabétologie", "Biomédix", "2025-01-15", "2027-06-30", 80, "recrutement"),
    (3, "ONCO-03", "Tolérance de l'immunothérapie OX-3 dans le cancer du poumon", "II",
     "Oncologie", "Laboratoires Alvéa", "2025-06-01", "2027-12-31", 60, "recrutement"),
    (4, "NEURO-04", "Première administration de NR-1 chez le volontaire sain", "I",
     "Neurologie", "NeuroPharm", "2023-01-10", "2023-12-31", 30, "terminée"),
    (5, "DERM-05", "Efficacité de la crème DM-5 dans le psoriasis", "III",
     "Dermatologie", "Biomédix", None, None, 100, "en préparation"),
]

CENTRES = [
    (1, "Clinique du Val de Loire", "Tours", "France"),
    (2, "CHU Atlantique", "Nantes", "France"),
    (3, "Hôpital Saint-Roch", "Montpellier", "France"),
    (4, "Centre Hospitalier du Rhône", "Lyon", "France"),
    (5, "Clinique des Flandres", "Lille", "France"),
    (6, "Clinique du Léman", "Genève", "Suisse"),
    (7, "Hospital del Sol", "Valencia", "Espagne"),
    (8, "Centre Médical des Ardennes", "Liège", "Belgique"),
]

# id, nom, prenom, specialite, centre_id, superviseur_id
INVESTIGATEURS = [
    (1, "Martin", "Claire", "Cardiologie", 1, None),
    (2, "Bernard", "Hugo", "Diabétologie", 1, 1),
    (3, "Petit", "Inès", "Neurologie", 1, 1),
    (4, "Robert", "Lucas", "Dermatologie", 1, 1),
    (5, "Durand", "Sophie", "Oncologie", 2, None),
    (6, "Moreau", "Thomas", "Cardiologie", 2, 5),
    (7, "Lefèvre", "Camille", "Neurologie", 2, 5),
    (8, "Garcia", "Antoine", "Cardiologie", 3, None),
    (9, "Roux", "Léa", "Diabétologie", 3, 8),
    (10, "Fournier", "Julien", "Oncologie", 4, None),
    (11, "Girard", "Manon", "Cardiologie", 4, 10),
    (12, "Bonnet", "Paul", "Médecine interne", 4, 10),
    (13, "Lambert", "Emma", "Diabétologie", 5, None),
    (14, "Favre", "Nicolas", "Oncologie", 6, None),
    (15, "Müller", "Anna", "Cardiologie", 6, 14),
    (16, "López", "Carmen", "Diabétologie", 7, None),
    (17, "Sánchez", "Javier", "Médecine interne", 7, 16),
    (18, "Dubois", "Marc", "Dermatologie", 8, None),
]

# etude_id, centre_id, pi_id, date_ouverture, objectif, nb_inclus_visés
ETUDE_CENTRES = [
    (1, 1, 1, "2024-03-15", 30, 33),
    (1, 2, 6, "2024-04-01", 25, 21),
    (1, 3, 8, "2024-05-10", 25, 26),
    (1, 4, 11, "2024-06-01", 20, 14),
    (1, 6, 15, "2024-09-01", 20, 18),
    (2, 1, 2, "2025-02-01", 20, 15),
    (2, 3, 9, "2025-03-01", 20, 9),
    (2, 5, 13, "2025-02-15", 25, 19),
    (2, 7, 16, "2025-05-01", 15, 6),
    (3, 2, 5, "2025-07-01", 20, 10),
    (3, 4, 10, "2025-08-15", 20, 7),
    (3, 6, 14, "2025-10-01", 20, 4),
    (4, 1, 3, "2023-01-20", 15, 15),
    (4, 2, 7, "2023-02-01", 15, 15),
    (5, 1, 4, None, 50, 0),
    (5, 8, 18, None, 50, 0),
]

# Paramètres propres à chaque étude
PROFIL = {
    1: dict(fin_recrut="2025-09-30", taux_echec=0.20, naiss=(1945, 1975),
            visites=[("V0", 0), ("V1", 14), ("V2", 28), ("V3", 56), ("V4", 84), ("V5", 168), ("V6", 336)],
            pas=150, pad=92, glycemie=False, abandon=0.14,
            termes=["Hypotension", "Œdème des chevilles", "Toux"]),
    2: dict(fin_recrut=None, taux_echec=0.25, naiss=(1950, 1985),
            visites=[("V0", 0), ("V1", 14), ("V2", 28), ("V3", 56), ("V4", 84), ("V5", 168), ("V6", 336)],
            pas=135, pad=84, glycemie=True, abandon=0.10,
            termes=["Hypoglycémie", "Diarrhée"]),
    3: dict(fin_recrut=None, taux_echec=0.35, naiss=(1945, 1970),
            visites=[("V0", 0), ("V1", 14), ("V2", 28), ("V3", 56), ("V4", 84), ("V5", 168), ("V6", 336)],
            pas=130, pad=80, glycemie=False, abandon=0.15,
            termes=["Éruption cutanée", "Anémie", "Fièvre", "Pneumopathie"]),
    4: dict(fin_recrut="2023-06-30", taux_echec=0.10, naiss=(1980, 2004),
            visites=[("V0", 0), ("V1", 7), ("V2", 14), ("V3", 28)],
            pas=122, pad=76, glycemie=False, abandon=0.05,
            termes=["Somnolence"]),
}

TERMES_COMMUNS = ["Céphalées", "Nausées", "Fatigue", "Vertiges",
                  "Infection respiratoire", "Douleur abdominale", "Insomnie"]

# ---------------------------------------------------------------------------
#  Génération
# ---------------------------------------------------------------------------

patients, visites, mesures, eis = [], [], [], []
pid = vid = mid = eid = 0


def rand_date(start, end):
    if end <= start:
        return start
    return plus(start, R.randint(0, (end - start).days))


def ajoute_ei(patient_id, date_survenue, termes, bras, grade=None, grave=None):
    global eid
    eid += 1
    if grade is None:
        grade = R.choices([1, 2, 3, 4], weights=[50, 32, 13, 5])[0]
    if grave is None:
        grave = grade >= 4 or (grade == 3 and R.random() < 0.3)
    if bras == "traitement":
        lien = R.choices(["certain", "probable", "possible", "improbable", "exclu"], [5, 20, 35, 25, 15])[0]
    else:
        lien = R.choices(["certain", "probable", "possible", "improbable", "exclu"], [1, 8, 26, 35, 30])[0]
    resolution = plus(date_survenue, R.randint(1, 30))
    if resolution > REF or R.random() < 0.05:
        resolution = None
    eis.append((eid, patient_id, date_survenue, R.choice(termes), grade, grave, lien, resolution))


for etude_id, centre_id, pi, ouverture, objectif, nb_inclus in ETUDE_CENTRES:
    if nb_inclus == 0:
        continue
    p = PROFIL[etude_id]
    code_etude = ETUDES[etude_id - 1][1]
    debut = d(ouverture)
    fin = d(p["fin_recrut"]) or plus(REF, -21)
    nb_echecs = round(nb_inclus * p["taux_echec"] / (1 - p["taux_echec"])) + R.randint(-1, 1)
    nb_echecs = max(nb_echecs, 1)
    statuts = [True] * nb_inclus + [False] * nb_echecs
    R.shuffle(statuts)
    dates = sorted(rand_date(debut, fin) for _ in statuts)
    termes = TERMES_COMMUNS + p["termes"]

    for n, (inclus, screening) in enumerate(zip(statuts, dates), start=1):
        pid += 1
        sexe = R.choice("FM")
        naissance = R.randint(*p["naiss"])
        code = f"{code_etude}-C{centre_id:02d}-{n:03d}"
        if not inclus:
            patients.append((pid, code, etude_id, centre_id, sexe, naissance, screening,
                             None, None, None, None))
            continue

        inclusion = plus(screening, R.randint(7, 21))
        bras = R.choice(["traitement", "placebo"])
        plan = p["visites"]

        # abandon éventuel : avant la visite n° k
        abandon_k, motif_abandon = None, None
        if R.random() < p["abandon"]:
            abandon_k = R.randint(1, len(plan) - 1)
            motif_abandon = R.choices(["retrait du consentement", "perdu de vue", "événement indésirable"],
                                      [50, 30, 20])[0]

        sortie, motif = None, None
        derniere_date = inclusion
        poids0 = R.gauss(64 if sexe == "F" else 79, 11)
        pas0, pad0 = R.gauss(p["pas"], 9), R.gauss(p["pad"], 6)
        gly0 = R.gauss(1.65, 0.22)

        for k, (tv, offset) in enumerate(plan):
            if abandon_k is not None and k == abandon_k:
                s = plus(derniere_date, R.randint(5, 40))
                if s <= REF:
                    sortie, motif = s, motif_abandon
                    break
            vid += 1
            prevue = plus(inclusion, offset)
            if k == 0:
                realisee = inclusion
            elif prevue > REF:
                realisee = None
            elif R.random() < 0.08:
                realisee = None  # visite manquée
            else:
                realisee = min(plus(prevue, R.randint(-3, 7)), REF)
            visites.append((vid, pid, tv, prevue, realisee))
            if realisee is None:
                continue
            derniere_date = realisee

            # mesures
            progression = offset / plan[-1][1]
            effet = 1.0 if bras == "traitement" else 0.25
            vals = [
                ("poids", round(poids0 + R.gauss(0, 1.2), 1), "kg"),
                ("pas", round(pas0 - (14 if etude_id == 1 else 4) * effet * progression + R.gauss(0, 5)), "mmHg"),
                ("pad", round(pad0 - (7 if etude_id == 1 else 2) * effet * progression + R.gauss(0, 4)), "mmHg"),
            ]
            if p["glycemie"]:
                vals.append(("glycemie", round(gly0 - 0.40 * effet * progression + R.gauss(0, 0.08), 2), "g/L"))
            for param, valeur, unite in vals:
                mid += 1
                mesures.append((mid, vid, param, valeur, unite))

            if k == len(plan) - 1:
                sortie, motif = realisee, "fin d'étude"

        # événements indésirables
        fin_suivi = min(sortie or REF, REF)
        lam = 1.3 if bras == "traitement" else 0.7
        nb_ei = sum(R.random() < lam / 3 for _ in range(3))
        for _ in range(nb_ei):
            ajoute_ei(pid, rand_date(inclusion, fin_suivi), termes, bras)
        if motif == "événement indésirable":
            ajoute_ei(pid, plus(sortie, -R.randint(1, 6)), termes, bras,
                      grade=R.choice([3, 4]), grave=True)

        patients.append((pid, code, etude_id, centre_id, sexe, naissance, screening,
                         inclusion, bras, sortie, motif))

# ---------------------------------------------------------------------------
#  Écriture SQL
# ---------------------------------------------------------------------------


def lit(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, dt.date):
        return f"'{v.isoformat()}'"
    return "'" + str(v).replace("'", "''") + "'"


def inserts(table, cols, rows, lot=200):
    out = []
    for i in range(0, len(rows), lot):
        chunk = rows[i:i + lot]
        vals = ",\n".join("  (" + ", ".join(lit(v) for v in r) + ")" for r in chunk)
        out.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES\n{vals};\n")
    return "\n".join(out)


etudes_rows = [(e[0], e[1], e[2], e[3], e[4], e[5], d(e[6]), d(e[7]), e[8], e[9]) for e in ETUDES]
inv_rows = []
for i, nom, prenom, spe, c, sup in INVESTIGATEURS:
    email = f"{slug(prenom)}.{slug(nom)}@{slug(CENTRES[c - 1][1].split()[-1])}-centre{c}.example"
    inv_rows.append((i, nom, prenom, spe, email, c, sup))
ec_rows = [(e, c, pi, d(o), obj) for e, c, pi, o, obj, _ in ETUDE_CENTRES]
patients.sort()

data = [
    "-- =====================================================================",
    "--  Données de la base essais_cliniques — GÉNÉRÉES par db/generate_data.py",
    "--  Ne pas modifier à la main : modifier le générateur puis le relancer.",
    "-- =====================================================================",
    "",
    "USE essais_cliniques;",
    "",
    inserts("etude", ["id", "code", "titre", "phase", "aire_therapeutique", "promoteur",
                      "date_debut", "date_fin_prevue", "objectif_inclusions", "statut"], etudes_rows),
    inserts("centre", ["id", "nom", "ville", "pays"], CENTRES),
    inserts("investigateur", ["id", "nom", "prenom", "specialite", "email", "centre_id", "superviseur_id"], inv_rows),
    inserts("etude_centre", ["etude_id", "centre_id", "investigateur_principal_id",
                             "date_ouverture", "objectif_inclusions"], ec_rows),
    inserts("patient", ["id", "code_patient", "etude_id", "centre_id", "sexe", "annee_naissance",
                        "date_screening", "date_inclusion", "bras", "date_sortie", "motif_sortie"], patients),
    inserts("visite", ["id", "patient_id", "type_visite", "date_prevue", "date_realisee"], visites),
    inserts("evenement_indesirable", ["id", "patient_id", "date_survenue", "terme", "grade", "grave",
                                      "lien_traitement", "date_resolution"], eis),
    inserts("mesure", ["id", "visite_id", "parametre", "valeur", "unite"], mesures, lot=500),
]
data_sql = "\n".join(data)
(HERE / "02_data.sql").write_text(data_sql, encoding="utf-8")
schema_sql = (HERE / "01_schema.sql").read_text(encoding="utf-8")
(HERE / "essais_cliniques.sql").write_text(schema_sql + "\n\n" + data_sql, encoding="utf-8")

print(f"etudes={len(etudes_rows)} centres={len(CENTRES)} investigateurs={len(inv_rows)} "
      f"etude_centre={len(ec_rows)} patients={len(patients)} visites={len(visites)} "
      f"ei={len(eis)} mesures={len(mesures)}")
