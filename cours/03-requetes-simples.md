# Module 3 — Requêtes simples

> **Objectif** : extraire, filtrer, trier, calculer et agréger des données avec `SELECT`, `WHERE`, `ORDER BY`, les fonctions, `GROUP BY` / `HAVING` et les sous-requêtes.
> **Durée indicative** : 8 h — c'est le cœur de la formation.

---

## 3.1 `SELECT` : choisir et calculer des colonnes

### Concept

```
SELECT  colonnes à afficher
FROM    table
```

Dans la clause `SELECT` on peut mettre :
- des **colonnes** de la table ;
- des **expressions calculées** (`objectif_inclusions * 1.1`, `2026 - annee_naissance`) ;
- des **alias** pour renommer une colonne du résultat : `expression AS nom_alias` ;
- le mot-clé **`DISTINCT`** pour supprimer les lignes en double.

### Visuel — `SELECT` choisit des colonnes (une « projection »)

```
            table centre                              SELECT nom, ville FROM centre
 ┌────┬──────────────────────────┬────────┬────────┐       ┌──────────────────────────┬────────┐
 │ id │ nom                      │ ville  │ pays   │       │ nom                      │ ville  │
 ├────┼──────────────────────────┼────────┼────────┤  ──►  ├──────────────────────────┼────────┤
 │ 1  │ Clinique du Val de Loire │ Tours  │ France │       │ Clinique du Val de Loire │ Tours  │
 │ 2  │ CHU Atlantique           │ Nantes │ France │       │ CHU Atlantique           │ Nantes │
 │ …  │ …                        │ …      │ …      │       │ …                        │ …      │
 └────┴──────────────────────────┴────────┴────────┘       └──────────────────────────┴────────┘
        ▲ ne garde que                ▲      ▲
          les colonnes demandées
```

### Exemples

**Colonnes et alias**

```sql
SELECT code AS etude, objectif_inclusions AS objectif
FROM etude;
```
<!-- resultat -->
```text
+-----------+----------+
| etude     | objectif |
+-----------+----------+
| CARDIO-01 | 120      |
| DIAB-02   | 80       |
| ONCO-03   | 60       |
| NEURO-04  | 30       |
| DERM-05   | 100      |
+-----------+----------+
5 lignes
```
<!-- /resultat -->

> Le mot `AS` est facultatif (`code etude` marche aussi), mais il rend la lecture plus claire. Si l'alias contient un espace ou un accent, entourez-le : `AS "Objectif d'inclusions"` (standard) ou `` AS `Objectif` `` (MySQL).

**Colonnes calculées** — l'âge approximatif des patients au 30 juin 2026 :

```sql
SELECT code_patient, annee_naissance, 2026 - annee_naissance AS age_approx
FROM patient;
```
<!-- resultat:5 -->
```text
+-------------------+-----------------+------------+
| code_patient      | annee_naissance | age_approx |
+-------------------+-----------------+------------+
| CARDIO-01-C01-001 | 1970            | 56         |
| CARDIO-01-C01-002 | 1966            | 60         |
| CARDIO-01-C01-003 | 1960            | 66         |
| CARDIO-01-C01-004 | 1959            | 67         |
| CARDIO-01-C01-005 | 1965            | 61         |
+-------------------+-----------------+------------+
… 262 lignes au total (5 affichées)
```
<!-- /resultat -->

**Calcul sur des colonnes numériques** — si l'on voulait augmenter tous les objectifs de 10 % :

```sql
SELECT code, objectif_inclusions, objectif_inclusions * 1.1 AS objectif_majore
FROM etude;
```
<!-- resultat -->
```text
+-----------+---------------------+-----------------+
| code      | objectif_inclusions | objectif_majore |
+-----------+---------------------+-----------------+
| CARDIO-01 | 120                 | 132.0           |
| DIAB-02   | 80                  | 88.0            |
| ONCO-03   | 60                  | 66.0            |
| NEURO-04  | 30                  | 33.0            |
| DERM-05   | 100                 | 110.0           |
+-----------+---------------------+-----------------+
5 lignes
```
<!-- /resultat -->

**`DISTINCT`** — quels pays sont représentés ?

```sql
SELECT DISTINCT pays FROM centre;
```
<!-- resultat -->
```text
+----------+
| pays     |
+----------+
| France   |
| Suisse   |
| Espagne  |
| Belgique |
+----------+
4 lignes
```
<!-- /resultat -->

`DISTINCT` porte sur **toute la ligne** du résultat :

```sql
SELECT DISTINCT etude_id, bras FROM patient;
```
<!-- resultat -->
```text
+----------+------------+
| etude_id | bras       |
+----------+------------+
| 1        | placebo    |
| 1        | traitement |
| 1        | NULL       |
| 2        | NULL       |
| 2        | placebo    |
| 2        | traitement |
| 3        | placebo    |
| 3        | NULL       |
| 3        | traitement |
| 4        | traitement |
| 4        | placebo    |
| 4        | NULL       |
+----------+------------+
12 lignes
```
<!-- /resultat -->

Remarquez les lignes avec `bras` à NULL : ce sont les patients non inclus (pas de bras attribué).

---

## 3.2 `WHERE` : filtrer les lignes

### Concept

```
SELECT  colonnes
FROM    table
WHERE   condition          ← seules les lignes où la condition est VRAIE sont gardées
```

| Opérateur | Signification | Exemple |
|---|---|---|
| `=` `<>` (ou `!=`) | égal, différent | `pays = 'France'` |
| `<` `<=` `>` `>=` | comparaisons (nombres, dates, textes) | `annee_naissance < 1950` |
| `BETWEEN a AND b` | entre a et b **inclus** | `grade BETWEEN 2 AND 3` |
| `IN (v1, v2, …)` | dans une liste | `pays IN ('Suisse', 'Belgique')` |
| `LIKE 'motif'` | ressemble à (`%` = n'importe quelle suite, `_` = un caractère) | `code LIKE 'CARDIO%'` |
| `IS NULL` / `IS NOT NULL` | valeur absente / présente | `date_inclusion IS NULL` |
| `AND` `OR` `NOT` | combiner des conditions | |

### Visuel — `WHERE` choisit des lignes (une « restriction »)

```
          table centre                               WHERE pays <> 'France'
 ┌────┬─────────────────────────────┬────────┬──────────┐
 │ id │ nom                         │ ville  │ pays     │
 ├────┼─────────────────────────────┼────────┼──────────┤
 │ 1  │ Clinique du Val de Loire    │ Tours  │ France   │   ✘ écartée
 │ …  │ …                           │ …      │ France   │   ✘
 │ 6  │ Clinique du Léman           │ Genève │ Suisse   │   ✔ gardée
 │ 7  │ Hospital del Sol            │Valencia│ Espagne  │   ✔ gardée
 │ 8  │ Centre Médical des Ardennes │ Liège  │ Belgique │   ✔ gardée
 └────┴─────────────────────────────┴────────┴──────────┘
```

### Exemples

**Égalité sur un texte** (apostrophes obligatoires) :

```sql
SELECT nom, ville FROM centre WHERE pays = 'France';
```
<!-- resultat -->
```text
+-----------------------------+-------------+
| nom                         | ville       |
+-----------------------------+-------------+
| Clinique du Val de Loire    | Tours       |
| CHU Atlantique              | Nantes      |
| Hôpital Saint-Roch          | Montpellier |
| Centre Hospitalier du Rhône | Lyon        |
| Clinique des Flandres       | Lille       |
+-----------------------------+-------------+
5 lignes
```
<!-- /resultat -->

**Comparaison sur un nombre** — les patients nés avant 1950 :

```sql
SELECT code_patient, annee_naissance FROM patient WHERE annee_naissance < 1950;
```
<!-- resultat:5 -->
```text
+-------------------+-----------------+
| code_patient      | annee_naissance |
+-------------------+-----------------+
| CARDIO-01-C01-011 | 1949            |
| CARDIO-01-C01-013 | 1949            |
| CARDIO-01-C01-018 | 1947            |
| CARDIO-01-C01-021 | 1946            |
| CARDIO-01-C01-032 | 1947            |
+-------------------+-----------------+
… 31 lignes au total (5 affichées)
```
<!-- /resultat -->

**Comparaison sur une date** — les patients screenés depuis le 1er janvier 2026 :

```sql
SELECT code_patient, date_screening
FROM patient
WHERE date_screening >= '2026-01-01';
```
<!-- resultat:5 -->
```text
+-----------------+----------------+
| code_patient    | date_screening |
+-----------------+----------------+
| DIAB-02-C01-019 | 2026-01-03     |
| DIAB-02-C01-020 | 2026-03-02     |
| DIAB-02-C01-021 | 2026-04-17     |
| DIAB-02-C03-008 | 2026-01-15     |
| DIAB-02-C03-009 | 2026-03-21     |
+-----------------+----------------+
… 26 lignes au total (5 affichées)
```
<!-- /resultat -->

**`BETWEEN`** — les événements indésirables survenus au premier trimestre 2026 :

```sql
SELECT id, terme, date_survenue
FROM evenement_indesirable
WHERE date_survenue BETWEEN '2026-01-01' AND '2026-03-31';
```
<!-- resultat:5 -->
```text
+----+------------------------+---------------+
| id | terme                  | date_survenue |
+----+------------------------+---------------+
| 11 | Infection respiratoire | 2026-01-11    |
| 18 | Douleur abdominale     | 2026-03-13    |
| 19 | Douleur abdominale     | 2026-03-16    |
| 22 | Douleur abdominale     | 2026-02-21    |
| 39 | Œdème des chevilles    | 2026-02-14    |
+----+------------------------+---------------+
… 29 lignes au total (5 affichées)
```
<!-- /resultat -->

**`IN`** — les centres hors de France, autrement :

```sql
SELECT nom, pays FROM centre WHERE pays IN ('Suisse', 'Espagne', 'Belgique');
```
<!-- resultat -->
```text
+-----------------------------+----------+
| nom                         | pays     |
+-----------------------------+----------+
| Clinique du Léman           | Suisse   |
| Hospital del Sol            | Espagne  |
| Centre Médical des Ardennes | Belgique |
+-----------------------------+----------+
3 lignes
```
<!-- /resultat -->

**`LIKE`** — les patients de l'étude cardiologie, d'après leur code :

```sql
SELECT code_patient FROM patient WHERE code_patient LIKE 'CARDIO%';
```
<!-- resultat:3 -->
```text
+-------------------+
| code_patient      |
+-------------------+
| CARDIO-01-C01-001 |
| CARDIO-01-C01-002 |
| CARDIO-01-C01-003 |
+-------------------+
… 136 lignes au total (3 affichées)
```
<!-- /resultat -->

```
  Motifs LIKE :
  'CARDIO%'    commence par CARDIO
  '%-C01-%'    contient « -C01- »  (patients du centre 1)
  '%1'         se termine par 1
  'V_'         V suivi d'exactement un caractère (V0 … V9)
```

**`IS NULL`** — les patients non inclus (échecs de screening) :

```sql
SELECT code_patient, date_screening, date_inclusion
FROM patient
WHERE date_inclusion IS NULL;
```
<!-- resultat:5 -->
```text
+-------------------+----------------+----------------+
| code_patient      | date_screening | date_inclusion |
+-------------------+----------------+----------------+
| CARDIO-01-C01-005 | 2024-06-28     | NULL           |
| CARDIO-01-C01-008 | 2024-07-25     | NULL           |
| CARDIO-01-C01-011 | 2024-11-04     | NULL           |
| CARDIO-01-C01-020 | 2025-04-30     | NULL           |
| CARDIO-01-C01-022 | 2025-05-21     | NULL           |
+-------------------+----------------+----------------+
… 50 lignes au total (5 affichées)
```
<!-- /resultat -->

**Combiner avec `AND` / `OR`** — les EI graves de grade 4 :

```sql
SELECT id, patient_id, terme, grade
FROM evenement_indesirable
WHERE grave = TRUE AND grade = 4;
```
<!-- resultat:5 -->
```text
+-----+------------+------------------------+-------+
| id  | patient_id | terme                  | grade |
+-----+------------+------------------------+-------+
| 10  | 16         | Douleur abdominale     | 4     |
| 13  | 23         | Hypotension            | 4     |
| 76  | 86         | Infection respiratoire | 4     |
| 104 | 131        | Vertiges               | 4     |
| 122 | 158        | Céphalées              | 4     |
+-----+------------+------------------------+-------+
… 11 lignes au total (5 affichées)
```
<!-- /resultat -->

**Attention à la priorité : `AND` passe avant `OR`.** On veut les patientes (F) nées avant 1950 ou après 1990 :

```sql
-- ❌ FAUX : se lit « (F et avant 1950) OU (après 1990, homme ou femme) »
SELECT code_patient, sexe, annee_naissance
FROM patient
WHERE sexe = 'F' AND annee_naissance < 1950 OR annee_naissance > 1990;
```
<!-- resultat:6 -->
```text
+-------------------+------+-----------------+
| code_patient      | sexe | annee_naissance |
+-------------------+------+-----------------+
| CARDIO-01-C01-011 | F    | 1949            |
| CARDIO-01-C01-018 | F    | 1947            |
| CARDIO-01-C01-021 | F    | 1946            |
| CARDIO-01-C01-037 | F    | 1945            |
| CARDIO-01-C02-002 | F    | 1947            |
| CARDIO-01-C02-011 | F    | 1945            |
+-------------------+------+-----------------+
… 35 lignes au total (6 affichées)
```
<!-- /resultat -->

```sql
-- ✅ JUSTE : des parenthèses
SELECT code_patient, sexe, annee_naissance
FROM patient
WHERE sexe = 'F' AND (annee_naissance < 1950 OR annee_naissance > 1990);
```
<!-- resultat:6 -->
```text
+-------------------+------+-----------------+
| code_patient      | sexe | annee_naissance |
+-------------------+------+-----------------+
| CARDIO-01-C01-011 | F    | 1949            |
| CARDIO-01-C01-018 | F    | 1947            |
| CARDIO-01-C01-021 | F    | 1946            |
| CARDIO-01-C01-037 | F    | 1945            |
| CARDIO-01-C02-002 | F    | 1947            |
| CARDIO-01-C02-011 | F    | 1945            |
+-------------------+------+-----------------+
… 24 lignes au total (6 affichées)
```
<!-- /resultat -->

> 💡 Dès qu'un `WHERE` mélange `AND` et `OR`, mettez des parenthèses, même quand elles ne sont pas nécessaires.

### Le cas particulier de NULL

Toute comparaison avec NULL donne… **NULL** (« inconnu »), et `WHERE` ne garde que ce qui est **VRAI**.

```
   date_inclusion = NULL      → NULL (inconnu)  → ligne écartée, TOUJOURS   ❌
   date_inclusion IS NULL     → VRAI ou FAUX                                ✅

   Logique à 3 valeurs :      VRAI AND NULL = NULL     VRAI OR NULL = VRAI
                              FAUX AND NULL = FAUX     FAUX OR NULL = NULL
                              NOT NULL      = NULL
```

```sql
-- ❌ ne renvoie AUCUNE ligne, sans erreur !
SELECT COUNT(*) AS nb FROM patient WHERE date_inclusion = NULL;
```
<!-- resultat -->
```text
+----+
| nb |
+----+
| 0  |
+----+
1 ligne
```
<!-- /resultat -->

```sql
-- ✅
SELECT COUNT(*) AS nb FROM patient WHERE date_inclusion IS NULL;
```
<!-- resultat -->
```text
+----+
| nb |
+----+
| 50 |
+----+
1 ligne
```
<!-- /resultat -->

Autre conséquence : `bras <> 'placebo'` **n'inclut pas** les patients dont le bras est NULL.

---

## 3.3 `ORDER BY` et limitation des résultats

### Concept

```
SELECT …
FROM …
WHERE …
ORDER BY colonne1 [ASC | DESC], colonne2 [ASC | DESC]   ← ASC (croissant) par défaut
LIMIT n                                                  ← MySQL : seulement les n premières lignes
```

Sans `ORDER BY`, **l'ordre des lignes n'est pas garanti**, même s'il semble stable.

### Exemples

**Trier par une colonne** — les études de la plus grande à la plus petite :

```sql
SELECT code, objectif_inclusions
FROM etude
ORDER BY objectif_inclusions DESC;
```
<!-- resultat -->
```text
+-----------+---------------------+
| code      | objectif_inclusions |
+-----------+---------------------+
| CARDIO-01 | 120                 |
| DERM-05   | 100                 |
| DIAB-02   | 80                  |
| ONCO-03   | 60                  |
| NEURO-04  | 30                  |
+-----------+---------------------+
5 lignes
```
<!-- /resultat -->

**Trier sur plusieurs colonnes** — par pays, puis par ville :

```sql
SELECT pays, ville, nom
FROM centre
ORDER BY pays, ville;
```
<!-- resultat -->
```text
+----------+-------------+-----------------------------+
| pays     | ville       | nom                         |
+----------+-------------+-----------------------------+
| Belgique | Liège       | Centre Médical des Ardennes |
| Espagne  | Valencia    | Hospital del Sol            |
| France   | Lille       | Clinique des Flandres       |
| France   | Lyon        | Centre Hospitalier du Rhône |
| France   | Montpellier | Hôpital Saint-Roch          |
| France   | Nantes      | CHU Atlantique              |
| France   | Tours       | Clinique du Val de Loire    |
| Suisse   | Genève      | Clinique du Léman           |
+----------+-------------+-----------------------------+
8 lignes
```
<!-- /resultat -->

**Le « top N »** — les 5 patients les plus âgés :

```sql
SELECT code_patient, annee_naissance
FROM patient
ORDER BY annee_naissance, code_patient
LIMIT 5;
```
<!-- resultat -->
```text
+-------------------+-----------------+
| code_patient      | annee_naissance |
+-------------------+-----------------+
| CARDIO-01-C01-037 | 1945            |
| CARDIO-01-C02-011 | 1945            |
| CARDIO-01-C03-006 | 1945            |
| CARDIO-01-C03-014 | 1945            |
| CARDIO-01-C03-027 | 1945            |
+-------------------+-----------------+
5 lignes
```
<!-- /resultat -->

> On a ajouté `code_patient` en second critère : sans lui, en cas d'égalité d'année, l'ordre (et donc le « top 5 ») pourrait varier d'une exécution à l'autre.

**Trier par un alias** :

```sql
SELECT code_patient, 2026 - annee_naissance AS age_approx
FROM patient
ORDER BY age_approx DESC
LIMIT 3;
```
<!-- resultat -->
```text
+-------------------+------------+
| code_patient      | age_approx |
+-------------------+------------+
| CARDIO-01-C01-037 | 81         |
| CARDIO-01-C02-011 | 81         |
| CARDIO-01-C03-006 | 81         |
+-------------------+------------+
3 lignes
```
<!-- /resultat -->

**Pagination** — `LIMIT n OFFSET d` : n lignes, en sautant les d premières (lignes 6 à 10) :

```sql
SELECT code_patient, annee_naissance
FROM patient
ORDER BY annee_naissance, code_patient
LIMIT 5 OFFSET 5;
```
<!-- resultat -->
```text
+-------------------+-----------------+
| code_patient      | annee_naissance |
+-------------------+-----------------+
| ONCO-03-C02-005   | 1945            |
| ONCO-03-C04-008   | 1945            |
| ONCO-03-C06-006   | 1945            |
| CARDIO-01-C01-021 | 1946            |
| CARDIO-01-C02-019 | 1946            |
+-------------------+-----------------+
5 lignes
```
<!-- /resultat -->

**Où vont les NULL ?** En MySQL, ils sont placés **en premier** en tri croissant :

```sql
SELECT code_patient, date_inclusion
FROM patient
ORDER BY date_inclusion
LIMIT 3;
```
<!-- resultat -->
```text
+-------------------+----------------+
| code_patient      | date_inclusion |
+-------------------+----------------+
| CARDIO-01-C01-005 | NULL           |
| CARDIO-01-C01-008 | NULL           |
| CARDIO-01-C01-011 | NULL           |
+-------------------+----------------+
3 lignes
```
<!-- /resultat -->

---

## 3.4 Les fonctions utiles

### Fonctions sur le texte

| Fonction | Rôle | Exemple → résultat |
|---|---|---|
| `CONCAT(a, b, …)` | assembler | `CONCAT(prenom, ' ', nom)` → `Claire Martin` |
| `UPPER(t)` / `LOWER(t)` | majuscules / minuscules | `UPPER(nom)` → `MARTIN` |
| `CHAR_LENGTH(t)` | nombre de caractères | `CHAR_LENGTH('Tours')` → `5` |
| `SUBSTRING(t, début, longueur)` | extraire | `SUBSTRING('CARDIO-01', 1, 6)` → `CARDIO` |
| `LEFT(t, n)` / `RIGHT(t, n)` | début / fin | `RIGHT('V3', 1)` → `3` |
| `REPLACE(t, a, b)` | remplacer | `REPLACE('CARDIO-01', '-', '_')` → `CARDIO_01` |
| `TRIM(t)` | retirer les espaces autour | `TRIM('  Tours ')` → `Tours` |

```sql
SELECT CONCAT(UPPER(nom), ' ', prenom) AS investigateur,
       CHAR_LENGTH(specialite)         AS longueur,
       LEFT(email, 5)                  AS debut_email
FROM investigateur;
```
<!-- resultat:5 -->
```text
+---------------+----------+-------------+
| investigateur | longueur | debut_email |
+---------------+----------+-------------+
| MARTIN Claire | 11       | clair       |
| BERNARD Hugo  | 12       | hugo.       |
| PETIT Inès    | 10       | ines.       |
| ROBERT Lucas  | 12       | lucas       |
| DURAND Sophie | 9        | sophi       |
+---------------+----------+-------------+
… 18 lignes au total (5 affichées)
```
<!-- /resultat -->

```sql
-- l'étude et le centre se lisent dans le code patient : CARDIO-01-C01-003
SELECT code_patient,
       SUBSTRING(code_patient, 1, CHAR_LENGTH(code_patient) - 8) AS etude,
       RIGHT(code_patient, 3)                                    AS numero
FROM patient
LIMIT 3;
```
<!-- resultat -->
```text
+-------------------+-----------+--------+
| code_patient      | etude     | numero |
+-------------------+-----------+--------+
| CARDIO-01-C01-001 | CARDIO-01 | 001    |
| CARDIO-01-C01-002 | CARDIO-01 | 002    |
| CARDIO-01-C01-003 | CARDIO-01 | 003    |
+-------------------+-----------+--------+
3 lignes
```
<!-- /resultat -->

### Fonctions numériques

| Fonction | Rôle | Exemple → résultat |
|---|---|---|
| `ROUND(x, n)` | arrondir à n décimales | `ROUND(3.14159, 2)` → `3.14` |
| `FLOOR(x)` / `CEIL(x)` | arrondi inférieur / supérieur | `FLOOR(3.7)` → `3` |
| `ABS(x)` | valeur absolue | `ABS(-5)` → `5` |
| `x % y` ou `MOD(x, y)` | reste de la division | `MOD(10, 3)` → `1` |

### Fonctions sur les dates

| Fonction (MySQL) | Rôle | Exemple → résultat |
|---|---|---|
| `YEAR(d)`, `MONTH(d)`, `DAY(d)` | extraire une partie | `YEAR('2026-06-30')` → `2026` |
| `DATEDIFF(d1, d2)` | nombre de jours `d1 − d2` | `DATEDIFF('2026-06-30', '2026-06-01')` → `29` |
| `DATE_ADD(d, INTERVAL n unité)` | ajouter | `DATE_ADD('2026-06-30', INTERVAL 1 MONTH)` → `2026-07-30` |
| `TIMESTAMPDIFF(unité, d1, d2)` | écart en MONTH, YEAR… (`d2 − d1`) | `TIMESTAMPDIFF(MONTH, '2026-01-15', '2026-06-30')` → `5` |
| `DATE_FORMAT(d, format)` | mettre en forme | `DATE_FORMAT('2026-06-30', '%d/%m/%Y')` → `30/06/2026` |
| `CURRENT_DATE` | la date du jour | |

**Délai entre screening et inclusion** :

```sql
SELECT code_patient, date_screening, date_inclusion,
       DATEDIFF(date_inclusion, date_screening) AS delai_jours
FROM patient
WHERE date_inclusion IS NOT NULL;
```
<!-- resultat:5 -->
```text
+-------------------+----------------+----------------+-------------+
| code_patient      | date_screening | date_inclusion | delai_jours |
+-------------------+----------------+----------------+-------------+
| CARDIO-01-C01-001 | 2024-04-09     | 2024-04-30     | 21          |
| CARDIO-01-C01-002 | 2024-04-09     | 2024-04-28     | 19          |
| CARDIO-01-C01-003 | 2024-05-04     | 2024-05-18     | 14          |
| CARDIO-01-C01-004 | 2024-06-15     | 2024-06-24     | 9           |
| CARDIO-01-C01-006 | 2024-07-12     | 2024-07-24     | 12          |
+-------------------+----------------+----------------+-------------+
… 212 lignes au total (5 affichées)
```
<!-- /resultat -->

**Mois d'inclusion** (pour compter les inclusions par mois, voir 3.6) :

```sql
SELECT code_patient, date_inclusion,
       YEAR(date_inclusion)  AS annee,
       MONTH(date_inclusion) AS mois,
       DATE_FORMAT(date_inclusion, '%Y-%m') AS annee_mois
FROM patient
WHERE date_inclusion IS NOT NULL
LIMIT 4;
```
<!-- resultat -->
```text
+-------------------+----------------+-------+------+------------+
| code_patient      | date_inclusion | annee | mois | annee_mois |
+-------------------+----------------+-------+------+------------+
| CARDIO-01-C01-001 | 2024-04-30     | 2024  | 4    | 2024-04    |
| CARDIO-01-C01-002 | 2024-04-28     | 2024  | 4    | 2024-04    |
| CARDIO-01-C01-003 | 2024-05-18     | 2024  | 5    | 2024-05    |
| CARDIO-01-C01-004 | 2024-06-24     | 2024  | 6    | 2024-06    |
+-------------------+----------------+-------+------+------------+
4 lignes
```
<!-- /resultat -->

**Retard d'une visite** (réalisée après la date prévue) :

```sql
SELECT id, type_visite, date_prevue, date_realisee,
       DATEDIFF(date_realisee, date_prevue) AS retard_jours
FROM visite
WHERE date_realisee > date_prevue
ORDER BY retard_jours DESC
LIMIT 5;
```
<!-- resultat -->
```text
+----+-------------+-------------+---------------+--------------+
| id | type_visite | date_prevue | date_realisee | retard_jours |
+----+-------------+-------------+---------------+--------------+
| 14 | V6          | 2025-03-30  | 2025-04-06    | 7            |
| 18 | V3          | 2024-07-13  | 2024-07-20    | 7            |
| 20 | V5          | 2024-11-02  | 2024-11-09    | 7            |
| 31 | V2          | 2024-08-21  | 2024-08-28    | 7            |
| 34 | V5          | 2025-01-08  | 2025-01-15    | 7            |
+----+-------------+-------------+---------------+--------------+
5 lignes
```
<!-- /resultat -->

**Date limite** — une visite prévue doit être faite au plus tard 7 jours après la date prévue :

```sql
SELECT id, date_prevue, DATE_ADD(date_prevue, INTERVAL 7 DAY) AS date_limite
FROM visite
LIMIT 3;
```
<!-- resultat -->
```text
+----+-------------+-------------+
| id | date_prevue | date_limite |
+----+-------------+-------------+
| 1  | 2024-04-30  | 2024-05-07  |
| 2  | 2024-05-14  | 2024-05-21  |
| 3  | 2024-05-28  | 2024-06-04  |
+----+-------------+-------------+
3 lignes
```
<!-- /resultat -->

> 💡 Dans cette formation, « aujourd'hui » = `'2026-06-30'` (date de référence des données). Dans la vraie vie, on écrirait `CURRENT_DATE`.

### `CASE WHEN` : le « SI » du SQL

```
CASE
    WHEN condition1 THEN valeur1
    WHEN condition2 THEN valeur2
    ELSE valeur_par_defaut          ← facultatif (sinon NULL)
END
```

Les conditions sont testées **dans l'ordre** ; la première vraie l'emporte.

```sql
SELECT code_patient, annee_naissance,
       CASE
           WHEN 2026 - annee_naissance < 40 THEN 'moins de 40 ans'
           WHEN 2026 - annee_naissance < 65 THEN '40-64 ans'
           ELSE '65 ans et plus'
       END AS classe_age
FROM patient
LIMIT 5;
```
<!-- resultat -->
```text
+-------------------+-----------------+----------------+
| code_patient      | annee_naissance | classe_age     |
+-------------------+-----------------+----------------+
| CARDIO-01-C01-001 | 1970            | 40-64 ans      |
| CARDIO-01-C01-002 | 1966            | 40-64 ans      |
| CARDIO-01-C01-003 | 1960            | 65 ans et plus |
| CARDIO-01-C01-004 | 1959            | 65 ans et plus |
| CARDIO-01-C01-005 | 1965            | 40-64 ans      |
+-------------------+-----------------+----------------+
5 lignes
```
<!-- /resultat -->

```sql
-- un statut lisible à partir des dates
SELECT code_patient,
       CASE
           WHEN date_inclusion IS NULL THEN 'échec de screening'
           WHEN date_sortie IS NULL    THEN 'en cours'
           ELSE CONCAT('sorti : ', motif_sortie)
       END AS statut
FROM patient
LIMIT 6;
```
<!-- resultat -->
```text
+-------------------+---------------------+
| code_patient      | statut              |
+-------------------+---------------------+
| CARDIO-01-C01-001 | sorti : fin d'étude |
| CARDIO-01-C01-002 | sorti : fin d'étude |
| CARDIO-01-C01-003 | sorti : fin d'étude |
| CARDIO-01-C01-004 | sorti : fin d'étude |
| CARDIO-01-C01-005 | échec de screening  |
| CARDIO-01-C01-006 | sorti : fin d'étude |
+-------------------+---------------------+
6 lignes
```
<!-- /resultat -->

### `COALESCE` : remplacer un NULL

`COALESCE(a, b, c…)` renvoie la **première valeur non NULL**.

```sql
SELECT code_patient,
       COALESCE(bras, 'non randomisé')   AS bras,
       COALESCE(motif_sortie, '—')       AS motif
FROM patient
LIMIT 4;
```
<!-- resultat -->
```text
+-------------------+------------+-------------+
| code_patient      | bras       | motif       |
+-------------------+------------+-------------+
| CARDIO-01-C01-001 | placebo    | fin d'étude |
| CARDIO-01-C01-002 | placebo    | fin d'étude |
| CARDIO-01-C01-003 | traitement | fin d'étude |
| CARDIO-01-C01-004 | placebo    | fin d'étude |
+-------------------+------------+-------------+
4 lignes
```
<!-- /resultat -->

---

## 3.5 Les fonctions d'agrégation

### Concept

Une fonction d'agrégation **résume plusieurs lignes en une seule valeur**.

| Fonction | Résultat | NULL ? |
|---|---|---|
| `COUNT(*)` | nombre de **lignes** | compte tout |
| `COUNT(colonne)` | nombre de valeurs **non NULL** | ignorés |
| `COUNT(DISTINCT colonne)` | nombre de valeurs **différentes** non NULL | ignorés |
| `SUM(colonne)` | somme | ignorés |
| `AVG(colonne)` | moyenne | ignorés (ne comptent pas au dénominateur !) |
| `MIN(colonne)` / `MAX(colonne)` | plus petite / plus grande valeur (nombres, dates, textes) | ignorés |

### Visuel

```
  patient.date_inclusion              COUNT(*)              = 5
  ┌────────────┐                      COUNT(date_inclusion) = 3   (les NULL ne comptent pas)
  │ 2024-04-30 │                      MIN(date_inclusion)   = 2024-04-30
  │ NULL       │   ──── agrégats ──►  MAX(date_inclusion)   = 2025-01-12
  │ 2024-06-02 │
  │ NULL       │
  │ 2025-01-12 │
  └────────────┘
```

### Exemples

```sql
SELECT COUNT(*)                 AS nb_patients_screenes,
       COUNT(date_inclusion)    AS nb_inclus,
       COUNT(DISTINCT etude_id) AS nb_etudes_avec_patients
FROM patient;
```
<!-- resultat -->
```text
+----------------------+-----------+-------------------------+
| nb_patients_screenes | nb_inclus | nb_etudes_avec_patients |
+----------------------+-----------+-------------------------+
| 262                  | 212       | 4                       |
+----------------------+-----------+-------------------------+
1 ligne
```
<!-- /resultat -->

```sql
SELECT MIN(annee_naissance)        AS plus_ancien,
       MAX(annee_naissance)        AS plus_recent,
       ROUND(AVG(annee_naissance)) AS annee_moyenne
FROM patient;
```
<!-- resultat -->
```text
+-------------+-------------+---------------+
| plus_ancien | plus_recent | annee_moyenne |
+-------------+-------------+---------------+
| 1945        | 2004        | 1965.0        |
+-------------+-------------+---------------+
1 ligne
```
<!-- /resultat -->

```sql
SELECT SUM(objectif_inclusions) AS objectif_total FROM etude;
```
<!-- resultat -->
```text
+----------------+
| objectif_total |
+----------------+
| 390            |
+----------------+
1 ligne
```
<!-- /resultat -->

```sql
-- premier et dernier screening de l'étude 2
SELECT MIN(date_screening) AS premier, MAX(date_screening) AS dernier
FROM patient
WHERE etude_id = 2;
```
<!-- resultat -->
```text
+------------+------------+
| premier    | dernier    |
+------------+------------+
| 2025-02-10 | 2026-05-19 |
+------------+------------+
1 ligne
```
<!-- /resultat -->

**Un taux** : la part de patients inclus. Astuce : `SUM(CASE WHEN … THEN 1 ELSE 0 END)` compte les lignes qui vérifient une condition.

```sql
SELECT COUNT(*) AS screenes,
       SUM(CASE WHEN date_inclusion IS NULL THEN 1 ELSE 0 END) AS echecs,
       ROUND(100 * SUM(CASE WHEN date_inclusion IS NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS taux_echec_pct
FROM patient;
```
<!-- resultat -->
```text
+----------+--------+----------------+
| screenes | echecs | taux_echec_pct |
+----------+--------+----------------+
| 262      | 50     | 19.1           |
+----------+--------+----------------+
1 ligne
```
<!-- /resultat -->

---

## 3.6 `GROUP BY` et `HAVING` : agréger par groupe

### Concept

`GROUP BY` découpe les lignes en **groupes** (une valeur de la colonne = un groupe), puis calcule les agrégats **pour chaque groupe**. Résultat : **une ligne par groupe**.

```
SELECT  colonne_de_groupe, AGREGAT(…)
FROM    table
WHERE   condition sur les LIGNES          ← avant le regroupement
GROUP BY colonne_de_groupe
HAVING  condition sur les GROUPES         ← après le regroupement (peut utiliser des agrégats)
```

### Visuel

```
 patient (extrait)                      GROUP BY etude_id               COUNT(*)
 ┌────┬──────────┐               ┌─────────────────────────┐        ┌──────────┬──────┐
 │ id │ etude_id │               │ etude_id = 1            │        │ etude_id │ nb   │
 ├────┼──────────┤               │  id 1, id 2, id 3, …    │ ─────► │ 1        │ 136  │
 │ 1  │ 1        │   ───────►    ├─────────────────────────┤        │ 2        │  64  │
 │ 2  │ 1        │               │ etude_id = 2            │ ─────► │ 3        │  30  │
 │ …  │ …        │               │  …                      │        │ 4        │  32  │
 │ 140│ 2        │               ├─────────────────────────┤        └──────────┴──────┘
 │ …  │ …        │               │ etude_id = 3  …         │
 └────┴──────────┘               └─────────────────────────┘
                                   (les nombres affichés ici sont illustratifs)
```

### Exemples

**Nombre de patients screenés et inclus par étude** :

```sql
SELECT etude_id,
       COUNT(*)              AS screenes,
       COUNT(date_inclusion) AS inclus
FROM patient
GROUP BY etude_id;
```
<!-- resultat -->
```text
+----------+----------+--------+
| etude_id | screenes | inclus |
+----------+----------+--------+
| 1        | 136      | 112    |
| 2        | 64       | 49     |
| 3        | 30       | 21     |
| 4        | 32       | 30     |
+----------+----------+--------+
4 lignes
```
<!-- /resultat -->

**Grouper sur plusieurs colonnes** — inclus par étude et par bras :

```sql
SELECT etude_id, bras, COUNT(*) AS nb
FROM patient
WHERE date_inclusion IS NOT NULL
GROUP BY etude_id, bras
ORDER BY etude_id, bras;
```
<!-- resultat -->
```text
+----------+------------+----+
| etude_id | bras       | nb |
+----------+------------+----+
| 1        | placebo    | 60 |
| 1        | traitement | 52 |
| 2        | placebo    | 26 |
| 2        | traitement | 23 |
| 3        | placebo    | 12 |
| 3        | traitement | 9  |
| 4        | placebo    | 16 |
| 4        | traitement | 14 |
+----------+------------+----+
8 lignes
```
<!-- /resultat -->

**Répartition des EI par grade** :

```sql
SELECT grade,
       COUNT(*)                                   AS nb_ei,
       SUM(CASE WHEN grave THEN 1 ELSE 0 END)     AS dont_graves
FROM evenement_indesirable
GROUP BY grade
ORDER BY grade;
```
<!-- resultat -->
```text
+-------+-------+-------------+
| grade | nb_ei | dont_graves |
+-------+-------+-------------+
| 1     | 101   | 0           |
| 2     | 68    | 0           |
| 3     | 28    | 15          |
| 4     | 11    | 11          |
+-------+-------+-------------+
4 lignes
```
<!-- /resultat -->

**Les termes d'EI les plus fréquents** :

```sql
SELECT terme, COUNT(*) AS nb
FROM evenement_indesirable
GROUP BY terme
ORDER BY nb DESC
LIMIT 5;
```
<!-- resultat -->
```text
+---------------------+----+
| terme               | nb |
+---------------------+----+
| Douleur abdominale  | 34 |
| Vertiges            | 24 |
| Fatigue             | 23 |
| Céphalées           | 20 |
| Œdème des chevilles | 17 |
+---------------------+----+
5 lignes
```
<!-- /resultat -->

**Grouper sur une expression** — inclusions par mois (KPI de rythme de recrutement) :

```sql
SELECT DATE_FORMAT(date_inclusion, '%Y-%m') AS mois, COUNT(*) AS inclusions
FROM patient
WHERE etude_id = 2 AND date_inclusion IS NOT NULL
GROUP BY DATE_FORMAT(date_inclusion, '%Y-%m')
ORDER BY mois;
```
<!-- resultat:20 -->
```text
+---------+------------+
| mois    | inclusions |
+---------+------------+
| 2025-03 | 6          |
| 2025-04 | 4          |
| 2025-05 | 5          |
| 2025-06 | 2          |
| 2025-07 | 5          |
| 2025-08 | 3          |
| 2025-09 | 1          |
| 2025-10 | 3          |
| 2025-11 | 1          |
| 2025-12 | 6          |
| 2026-01 | 4          |
| 2026-02 | 2          |
| 2026-03 | 2          |
| 2026-04 | 2          |
| 2026-05 | 2          |
| 2026-06 | 1          |
+---------+------------+
16 lignes
```
<!-- /resultat -->

**Grouper sur un `CASE`** — patients par classe d'âge :

```sql
SELECT CASE
           WHEN 2026 - annee_naissance < 40 THEN '1. moins de 40 ans'
           WHEN 2026 - annee_naissance < 65 THEN '2. 40-64 ans'
           ELSE '3. 65 ans et plus'
       END AS classe_age,
       COUNT(*) AS nb
FROM patient
GROUP BY classe_age
ORDER BY classe_age;
```
<!-- resultat -->
```text
+--------------------+-----+
| classe_age         | nb  |
+--------------------+-----+
| 1. moins de 40 ans | 20  |
| 2. 40-64 ans       | 116 |
| 3. 65 ans et plus  | 126 |
+--------------------+-----+
3 lignes
```
<!-- /resultat -->

**`HAVING`** — les termes d'EI déclarés plus de 20 fois :

```sql
SELECT terme, COUNT(*) AS nb
FROM evenement_indesirable
GROUP BY terme
HAVING COUNT(*) > 20
ORDER BY nb DESC;
```
<!-- resultat -->
```text
+--------------------+----+
| terme              | nb |
+--------------------+----+
| Douleur abdominale | 34 |
| Vertiges           | 24 |
| Fatigue            | 23 |
+--------------------+----+
3 lignes
```
<!-- /resultat -->

**`WHERE` et `HAVING` ensemble** — parmi les EI **graves** (filtre de lignes), les patients qui en ont eu **au moins 2** (filtre de groupes) :

```sql
SELECT patient_id, COUNT(*) AS nb_ei_graves
FROM evenement_indesirable
WHERE grave = TRUE
GROUP BY patient_id
HAVING COUNT(*) >= 2;
```
<!-- resultat -->
```text
+------------+--------------+
| patient_id | nb_ei_graves |
+------------+--------------+
| 176        | 2            |
+------------+--------------+
1 ligne
```
<!-- /resultat -->

**Le taux d'échec de screening par étude** (un vrai KPI) :

```sql
SELECT etude_id,
       COUNT(*) AS screenes,
       ROUND(100 * SUM(CASE WHEN date_inclusion IS NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS taux_echec_pct
FROM patient
GROUP BY etude_id
ORDER BY taux_echec_pct DESC;
```
<!-- resultat -->
```text
+----------+----------+----------------+
| etude_id | screenes | taux_echec_pct |
+----------+----------+----------------+
| 3        | 30       | 30.0           |
| 2        | 64       | 23.4           |
| 1        | 136      | 17.6           |
| 4        | 32       | 6.3            |
+----------+----------+----------------+
4 lignes
```
<!-- /resultat -->

### La règle d'or du `GROUP BY`

> Dans le `SELECT` d'une requête groupée, chaque colonne doit être **soit dans le `GROUP BY`, soit dans une fonction d'agrégation**.

```sql
-- ❌ Erreur : de quel patient afficher le code, alors qu'il y a une ligne par étude ?
SELECT etude_id, code_patient, COUNT(*)
FROM patient
GROUP BY etude_id;
```

```text
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause and contains
nonaggregated column 'essais_cliniques.patient.code_patient' which is not functionally
dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

---

## 3.7 L'ordre d'exécution d'une requête

### Concept

On **écrit** une requête dans un ordre, mais le SGBD l'**exécute** dans un autre. Le connaître explique la plupart des erreurs.

### Visuel

```
   ORDRE D'ÉCRITURE                  ORDRE LOGIQUE D'EXÉCUTION

   SELECT   …      (5)               1. FROM      on prend la (les) table(s)
   FROM     …      (1)               2. WHERE     on filtre les LIGNES
   WHERE    …      (2)               3. GROUP BY  on forme les groupes
   GROUP BY …      (3)               4. HAVING    on filtre les GROUPES
   HAVING   …      (4)               5. SELECT    on calcule les colonnes (et les alias)
   ORDER BY …      (6)               6. ORDER BY  on trie
   LIMIT    …      (7)               7. LIMIT     on coupe
```

Conséquences pratiques :
- ❌ On ne peut **pas** utiliser un agrégat dans `WHERE` (les groupes n'existent pas encore) → `HAVING`.
- ❌ On ne peut **pas** utiliser un alias du `SELECT` dans `WHERE` (il n'est pas encore calculé).
- ✅ On **peut** utiliser un alias dans `ORDER BY` (calculé avant).

```sql
-- ❌ Unknown column 'age_approx' in 'where clause'
SELECT code_patient, 2026 - annee_naissance AS age_approx
FROM patient
WHERE age_approx > 80;

-- ✅ on répète l'expression
SELECT code_patient, 2026 - annee_naissance AS age_approx
FROM patient
WHERE 2026 - annee_naissance > 80;
```

---

## 3.8 Les sous-requêtes

### Concept

Une **sous-requête** est un `SELECT` écrit **entre parenthèses à l'intérieur** d'une autre requête. Elle permet d'utiliser le résultat d'une question pour en poser une autre (et de combiner plusieurs tables sans jointure).

```
                 ┌───────────── requête principale ─────────────┐
   SELECT …  FROM …  WHERE colonne  >  ( SELECT AVG(…) FROM … )
                                        └── sous-requête ──────┘
                                        exécutée d'abord, son résultat
                                        est injecté dans la requête principale
```

| Type | Renvoie | Utilisée avec | Exemple |
|---|---|---|---|
| **Scalaire** | 1 valeur | `=`, `>`, `<`… ou dans le `SELECT` | `> (SELECT AVG(…) …)` |
| **Liste** | 1 colonne, n lignes | `IN`, `NOT IN` | `etude_id IN (SELECT id …)` |
| **Existence** | vrai / faux | `EXISTS`, `NOT EXISTS` | `EXISTS (SELECT 1 …)` |
| **Table** | n colonnes, n lignes | dans le `FROM` (avec un alias) | `FROM (SELECT …) AS t` |

### Exemples

**Scalaire** — les patients nés avant l'année de naissance moyenne :

```sql
SELECT code_patient, annee_naissance
FROM patient
WHERE annee_naissance < (SELECT AVG(annee_naissance) FROM patient)
ORDER BY annee_naissance
LIMIT 3;
```
<!-- resultat -->
```text
+-------------------+-----------------+
| code_patient      | annee_naissance |
+-------------------+-----------------+
| CARDIO-01-C01-037 | 1945            |
| CARDIO-01-C02-011 | 1945            |
| CARDIO-01-C03-006 | 1945            |
+-------------------+-----------------+
3 lignes
```
<!-- /resultat -->

**Liste avec `IN`** — les patients des études du promoteur « Laboratoires Alvéa » :

```sql
SELECT etude_id, COUNT(*) AS nb_patients
FROM patient
WHERE etude_id IN (SELECT id FROM etude WHERE promoteur = 'Laboratoires Alvéa')
GROUP BY etude_id;
```
<!-- resultat -->
```text
+----------+-------------+
| etude_id | nb_patients |
+----------+-------------+
| 1        | 136         |
| 3        | 30          |
+----------+-------------+
2 lignes
```
<!-- /resultat -->

**`NOT IN`** — les centres qui n'ont recruté aucun patient :

```sql
SELECT id, nom, ville
FROM centre
WHERE id NOT IN (SELECT centre_id FROM patient);
```
<!-- resultat -->
```text
+----+-----------------------------+-------+
| id | nom                         | ville |
+----+-----------------------------+-------+
| 8  | Centre Médical des Ardennes | Liège |
+----+-----------------------------+-------+
1 ligne
```
<!-- /resultat -->

**`EXISTS`** — les patients ayant eu au moins un EI grave. La sous-requête fait référence à la ligne courante de la requête principale (`p.id`) : on dit qu'elle est **corrélée**.

```sql
SELECT p.code_patient, p.bras
FROM patient p
WHERE EXISTS (
    SELECT 1
    FROM evenement_indesirable ei
    WHERE ei.patient_id = p.id
      AND ei.grave = TRUE
);
```
<!-- resultat:5 -->
```text
+-------------------+------------+
| code_patient      | bras       |
+-------------------+------------+
| CARDIO-01-C01-016 | traitement |
| CARDIO-01-C01-023 | traitement |
| CARDIO-01-C02-002 | placebo    |
| CARDIO-01-C02-008 | placebo    |
| CARDIO-01-C02-017 | traitement |
+-------------------+------------+
… 25 lignes au total (5 affichées)
```
<!-- /resultat -->

> `p` et `ei` sont des **alias de table** (détaillés au module 4) : ils permettent de dire de quelle table vient chaque colonne.

**`NOT EXISTS`** — les patients inclus sans aucun événement indésirable :

```sql
SELECT COUNT(*) AS inclus_sans_ei
FROM patient p
WHERE p.date_inclusion IS NOT NULL
  AND NOT EXISTS (SELECT 1 FROM evenement_indesirable ei WHERE ei.patient_id = p.id);
```
<!-- resultat -->
```text
+----------------+
| inclus_sans_ei |
+----------------+
| 69             |
+----------------+
1 ligne
```
<!-- /resultat -->

**Sous-requête dans le `SELECT`** — le nombre d'EI de chaque patient :

```sql
SELECT p.code_patient,
       (SELECT COUNT(*) FROM evenement_indesirable ei WHERE ei.patient_id = p.id) AS nb_ei
FROM patient p
WHERE p.date_inclusion IS NOT NULL
ORDER BY nb_ei DESC, p.code_patient
LIMIT 5;
```
<!-- resultat -->
```text
+-------------------+-------+
| code_patient      | nb_ei |
+-------------------+-------+
| CARDIO-01-C01-028 | 3     |
| CARDIO-01-C02-015 | 3     |
| CARDIO-01-C02-019 | 3     |
| CARDIO-01-C03-003 | 3     |
| CARDIO-01-C03-011 | 3     |
+-------------------+-------+
5 lignes
```
<!-- /resultat -->

**Sous-requête dans le `FROM`** — d'abord compter les inclus **par centre et par étude**, puis faire la moyenne de ces comptes **par étude** (une moyenne de comptes nécessite deux niveaux) :

```sql
SELECT etude_id, ROUND(AVG(nb_inclus), 1) AS moyenne_inclus_par_centre
FROM (
    SELECT etude_id, centre_id, COUNT(date_inclusion) AS nb_inclus
    FROM patient
    GROUP BY etude_id, centre_id
) AS par_centre
GROUP BY etude_id;
```
<!-- resultat -->
```text
+----------+---------------------------+
| etude_id | moyenne_inclus_par_centre |
+----------+---------------------------+
| 1        | 22.4                      |
| 2        | 12.3                      |
| 3        | 7.0                       |
| 4        | 15.0                      |
+----------+---------------------------+
4 lignes
```
<!-- /resultat -->

**Comparer chaque centre à l'objectif** — inclus vs objectif, sans jointure :

```sql
SELECT ec.etude_id, ec.centre_id, ec.objectif_inclusions,
       (SELECT COUNT(date_inclusion)
          FROM patient p
         WHERE p.etude_id = ec.etude_id AND p.centre_id = ec.centre_id) AS inclus
FROM etude_centre ec
ORDER BY ec.etude_id, ec.centre_id;
```
<!-- resultat:20 -->
```text
+----------+-----------+---------------------+--------+
| etude_id | centre_id | objectif_inclusions | inclus |
+----------+-----------+---------------------+--------+
| 1        | 1         | 30                  | 33     |
| 1        | 2         | 25                  | 21     |
| 1        | 3         | 25                  | 26     |
| 1        | 4         | 20                  | 14     |
| 1        | 6         | 20                  | 18     |
| 2        | 1         | 20                  | 15     |
| 2        | 3         | 20                  | 9      |
| 2        | 5         | 25                  | 19     |
| 2        | 7         | 15                  | 6      |
| 3        | 2         | 20                  | 10     |
| 3        | 4         | 20                  | 7      |
| 3        | 6         | 20                  | 4      |
| 4        | 1         | 15                  | 15     |
| 4        | 2         | 15                  | 15     |
| 5        | 1         | 50                  | 0      |
| 5        | 8         | 50                  | 0      |
+----------+-----------+---------------------+--------+
16 lignes
```
<!-- /resultat -->

---

## À vous

👉 Exercices : [`exercices/03-requetes-simples.md`](../exercices/03-requetes-simples.md)

---

## Pièges

- **`= NULL`** au lieu de **`IS NULL`** : aucune erreur, aucun résultat.
- **`NOT IN` avec un NULL dans la liste** : si la sous-requête renvoie un seul NULL, `NOT IN` ne renvoie **plus rien**. Ajoutez `WHERE colonne IS NOT NULL` dans la sous-requête, ou préférez `NOT EXISTS`.
- **`AND` / `OR` sans parenthèses**.
- **`COUNT(colonne)` au lieu de `COUNT(*)`** (ou l'inverse) : le premier ignore les NULL. C'est parfois exactement ce qu'on veut (`COUNT(date_inclusion)` = nombre d'inclus), parfois un bug.
- **`AVG` ignore les NULL** : la moyenne porte sur les seules valeurs renseignées.
- **Agrégat dans `WHERE`** → utiliser `HAVING`.
- **Alias dans `WHERE`** → répéter l'expression (ou passer par une sous-requête).
- **`BETWEEN` avec des dates-heures** : `BETWEEN '2026-01-01' AND '2026-01-31'` exclut le 31 janvier après minuit pour une colonne `DATETIME`. Préférez `>= '2026-01-01' AND < '2026-02-01'`.
- **`LENGTH` vs `CHAR_LENGTH`** en MySQL : `LENGTH('é')` = 2 (octets), `CHAR_LENGTH('é')` = 1 (caractères).
- **Casse et accents** : avec la collation de notre base, MySQL considère `'tours' = 'Tours'` et `'evenement' = 'événement'` comme vrais. D'autres SGBD (ou d'autres collations) non : ne comptez pas dessus.

> ### ⚖️ Standard vs MySQL
> | Besoin | SQL standard | MySQL |
> |---|---|---|
> | Limiter le nombre de lignes | `FETCH FIRST 5 ROWS ONLY` (`OFFSET 5 ROWS` avant) | `LIMIT 5` (`OFFSET 5`) — MySQL ne connaît pas `FETCH FIRST` |
> | Concaténer | `prenom \|\| ' ' \|\| nom` | `CONCAT(prenom, ' ', nom)` — en MySQL, `\|\|` est un **OU logique** ! |
> | Extraire l'année | `EXTRACT(YEAR FROM d)` | `YEAR(d)` (et `EXTRACT` fonctionne aussi) |
> | Sous-chaîne | `SUBSTRING(t FROM 1 FOR 6)` | `SUBSTRING(t, 1, 6)` (les deux marchent) |
> | Écart entre dates | pas de fonction unique (`d1 - d2` selon les SGBD) | `DATEDIFF`, `TIMESTAMPDIFF` |
> | Date du jour | `CURRENT_DATE` | `CURRENT_DATE` ou `CURDATE()` |
> | Alias de colonne avec espace | `AS "Nb patients"` | `` AS `Nb patients` `` (ou `"…"` selon le mode) |
> | Colonnes hors GROUP BY | interdit | interdit par défaut depuis MySQL 5.7 (`ONLY_FULL_GROUP_BY`) |

---

## Quiz

1. Que renvoie `SELECT COUNT(date_inclusion) FROM patient` ?
   - a) Le nombre total de patients
   - b) Le nombre de patients dont la date d'inclusion est renseignée
   - c) Le nombre de dates d'inclusion différentes
   - d) Une erreur

2. Quelle clause permet de filtrer sur le résultat d'un `COUNT(*)` ?
   - a) `WHERE`  - b) `HAVING`  - c) `ORDER BY`  - d) `GROUP BY`

3. `WHERE grade BETWEEN 2 AND 4` équivaut à :
   - a) `grade > 2 AND grade < 4`
   - b) `grade >= 2 AND grade <= 4`
   - c) `grade IN (2, 4)`
   - d) `grade >= 2 OR grade <= 4`

4. Quelle condition sélectionne les codes se terminant par `001` ?
   - a) `code_patient LIKE '001%'`
   - b) `code_patient = '%001'`
   - c) `code_patient LIKE '%001'`
   - d) `code_patient LIKE '_001'`

5. Dans quel ordre logique ces clauses sont-elles exécutées ?
   - a) SELECT, FROM, WHERE, GROUP BY
   - b) FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY
   - c) FROM, SELECT, WHERE, ORDER BY
   - d) WHERE, FROM, GROUP BY, SELECT

6. *(bonus)* Que renvoie `SELECT * FROM patient WHERE bras <> 'placebo'` ?
   - a) Tous les patients sauf ceux du bras placebo
   - b) Les patients du bras traitement uniquement
   - c) Une erreur à cause des NULL
   - d) Les patients non inclus

<details>
<summary>Réponses</summary>

1. **b**. 2. **b**. 3. **b** — bornes incluses. 4. **c**. 5. **b**. 6. **b** — les patients dont `bras` est NULL ne vérifient pas la condition (NULL <> 'placebo' vaut NULL, donc écarté).
</details>

---

## Côté métier

Avec ce seul module, vous savez déjà produire la plupart des indicateurs d'un tableau de bord **sur une table** :

| Indicateur | Ingrédients |
|---|---|
| Nombre d'inclus par étude / par centre | `COUNT(date_inclusion)` + `GROUP BY` |
| Taux d'échec de screening | `SUM(CASE …) / COUNT(*)` |
| Rythme d'inclusion mensuel | `DATE_FORMAT(…, '%Y-%m')` + `GROUP BY` |
| Délai moyen screening → inclusion | `AVG(DATEDIFF(…))` |
| Répartition par classe d'âge | `CASE` + `GROUP BY` |
| « Top 10 » | `ORDER BY … DESC LIMIT 10` |

Et pour un indicateur qui mélange plusieurs tables, les sous-requêtes vous dépannent… en attendant les jointures du module suivant.

---

⬅️ [Module 2](02-modelisation.md) · ➡️ [Module 4 — Requêtes multi-tables](04-jointures.md)
