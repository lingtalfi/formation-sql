# Corrigés — Module 4 : Requêtes multi-tables

**Ex 4.1**

```sql
SELECT i.nom, i.prenom, c.nom AS centre, c.ville
FROM investigateur i
JOIN centre c ON i.centre_id = c.id
ORDER BY c.id, i.nom;
```
<!-- resultat:6 -->
```text
+---------+---------+--------------------------+--------+
| nom     | prenom  | centre                   | ville  |
+---------+---------+--------------------------+--------+
| Bernard | Hugo    | Clinique du Val de Loire | Tours  |
| Martin  | Claire  | Clinique du Val de Loire | Tours  |
| Petit   | Inès    | Clinique du Val de Loire | Tours  |
| Robert  | Lucas   | Clinique du Val de Loire | Tours  |
| Durand  | Sophie  | CHU Atlantique           | Nantes |
| Lefèvre | Camille | CHU Atlantique           | Nantes |
+---------+---------+--------------------------+--------+
… 18 lignes au total (6 affichées)
```
<!-- /resultat -->

**Ex 4.2**

```sql
SELECT p.code_patient, p.bras, p.date_inclusion
FROM patient p
JOIN etude e ON p.etude_id = e.id
WHERE e.code = 'ONCO-03'
  AND p.date_inclusion IS NOT NULL
ORDER BY p.date_inclusion;
```
<!-- resultat:5 -->
```text
+-----------------+------------+----------------+
| code_patient    | bras       | date_inclusion |
+-----------------+------------+----------------+
| ONCO-03-C02-001 | placebo    | 2025-07-28     |
| ONCO-03-C02-002 | placebo    | 2025-08-06     |
| ONCO-03-C02-004 | placebo    | 2025-09-03     |
| ONCO-03-C02-005 | placebo    | 2025-10-13     |
| ONCO-03-C02-006 | traitement | 2025-10-21     |
+-----------------+------------+----------------+
… 21 lignes au total (5 affichées)
```
<!-- /resultat -->

**Ex 4.3**

```sql
SELECT c.pays, COUNT(*) AS inclus
FROM patient p
JOIN centre c ON p.centre_id = c.id
WHERE p.date_inclusion IS NOT NULL
GROUP BY c.pays
ORDER BY inclus DESC;
```
<!-- resultat -->
```text
+---------+--------+
| pays    | inclus |
+---------+--------+
| France  | 184    |
| Suisse  | 22     |
| Espagne | 6      |
+---------+--------+
3 lignes
```
<!-- /resultat -->

**Ex 4.4**

```sql
SELECT e.promoteur, COUNT(*) AS nb_ei_graves
FROM evenement_indesirable ei
JOIN patient p ON ei.patient_id = p.id
JOIN etude   e ON p.etude_id    = e.id
WHERE ei.grave = TRUE
GROUP BY e.promoteur
ORDER BY nb_ei_graves DESC;
```
<!-- resultat -->
```text
+--------------------+--------------+
| promoteur          | nb_ei_graves |
+--------------------+--------------+
| Laboratoires Alvéa | 15           |
| Biomédix           | 6            |
| NeuroPharm         | 5            |
+--------------------+--------------+
3 lignes
```
<!-- /resultat -->

**Ex 4.5**

```sql
SELECT p.bras, v.type_visite, ROUND(AVG(m.valeur), 2) AS glycemie_moyenne
FROM mesure m
JOIN visite  v ON m.visite_id  = v.id
JOIN patient p ON v.patient_id = p.id
JOIN etude   e ON p.etude_id   = e.id
WHERE e.code = 'DIAB-02' AND m.parametre = 'glycemie'
GROUP BY p.bras, v.type_visite
ORDER BY p.bras, v.type_visite;
```
<!-- resultat:20 -->
```text
+------------+-------------+------------------+
| bras       | type_visite | glycemie_moyenne |
+------------+-------------+------------------+
| placebo    | V0          | 1.7              |
| placebo    | V1          | 1.7              |
| placebo    | V2          | 1.65             |
| placebo    | V3          | 1.67             |
| placebo    | V4          | 1.69             |
| placebo    | V5          | 1.62             |
| placebo    | V6          | 1.53             |
| traitement | V0          | 1.63             |
| traitement | V1          | 1.65             |
| traitement | V2          | 1.58             |
| traitement | V3          | 1.55             |
| traitement | V4          | 1.44             |
| traitement | V5          | 1.34             |
| traitement | V6          | 1.17             |
+------------+-------------+------------------+
14 lignes
```
<!-- /resultat -->

**Ex 4.6**

```sql
SELECT c.nom AS centre, e.code AS etude, p.code_patient, v.type_visite, v.date_prevue
FROM visite v
JOIN patient p ON v.patient_id = p.id
JOIN etude   e ON p.etude_id   = e.id
JOIN centre  c ON p.centre_id  = c.id
WHERE v.date_prevue < '2026-06-30'
  AND v.date_realisee IS NULL
ORDER BY c.nom, v.date_prevue, v.id;
```
<!-- resultat:8 -->
```text
+-----------------------------+-----------+-------------------+-------------+-------------+
| centre                      | etude     | code_patient      | type_visite | date_prevue |
+-----------------------------+-----------+-------------------+-------------+-------------+
| Centre Hospitalier du Rhône | CARDIO-01 | CARDIO-01-C04-007 | V2          | 2024-12-31  |
| Centre Hospitalier du Rhône | CARDIO-01 | CARDIO-01-C04-012 | V2          | 2025-05-21  |
| Centre Hospitalier du Rhône | CARDIO-01 | CARDIO-01-C04-016 | V1          | 2025-09-24  |
| Centre Hospitalier du Rhône | CARDIO-01 | CARDIO-01-C04-014 | V3          | 2025-10-24  |
| Centre Hospitalier du Rhône | ONCO-03   | ONCO-03-C04-005   | V1          | 2026-01-17  |
| Centre Hospitalier du Rhône | ONCO-03   | ONCO-03-C04-005   | V3          | 2026-02-28  |
| Centre Hospitalier du Rhône | ONCO-03   | ONCO-03-C04-009   | V2          | 2026-06-03  |
| Centre Hospitalier du Rhône | ONCO-03   | ONCO-03-C04-010   | V2          | 2026-06-12  |
+-----------------------------+-----------+-------------------+-------------+-------------+
… 77 lignes au total (8 affichées)
```
<!-- /resultat -->

**Ex 4.7**

```sql
SELECT c.nom, COUNT(ec.etude_id) AS nb_etudes
FROM centre c
LEFT JOIN etude_centre ec ON ec.centre_id = c.id
GROUP BY c.id, c.nom
ORDER BY nb_etudes DESC, c.nom;
```
<!-- resultat -->
```text
+-----------------------------+-----------+
| nom                         | nb_etudes |
+-----------------------------+-----------+
| Clinique du Val de Loire    | 4         |
| CHU Atlantique              | 3         |
| Centre Hospitalier du Rhône | 2         |
| Clinique du Léman           | 2         |
| Hôpital Saint-Roch          | 2         |
| Centre Médical des Ardennes | 1         |
| Clinique des Flandres       | 1         |
| Hospital del Sol            | 1         |
+-----------------------------+-----------+
8 lignes
```
<!-- /resultat -->

**Ex 4.8**

```sql
SELECT p.code_patient
FROM patient p
LEFT JOIN visite v ON v.patient_id = p.id
LEFT JOIN mesure m ON m.visite_id  = v.id
WHERE p.date_inclusion IS NOT NULL
GROUP BY p.code_patient
HAVING COUNT(m.id) = 0;
```
<!-- resultat -->
```text
+--------------+
| code_patient |
+--------------+
+--------------+
0 ligne
```
<!-- /resultat -->

Aucun : tout patient inclus a au moins sa visite V0 (réalisée le jour de l'inclusion) avec ses mesures. Un résultat vide est un résultat ! Vérifions avec les patients **non** inclus, qui eux n'ont jamais de mesure :

```sql
SELECT COUNT(*) AS patients_sans_mesure
FROM patient p
WHERE NOT EXISTS (
    SELECT 1 FROM visite v JOIN mesure m ON m.visite_id = v.id WHERE v.patient_id = p.id
);
```
<!-- resultat -->
```text
+----------------------+
| patients_sans_mesure |
+----------------------+
| 50                   |
+----------------------+
1 ligne
```
<!-- /resultat -->

(50 = le nombre d'échecs de screening.)

**Ex 4.9**

```sql
SELECT e.code, COUNT(p.id) AS en_cours
FROM etude e
LEFT JOIN patient p
       ON p.etude_id = e.id
      AND p.date_inclusion IS NOT NULL
      AND p.date_sortie IS NULL
GROUP BY e.code
ORDER BY e.code;
```
<!-- resultat -->
```text
+-----------+----------+
| code      | en_cours |
+-----------+----------+
| CARDIO-01 | 33       |
| DERM-05   | 0        |
| DIAB-02   | 26       |
| NEURO-04  | 0        |
| ONCO-03   | 15       |
+-----------+----------+
5 lignes
```
<!-- /resultat -->

Les conditions sur `patient` sont dans le `ON` pour garder les études sans patient en cours (DERM-05, NEURO-04).

**Ex 4.10**

```sql
SELECT c.nom, COUNT(v.id) AS visites_2026
FROM centre c
LEFT JOIN patient p ON p.centre_id = c.id
LEFT JOIN visite  v ON v.patient_id = p.id
                   AND v.date_realisee >= '2026-01-01'
GROUP BY c.id, c.nom
ORDER BY visites_2026 DESC, c.nom;
```
<!-- resultat -->
```text
+-----------------------------+--------------+
| nom                         | visites_2026 |
+-----------------------------+--------------+
| Clinique du Val de Loire    | 49           |
| Clinique des Flandres       | 39           |
| CHU Atlantique              | 33           |
| Centre Hospitalier du Rhône | 32           |
| Hôpital Saint-Roch          | 29           |
| Clinique du Léman           | 27           |
| Hospital del Sol            | 22           |
| Centre Médical des Ardennes | 0            |
+-----------------------------+--------------+
8 lignes
```
<!-- /resultat -->

Avec le filtre dans le `WHERE`, les centres sans visite en 2026 (ici Liège) disparaîtraient du résultat.

**Ex 4.11**

```sql
SELECT CONCAT(i.prenom, ' ', i.nom) AS investigateur, i.specialite,
       CONCAT(s.prenom, ' ', s.nom) AS superviseur,  s.specialite AS specialite_superviseur
FROM investigateur i
JOIN investigateur s ON i.superviseur_id = s.id
WHERE i.specialite <> s.specialite
ORDER BY i.id;
```
<!-- resultat:20 -->
```text
+-----------------+------------------+-----------------+------------------------+
| investigateur   | specialite       | superviseur     | specialite_superviseur |
+-----------------+------------------+-----------------+------------------------+
| Hugo Bernard    | Diabétologie     | Claire Martin   | Cardiologie            |
| Inès Petit      | Neurologie       | Claire Martin   | Cardiologie            |
| Lucas Robert    | Dermatologie     | Claire Martin   | Cardiologie            |
| Thomas Moreau   | Cardiologie      | Sophie Durand   | Oncologie              |
| Camille Lefèvre | Neurologie       | Sophie Durand   | Oncologie              |
| Léa Roux        | Diabétologie     | Antoine Garcia  | Cardiologie            |
| Manon Girard    | Cardiologie      | Julien Fournier | Oncologie              |
| Paul Bonnet     | Médecine interne | Julien Fournier | Oncologie              |
| Anna Müller     | Cardiologie      | Nicolas Favre   | Oncologie              |
| Javier Sánchez  | Médecine interne | Carmen López    | Diabétologie           |
+-----------------+------------------+-----------------+------------------------+
10 lignes
```
<!-- /resultat -->

**Ex 4.12**

```sql
SELECT t.type_visite, b.bras, COUNT(v.id) AS realisees
FROM (SELECT DISTINCT type_visite FROM visite) t
CROSS JOIN (SELECT DISTINCT bras FROM patient WHERE bras IS NOT NULL) b
LEFT JOIN patient p ON p.bras = b.bras
                   AND p.etude_id = (SELECT id FROM etude WHERE code = 'CARDIO-01')
LEFT JOIN visite v  ON v.patient_id = p.id
                   AND v.type_visite = t.type_visite
                   AND v.date_realisee IS NOT NULL
GROUP BY t.type_visite, b.bras
ORDER BY t.type_visite, b.bras;
```
<!-- resultat:20 -->
```text
+-------------+------------+-----------+
| type_visite | bras       | realisees |
+-------------+------------+-----------+
| V0          | placebo    | 60        |
| V0          | traitement | 52        |
| V1          | placebo    | 53        |
| V1          | traitement | 50        |
| V2          | placebo    | 54        |
| V2          | traitement | 44        |
| V3          | placebo    | 49        |
| V3          | traitement | 48        |
| V4          | placebo    | 52        |
| V4          | traitement | 45        |
| V5          | placebo    | 49        |
| V5          | traitement | 44        |
| V6          | placebo    | 33        |
| V6          | traitement | 30        |
+-------------+------------+-----------+
14 lignes
```
<!-- /resultat -->

**Ex 4.13**

```sql
SELECT 'investigateur' AS role, nom, prenom
FROM investigateur
UNION ALL
SELECT 'patient', code_patient, ''
FROM patient
WHERE centre_id = 7 AND date_inclusion IS NOT NULL
ORDER BY role, nom;
```
<!-- resultat:30 -->
```text
+---------------+-----------------+---------+
| role          | nom             | prenom  |
+---------------+-----------------+---------+
| investigateur | Bernard         | Hugo    |
| investigateur | Bonnet          | Paul    |
| investigateur | Dubois          | Marc    |
| investigateur | Durand          | Sophie  |
| investigateur | Favre           | Nicolas |
| investigateur | Fournier        | Julien  |
| investigateur | Garcia          | Antoine |
| investigateur | Girard          | Manon   |
| investigateur | Lambert         | Emma    |
| investigateur | Lefèvre         | Camille |
| investigateur | López           | Carmen  |
| investigateur | Martin          | Claire  |
| investigateur | Moreau          | Thomas  |
| investigateur | Müller          | Anna    |
| investigateur | Petit           | Inès    |
| investigateur | Robert          | Lucas   |
| investigateur | Roux            | Léa     |
| investigateur | Sánchez         | Javier  |
| patient       | DIAB-02-C07-001 |         |
| patient       | DIAB-02-C07-004 |         |
| patient       | DIAB-02-C07-005 |         |
| patient       | DIAB-02-C07-006 |         |
| patient       | DIAB-02-C07-007 |         |
| patient       | DIAB-02-C07-008 |         |
+---------------+-----------------+---------+
24 lignes
```
<!-- /resultat -->

**Ex 4.14**

```sql
SELECT v.date_prevue AS date, CONCAT(v.type_visite, ' prévue') AS evenement
FROM visite v JOIN patient p ON v.patient_id = p.id
WHERE p.code_patient = 'ONCO-03-C04-008'
UNION ALL
SELECT v.date_realisee, CONCAT(v.type_visite, ' réalisée')
FROM visite v JOIN patient p ON v.patient_id = p.id
WHERE p.code_patient = 'ONCO-03-C04-008' AND v.date_realisee IS NOT NULL
UNION ALL
SELECT ei.date_survenue, CONCAT('EI : ', ei.terme, CASE WHEN ei.grave THEN ' (GRAVE)' ELSE '' END)
FROM evenement_indesirable ei JOIN patient p ON ei.patient_id = p.id
WHERE p.code_patient = 'ONCO-03-C04-008'
UNION ALL
SELECT date_sortie, CONCAT('Sortie : ', motif_sortie)
FROM patient
WHERE code_patient = 'ONCO-03-C04-008' AND date_sortie IS NOT NULL
ORDER BY date, evenement;
```
<!-- resultat:20 -->
```text
+------------+--------------------------------+
| date       | evenement                      |
+------------+--------------------------------+
| 2026-03-15 | V0 prévue                      |
| 2026-03-15 | V0 réalisée                    |
| 2026-03-29 | V1 prévue                      |
| 2026-04-05 | V1 réalisée                    |
| 2026-04-12 | V2 prévue                      |
| 2026-04-12 | V2 réalisée                    |
| 2026-04-15 | EI : Insomnie                  |
| 2026-05-10 | V3 prévue                      |
| 2026-05-12 | V3 réalisée                    |
| 2026-06-11 | EI : Anémie (GRAVE)            |
| 2026-06-12 | Sortie : événement indésirable |
+------------+--------------------------------+
11 lignes
```
<!-- /resultat -->

**Ex 4.15**

<!-- exec -->
```sql
CREATE TEMPORARY TABLE tmp_eig AS
SELECT ei.id, ei.terme, ei.grade, ei.date_survenue, p.code_patient, e.code AS etude, c.ville
FROM evenement_indesirable ei
JOIN patient p ON ei.patient_id = p.id
JOIN etude   e ON p.etude_id    = e.id
JOIN centre  c ON p.centre_id   = c.id
WHERE ei.grave = TRUE;
```

```sql
SELECT ville, COUNT(*) AS nb_eig
FROM tmp_eig
GROUP BY ville
ORDER BY nb_eig DESC, ville;
```
<!-- resultat -->
```text
+-------------+--------+
| ville       | nb_eig |
+-------------+--------+
| Nantes      | 8      |
| Tours       | 7      |
| Montpellier | 4      |
| Lille       | 3      |
| Genève      | 2      |
| Lyon        | 2      |
+-------------+--------+
6 lignes
```
<!-- /resultat -->

**Ex 4.16**

```sql
WITH pas_visite AS (
    SELECT p.id AS patient_id, p.bras, v.type_visite, m.valeur
    FROM mesure m
    JOIN visite  v ON m.visite_id  = v.id
    JOIN patient p ON v.patient_id = p.id
    JOIN etude   e ON p.etude_id   = e.id
    WHERE e.code = 'CARDIO-01' AND m.parametre = 'pas'
      AND v.type_visite IN ('V0', 'V6')
), variation AS (
    SELECT v0.patient_id, v0.bras, v6.valeur - v0.valeur AS delta_pas
    FROM pas_visite v0
    JOIN pas_visite v6 ON v6.patient_id = v0.patient_id AND v6.type_visite = 'V6'
    WHERE v0.type_visite = 'V0'
)
SELECT bras, COUNT(*) AS nb_patients, ROUND(AVG(delta_pas), 1) AS variation_moyenne_pas
FROM variation
GROUP BY bras;
```
<!-- resultat -->
```text
+------------+-------------+-----------------------+
| bras       | nb_patients | variation_moyenne_pas |
+------------+-------------+-----------------------+
| placebo    | 33          | -3.6                  |
| traitement | 30          | -12.8                 |
+------------+-------------+-----------------------+
2 lignes
```
<!-- /resultat -->

Lecture : la tension a baissé en moyenne beaucoup plus dans le bras traitement que dans le bras placebo. C'est le **critère principal** typique d'une étude d'efficacité.

**Ex 4.17**

```sql
WITH inclus AS (
    SELECT centre_id, COUNT(date_inclusion) AS nb
    FROM patient
    WHERE etude_id = (SELECT id FROM etude WHERE code = 'DIAB-02')
    GROUP BY centre_id
), ei AS (
    SELECT p.centre_id, COUNT(*) AS nb
    FROM evenement_indesirable x
    JOIN patient p ON x.patient_id = p.id
    WHERE p.etude_id = (SELECT id FROM etude WHERE code = 'DIAB-02')
    GROUP BY p.centre_id
), manquees AS (
    SELECT p.centre_id, COUNT(*) AS nb
    FROM visite v
    JOIN patient p ON v.patient_id = p.id
    WHERE p.etude_id = (SELECT id FROM etude WHERE code = 'DIAB-02')
      AND v.date_prevue < '2026-06-30' AND v.date_realisee IS NULL
    GROUP BY p.centre_id
)
SELECT c.nom AS centre,
       CONCAT(i.prenom, ' ', i.nom)                         AS investigateur_principal,
       ec.objectif_inclusions                               AS objectif,
       COALESCE(inc.nb, 0)                                  AS inclus,
       ROUND(100 * COALESCE(inc.nb, 0) / ec.objectif_inclusions) AS atteinte_pct,
       COALESCE(ei.nb, 0)                                   AS nb_ei,
       COALESCE(mq.nb, 0)                                   AS visites_manquees
FROM etude_centre ec
JOIN centre c        ON ec.centre_id = c.id
JOIN investigateur i ON ec.investigateur_principal_id = i.id
LEFT JOIN inclus   inc ON inc.centre_id = ec.centre_id
LEFT JOIN ei           ON ei.centre_id  = ec.centre_id
LEFT JOIN manquees mq  ON mq.centre_id  = ec.centre_id
WHERE ec.etude_id = (SELECT id FROM etude WHERE code = 'DIAB-02')
ORDER BY atteinte_pct DESC;
```
<!-- resultat -->
```text
+--------------------------+-------------------------+----------+--------+--------------+-------+------------------+
| centre                   | investigateur_principal | objectif | inclus | atteinte_pct | nb_ei | visites_manquees |
+--------------------------+-------------------------+----------+--------+--------------+-------+------------------+
| Clinique des Flandres    | Emma Lambert            | 25       | 19     | 76           | 18    | 8                |
| Clinique du Val de Loire | Hugo Bernard            | 20       | 15     | 75           | 14    | 2                |
| Hôpital Saint-Roch       | Léa Roux                | 20       | 9      | 45           | 11    | 1                |
| Hospital del Sol         | Carmen López            | 15       | 6      | 40           | 4     | 2                |
+--------------------------+-------------------------+----------+--------+--------------+-------+------------------+
4 lignes
```
<!-- /resultat -->

Chaque indicateur est calculé **séparément** dans sa CTE, puis assemblé : c'est la méthode qui évite le piège de la multiplication des lignes (module 4, *Pièges*).
