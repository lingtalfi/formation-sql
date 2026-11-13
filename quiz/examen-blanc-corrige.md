# Examen blanc — Corrigé

## Partie A — Cas pratique

**A1.**

```sql
SELECT code, titre, phase, statut
FROM etude
WHERE promoteur = 'Laboratoires Alvéa'
ORDER BY date_debut;
```
<!-- resultat -->
```text
+-----------+-------------------------------------------------------------+-------+-------------+
| code      | titre                                                       | phase | statut      |
+-----------+-------------------------------------------------------------+-------+-------------+
| CARDIO-01 | Effet de la molécule KX-12 sur l'hypertension artérielle    | III   | suivi       |
| ONCO-03   | Tolérance de l'immunothérapie OX-3 dans le cancer du poumon | II    | recrutement |
+-----------+-------------------------------------------------------------+-------+-------------+
2 lignes
```
<!-- /resultat -->

**A2.**

```sql
SELECT e.code,
       (SELECT COUNT(*) FROM etude_centre ec WHERE ec.etude_id = e.id)          AS nb_centres,
       (SELECT COUNT(date_inclusion) FROM patient p WHERE p.etude_id = e.id)    AS nb_inclus
FROM etude e
WHERE e.promoteur = 'Laboratoires Alvéa'
ORDER BY e.code;
```
<!-- resultat -->
```text
+-----------+------------+-----------+
| code      | nb_centres | nb_inclus |
+-----------+------------+-----------+
| CARDIO-01 | 5          | 112       |
| ONCO-03   | 3          | 21        |
+-----------+------------+-----------+
2 lignes
```
<!-- /resultat -->

Avec deux jointures dans la même requête, attention à la multiplication des lignes : il faudrait `COUNT(DISTINCT ec.centre_id)` et un comptage distinct des patients inclus. Les sous-requêtes évitent le problème.

**A3.**

```sql
SELECT p.code_patient, e.code AS etude, c.ville, p.date_sortie, p.motif_sortie
FROM patient p
JOIN etude  e ON p.etude_id  = e.id
JOIN centre c ON p.centre_id = c.id
WHERE e.promoteur = 'Laboratoires Alvéa'
  AND p.date_sortie IS NOT NULL
  AND p.motif_sortie <> 'fin d''étude'
ORDER BY p.date_sortie, p.code_patient;
```
<!-- resultat:30 -->
```text
+-------------------+-----------+-------------+-------------+-------------------------+
| code_patient      | etude     | ville       | date_sortie | motif_sortie            |
+-------------------+-----------+-------------+-------------+-------------------------+
| CARDIO-01-C03-003 | CARDIO-01 | Montpellier | 2024-07-27  | événement indésirable   |
| CARDIO-01-C03-004 | CARDIO-01 | Montpellier | 2024-08-07  | retrait du consentement |
| CARDIO-01-C02-002 | CARDIO-01 | Nantes      | 2024-10-29  | perdu de vue            |
| CARDIO-01-C03-018 | CARDIO-01 | Montpellier | 2025-03-10  | retrait du consentement |
| CARDIO-01-C02-009 | CARDIO-01 | Nantes      | 2025-03-25  | retrait du consentement |
| CARDIO-01-C03-017 | CARDIO-01 | Montpellier | 2025-04-02  | retrait du consentement |
| CARDIO-01-C01-018 | CARDIO-01 | Tours       | 2025-06-02  | perdu de vue            |
| CARDIO-01-C01-010 | CARDIO-01 | Tours       | 2025-06-13  | retrait du consentement |
| CARDIO-01-C01-016 | CARDIO-01 | Tours       | 2025-07-06  | perdu de vue            |
| CARDIO-01-C06-011 | CARDIO-01 | Genève      | 2025-07-11  | retrait du consentement |
| CARDIO-01-C01-014 | CARDIO-01 | Tours       | 2025-08-21  | retrait du consentement |
| ONCO-03-C02-002   | ONCO-03   | Nantes      | 2025-09-11  | événement indésirable   |
| CARDIO-01-C01-037 | CARDIO-01 | Tours       | 2025-09-15  | perdu de vue            |
| CARDIO-01-C01-028 | CARDIO-01 | Tours       | 2025-09-24  | retrait du consentement |
| CARDIO-01-C01-033 | CARDIO-01 | Tours       | 2025-11-01  | retrait du consentement |
| CARDIO-01-C03-023 | CARDIO-01 | Montpellier | 2025-11-13  | retrait du consentement |
| CARDIO-01-C03-027 | CARDIO-01 | Montpellier | 2025-11-14  | retrait du consentement |
| ONCO-03-C06-001   | ONCO-03   | Genève      | 2025-11-26  | événement indésirable   |
| ONCO-03-C02-006   | ONCO-03   | Nantes      | 2025-12-24  | perdu de vue            |
| ONCO-03-C04-004   | ONCO-03   | Lyon        | 2026-02-16  | retrait du consentement |
| ONCO-03-C04-008   | ONCO-03   | Lyon        | 2026-06-12  | événement indésirable   |
+-------------------+-----------+-------------+-------------+-------------------------+
21 lignes
```
<!-- /resultat -->

**A4.**

```sql
SELECT e.code AS etude, b.bras, COUNT(ei.id) AS nb_ei_graves
FROM etude e
CROSS JOIN (SELECT 'traitement' AS bras UNION SELECT 'placebo') b
LEFT JOIN patient p                ON p.etude_id = e.id AND p.bras = b.bras
LEFT JOIN evenement_indesirable ei ON ei.patient_id = p.id AND ei.grave = TRUE
WHERE e.promoteur = 'Laboratoires Alvéa'
GROUP BY e.code, b.bras
ORDER BY e.code, b.bras;
```
<!-- resultat -->
```text
+-----------+------------+--------------+
| etude     | bras       | nb_ei_graves |
+-----------+------------+--------------+
| CARDIO-01 | placebo    | 5            |
| CARDIO-01 | traitement | 6            |
| ONCO-03   | placebo    | 4            |
| ONCO-03   | traitement | 0            |
+-----------+------------+--------------+
4 lignes
```
<!-- /resultat -->

Le `CROSS JOIN` avec la liste des bras garantit que chaque combinaison étude × bras apparaît, même à 0 ; les filtres sur les tables de droite sont dans les `ON`.

**A5.**

```sql
SELECT e.code AS etude, c.nom AS centre, ec.objectif_inclusions,
       COUNT(p.date_inclusion) AS inclus,
       ROUND(100 * COUNT(p.date_inclusion) / ec.objectif_inclusions, 1) AS atteinte_pct
FROM etude_centre ec
JOIN etude  e ON ec.etude_id  = e.id
JOIN centre c ON ec.centre_id = c.id
LEFT JOIN patient p ON p.etude_id = ec.etude_id AND p.centre_id = ec.centre_id
WHERE e.promoteur = 'Laboratoires Alvéa'
GROUP BY e.code, c.nom, ec.objectif_inclusions
ORDER BY atteinte_pct DESC
LIMIT 1;
```
<!-- resultat -->
```text
+-----------+--------------------------+---------------------+--------+--------------+
| etude     | centre                   | objectif_inclusions | inclus | atteinte_pct |
+-----------+--------------------------+---------------------+--------+--------------+
| CARDIO-01 | Clinique du Val de Loire | 30                  | 33     | 110.0        |
+-----------+--------------------------+---------------------+--------+--------------+
1 ligne
```
<!-- /resultat -->

**A6.**

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_alvea_visites_manquees AS
SELECT e.code AS etude, c.nom AS centre, p.code_patient, v.type_visite, v.date_prevue,
       DATEDIFF('2026-06-30', v.date_prevue) AS jours_retard
FROM visite v
JOIN patient p ON v.patient_id = p.id
JOIN etude   e ON p.etude_id   = e.id
JOIN centre  c ON p.centre_id  = c.id
WHERE e.promoteur = 'Laboratoires Alvéa'
  AND v.date_prevue < '2026-06-30'
  AND v.date_realisee IS NULL;
```

```sql
SELECT * FROM v_alvea_visites_manquees ORDER BY jours_retard DESC, code_patient LIMIT 5;
```
<!-- resultat -->
```text
+-----------+--------------------------+-------------------+-------------+-------------+--------------+
| etude     | centre                   | code_patient      | type_visite | date_prevue | jours_retard |
+-----------+--------------------------+-------------------+-------------+-------------+--------------+
| CARDIO-01 | CHU Atlantique           | CARDIO-01-C02-002 | V1          | 2024-05-20  | 771          |
| CARDIO-01 | Clinique du Val de Loire | CARDIO-01-C01-003 | V2          | 2024-06-15  | 745          |
| CARDIO-01 | Clinique du Val de Loire | CARDIO-01-C01-004 | V1          | 2024-07-08  | 722          |
| CARDIO-01 | Hôpital Saint-Roch       | CARDIO-01-C03-004 | V2          | 2024-08-07  | 692          |
| CARDIO-01 | Clinique du Val de Loire | CARDIO-01-C01-007 | V2          | 2024-08-27  | 672          |
+-----------+--------------------------+-------------------+-------------+-------------+--------------+
5 lignes
```
<!-- /resultat -->

**A7.**

```sql
SELECT centre, COUNT(*) AS nb_manquees
FROM v_alvea_visites_manquees
GROUP BY centre
HAVING COUNT(*) >= 5
ORDER BY nb_manquees DESC, centre;
```
<!-- resultat -->
```text
+-----------------------------+-------------+
| centre                      | nb_manquees |
+-----------------------------+-------------+
| CHU Atlantique              | 18          |
| Clinique du Val de Loire    | 14          |
| Centre Hospitalier du Rhône | 9           |
| Clinique du Léman           | 8           |
| Hôpital Saint-Roch          | 8           |
+-----------------------------+-------------+
5 lignes
```
<!-- /resultat -->

**A8.**

<!-- exec -->
```sql
START TRANSACTION;
```

```sql
UPDATE etude SET objectif_inclusions = 75 WHERE code = 'ONCO-03';
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

```sql
SELECT code, objectif_inclusions FROM etude WHERE code = 'ONCO-03';
```
<!-- resultat -->
```text
+---------+---------------------+
| code    | objectif_inclusions |
+---------+---------------------+
| ONCO-03 | 75                  |
+---------+---------------------+
1 ligne
```
<!-- /resultat -->

<!-- exec -->
```sql
COMMIT;
```

---

## Partie B — Réponses

| Q | Réponse | Explication |
|---|---|---|
| B1 | c | `ALTER TABLE` modifie une structure (LDD). `SELECT` = interrogation, `UPDATE` = manipulation, `COMMIT` = transactions. |
| B2 | b, c | Jamais NULL ; une seule clé primaire par table (éventuellement composée). |
| B3 | c | Association plusieurs-à-plusieurs → table d'association. |
| B4 | b | `DECIMAL` est exact ; `FLOAT` introduit des arrondis. |
| B5 | a, c | `UNIQUE` et `FOREIGN KEY` acceptent NULL. |
| B6 | b | `COUNT(colonne)` ignore les NULL. |
| B7 | b | `AVG` ignore les NULL : 70 / 7 = 10. |
| B8 | c | `= NULL` vaut toujours NULL (inconnu) : aucune ligne, sans erreur. |
| B9 | a, b, d | Les bornes de `BETWEEN` sont incluses ; (c) les exclut. |
| B10 | b | `_` = exactement un caractère, `%` = n'importe quelle suite. |
| B11 | b | |
| B12 | b | Toute colonne non agrégée doit figurer dans le `GROUP BY`. |
| B13 | b | |
| B14 | c | `LIMIT` : MySQL / PostgreSQL ; `TOP` : SQL Server ; `ROWNUM` : Oracle. |
| B15 | d | 4 × 6. |
| B16 | b | |
| B17 | a, b, c | (b) fonctionne ici car `patient.centre_id` n'est jamais NULL ; (d) ne renvoie rien. |
| B18 | c | |
| B19 | b | |
| B20 | b | `UNION` supprime les doublons (`UNION ALL` les garderait). |
| B21 | b | En MySQL, `SELECT … INTO` sert aux variables et aux fichiers. |
| B22 | b | |
| B23 | b | Aucune erreur : sans `WHERE`, toutes les lignes sont modifiées. |
| B24 | a, c | (b) : nombre de valeurs ≠ nombre de colonnes ; (d) : syntaxe propre à MySQL. |
| B25 | b | Intégrité référentielle. |
| B26 | b | Le `ROLLBACK` annule la suppression. |
| B27 | b, c, d | Une vue ne stocke que sa requête. |
| B28 | b | |
| B29 | b | Première valeur non NULL. |
| B30 | b | Une colonne, éventuellement plusieurs lignes. |

**Barème indicatif** : partie A sur 40 (5 points par question), partie B sur 60 (2 points par question, réponse entièrement juste exigée pour les QCM). Objectif : 70 / 100.
