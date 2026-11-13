# Corrigés — Module 3 : Requêtes simples

> D'autres écritures sont souvent possibles : l'important est d'obtenir le même résultat.

**Ex 3.1**

```sql
SELECT code, phase, promoteur
FROM etude
ORDER BY phase, code;
```
<!-- resultat -->
```text
+-----------+-------+--------------------+
| code      | phase | promoteur          |
+-----------+-------+--------------------+
| NEURO-04  | I     | NeuroPharm         |
| DIAB-02   | II    | Biomédix           |
| ONCO-03   | II    | Laboratoires Alvéa |
| CARDIO-01 | III   | Laboratoires Alvéa |
| DERM-05   | III   | Biomédix           |
+-----------+-------+--------------------+
5 lignes
```
<!-- /resultat -->

**Ex 3.2**

```sql
SELECT nom, prenom
FROM investigateur
WHERE specialite = 'Cardiologie';
```
<!-- resultat -->
```text
+--------+---------+
| nom    | prenom  |
+--------+---------+
| Martin | Claire  |
| Moreau | Thomas  |
| Garcia | Antoine |
| Girard | Manon   |
| Müller | Anna    |
+--------+---------+
5 lignes
```
<!-- /resultat -->

**Ex 3.3**

```sql
SELECT code_patient, annee_naissance
FROM patient
WHERE sexe = 'F' AND etude_id = 2
ORDER BY annee_naissance DESC;
```
<!-- resultat:5 -->
```text
+-----------------+-----------------+
| code_patient    | annee_naissance |
+-----------------+-----------------+
| DIAB-02-C07-006 | 1984            |
| DIAB-02-C05-018 | 1983            |
| DIAB-02-C01-006 | 1981            |
| DIAB-02-C03-003 | 1981            |
| DIAB-02-C01-014 | 1980            |
+-----------------+-----------------+
… 29 lignes au total (5 affichées)
```
<!-- /resultat -->

**Ex 3.4**

```sql
SELECT id, patient_id, date_realisee
FROM visite
WHERE type_visite = 'V6'
  AND date_realisee BETWEEN '2025-01-01' AND '2025-12-31';
```
<!-- resultat:5 -->
```text
+----+------------+---------------+
| id | patient_id | date_realisee |
+----+------------+---------------+
| 7  | 1          | 2025-04-01    |
| 14 | 2          | 2025-04-06    |
| 21 | 3          | 2025-04-22    |
| 28 | 4          | 2025-05-25    |
| 35 | 6          | 2025-06-28    |
+----+------------+---------------+
… 34 lignes au total (5 affichées)
```
<!-- /resultat -->

Variante : `AND YEAR(date_realisee) = 2025`.

**Ex 3.5**

```sql
SELECT code_patient, date_sortie, motif_sortie
FROM patient
WHERE date_sortie IS NOT NULL
  AND motif_sortie <> 'fin d''étude'
ORDER BY date_sortie, code_patient;
```
<!-- resultat:30 -->
```text
+-------------------+-------------+-------------------------+
| code_patient      | date_sortie | motif_sortie            |
+-------------------+-------------+-------------------------+
| NEURO-04-C01-007  | 2023-06-11  | événement indésirable   |
| CARDIO-01-C03-003 | 2024-07-27  | événement indésirable   |
| CARDIO-01-C03-004 | 2024-08-07  | retrait du consentement |
| CARDIO-01-C02-002 | 2024-10-29  | perdu de vue            |
| CARDIO-01-C03-018 | 2025-03-10  | retrait du consentement |
| CARDIO-01-C02-009 | 2025-03-25  | retrait du consentement |
| CARDIO-01-C03-017 | 2025-04-02  | retrait du consentement |
| CARDIO-01-C01-018 | 2025-06-02  | perdu de vue            |
| CARDIO-01-C01-010 | 2025-06-13  | retrait du consentement |
| CARDIO-01-C01-016 | 2025-07-06  | perdu de vue            |
| CARDIO-01-C06-011 | 2025-07-11  | retrait du consentement |
| DIAB-02-C01-006   | 2025-07-22  | retrait du consentement |
| DIAB-02-C01-004   | 2025-08-02  | retrait du consentement |
| CARDIO-01-C01-014 | 2025-08-21  | retrait du consentement |
| ONCO-03-C02-002   | 2025-09-11  | événement indésirable   |
| CARDIO-01-C01-037 | 2025-09-15  | perdu de vue            |
| CARDIO-01-C01-028 | 2025-09-24  | retrait du consentement |
| DIAB-02-C01-011   | 2025-10-19  | retrait du consentement |
| CARDIO-01-C01-033 | 2025-11-01  | retrait du consentement |
| CARDIO-01-C03-023 | 2025-11-13  | retrait du consentement |
| CARDIO-01-C03-027 | 2025-11-14  | retrait du consentement |
| ONCO-03-C06-001   | 2025-11-26  | événement indésirable   |
| ONCO-03-C02-006   | 2025-12-24  | perdu de vue            |
| ONCO-03-C04-004   | 2026-02-16  | retrait du consentement |
| DIAB-02-C05-022   | 2026-04-18  | retrait du consentement |
| ONCO-03-C04-008   | 2026-06-12  | événement indésirable   |
| DIAB-02-C03-010   | 2026-06-30  | retrait du consentement |
+-------------------+-------------+-------------------------+
27 lignes
```
<!-- /resultat -->

Notez l'apostrophe doublée dans `'fin d''étude'`. La condition `date_sortie IS NOT NULL` est ici redondante (un `motif_sortie` NULL est de toute façon écarté par `<>`), mais elle rend l'intention explicite.

**Ex 3.6**

```sql
SELECT id, patient_id, type_visite, date_prevue
FROM visite
WHERE date_prevue < '2026-06-30'
  AND date_realisee IS NULL
ORDER BY date_prevue, id
LIMIT 10;
```
<!-- resultat -->
```text
+------+------------+-------------+-------------+
| id   | patient_id | type_visite | date_prevue |
+------+------------+-------------+-------------+
| 1250 | 247        | V1          | 2023-03-05  |
| 1206 | 235        | V2          | 2023-04-13  |
| 1231 | 242        | V2          | 2023-06-21  |
| 1227 | 241        | V2          | 2023-06-22  |
| 1238 | 244        | V1          | 2023-06-27  |
| 1243 | 245        | V2          | 2023-07-17  |
| 1299 | 260        | V2          | 2023-07-22  |
| 219  | 42         | V1          | 2024-05-20  |
| 17   | 3          | V2          | 2024-06-15  |
| 23   | 4          | V1          | 2024-07-08  |
+------+------------+-------------+-------------+
10 lignes
```
<!-- /resultat -->

**Ex 3.7**

```sql
SELECT id, patient_id, terme, grade, lien_traitement, date_survenue
FROM evenement_indesirable
WHERE grade >= 2
  AND date_resolution IS NULL
  AND lien_traitement IN ('certain', 'probable', 'possible');
```
<!-- resultat -->
```text
+-----+------------+--------------------+-------+-----------------+---------------+
| id  | patient_id | terme              | grade | lien_traitement | date_survenue |
+-----+------------+--------------------+-------+-----------------+---------------+
| 99  | 117        | Insomnie           | 2     | probable        | 2025-03-02    |
| 129 | 164        | Fatigue            | 2     | possible        | 2026-06-29    |
| 142 | 178        | Douleur abdominale | 2     | probable        | 2025-08-11    |
| 174 | 224        | Douleur abdominale | 2     | possible        | 2026-06-25    |
| 175 | 224        | Vertiges           | 2     | possible        | 2026-06-23    |
+-----+------------+--------------------+-------+-----------------+---------------+
5 lignes
```
<!-- /resultat -->

**Ex 3.8**

```sql
SELECT CONCAT('Dr ', prenom, ' ', UPPER(nom)) AS nom_complet
FROM investigateur;
```
<!-- resultat:4 -->
```text
+------------------+
| nom_complet      |
+------------------+
| Dr Claire MARTIN |
| Dr Hugo BERNARD  |
| Dr Inès PETIT    |
| Dr Lucas ROBERT  |
+------------------+
… 18 lignes au total (4 affichées)
```
<!-- /resultat -->

**Ex 3.9**

```sql
SELECT code_patient, date_inclusion,
       DATE_ADD(date_inclusion, INTERVAL 336 DAY) AS date_fin_theorique
FROM patient
WHERE date_inclusion IS NOT NULL;
```
<!-- resultat:4 -->
```text
+-------------------+----------------+--------------------+
| code_patient      | date_inclusion | date_fin_theorique |
+-------------------+----------------+--------------------+
| CARDIO-01-C01-001 | 2024-04-30     | 2025-04-01         |
| CARDIO-01-C01-002 | 2024-04-28     | 2025-03-30         |
| CARDIO-01-C01-003 | 2024-05-18     | 2025-04-19         |
| CARDIO-01-C01-004 | 2024-06-24     | 2025-05-26         |
+-------------------+----------------+--------------------+
… 212 lignes au total (4 affichées)
```
<!-- /resultat -->

**Ex 3.10**

```sql
SELECT id, terme, date_survenue, date_resolution,
       DATEDIFF(date_resolution, date_survenue) AS duree_jours
FROM evenement_indesirable
WHERE date_resolution IS NOT NULL
ORDER BY duree_jours DESC, id
LIMIT 5;
```
<!-- resultat -->
```text
+-----+------------------------+---------------+-----------------+-------------+
| id  | terme                  | date_survenue | date_resolution | duree_jours |
+-----+------------------------+---------------+-----------------+-------------+
| 20  | Nausées                | 2025-11-27    | 2025-12-27      | 30          |
| 31  | Toux                   | 2025-04-23    | 2025-05-23      | 30          |
| 51  | Hypotension            | 2024-06-21    | 2024-07-21      | 30          |
| 84  | Infection respiratoire | 2024-11-12    | 2024-12-12      | 30          |
| 100 | Infection respiratoire | 2025-09-26    | 2025-10-26      | 30          |
+-----+------------------------+---------------+-----------------+-------------+
5 lignes
```
<!-- /resultat -->

**Ex 3.11**

```sql
SELECT code_patient,
       CASE
           WHEN annee_naissance < 1950 THEN 'avant 1950'
           WHEN annee_naissance < 1970 THEN '1950-1969'
           ELSE '1970 et après'
       END AS generation
FROM patient;
```
<!-- resultat:4 -->
```text
+-------------------+---------------+
| code_patient      | generation    |
+-------------------+---------------+
| CARDIO-01-C01-001 | 1970 et après |
| CARDIO-01-C01-002 | 1950-1969     |
| CARDIO-01-C01-003 | 1950-1969     |
| CARDIO-01-C01-004 | 1950-1969     |
+-------------------+---------------+
… 262 lignes au total (4 affichées)
```
<!-- /resultat -->

**Ex 3.12**

```sql
SELECT COUNT(*)                                          AS total,
       SUM(CASE WHEN grave THEN 1 ELSE 0 END)            AS graves,
       SUM(CASE WHEN date_resolution IS NULL THEN 1 ELSE 0 END) AS non_resolus
FROM evenement_indesirable;
```
<!-- resultat -->
```text
+-------+--------+-------------+
| total | graves | non_resolus |
+-------+--------+-------------+
| 208   | 26     | 20          |
+-------+--------+-------------+
1 ligne
```
<!-- /resultat -->

Variante pour les non résolus : `COUNT(*) - COUNT(date_resolution)`.

**Ex 3.13**

```sql
SELECT specialite, COUNT(*) AS nb
FROM investigateur
GROUP BY specialite
ORDER BY nb DESC, specialite;
```
<!-- resultat -->
```text
+------------------+----+
| specialite       | nb |
+------------------+----+
| Cardiologie      | 5  |
| Diabétologie     | 4  |
| Oncologie        | 3  |
| Dermatologie     | 2  |
| Médecine interne | 2  |
| Neurologie       | 2  |
+------------------+----+
6 lignes
```
<!-- /resultat -->

**Ex 3.14**

```sql
SELECT etude_id,
       COUNT(date_sortie) AS sortis,
       SUM(CASE WHEN date_inclusion IS NOT NULL AND date_sortie IS NULL THEN 1 ELSE 0 END) AS en_cours
FROM patient
GROUP BY etude_id;
```
<!-- resultat -->
```text
+----------+--------+----------+
| etude_id | sortis | en_cours |
+----------+--------+----------+
| 1        | 79     | 33       |
| 2        | 23     | 26       |
| 3        | 6      | 15       |
| 4        | 30     | 0        |
+----------+--------+----------+
4 lignes
```
<!-- /resultat -->

**Ex 3.15**

```sql
SELECT etude_id,
       ROUND(AVG(DATEDIFF(date_inclusion, date_screening)), 1) AS delai_moyen_jours
FROM patient
WHERE date_inclusion IS NOT NULL
GROUP BY etude_id;
```
<!-- resultat -->
```text
+----------+-------------------+
| etude_id | delai_moyen_jours |
+----------+-------------------+
| 1        | 13.7              |
| 2        | 13.9              |
| 3        | 12.4              |
| 4        | 13.6              |
+----------+-------------------+
4 lignes
```
<!-- /resultat -->

La condition `WHERE` n'est pas indispensable (`DATEDIFF` renvoie NULL pour les non-inclus, et `AVG` ignore les NULL), mais elle est plus claire.

**Ex 3.16**

```sql
SELECT YEAR(date_inclusion) AS annee, COUNT(*) AS inclusions
FROM patient
WHERE etude_id = 1 AND date_inclusion IS NOT NULL
GROUP BY YEAR(date_inclusion)
ORDER BY annee;
```
<!-- resultat -->
```text
+-------+------------+
| annee | inclusions |
+-------+------------+
| 2024  | 41         |
| 2025  | 71         |
+-------+------------+
2 lignes
```
<!-- /resultat -->

**Ex 3.17**

```sql
SELECT patient_id, COUNT(*) AS nb_ei
FROM evenement_indesirable
GROUP BY patient_id
HAVING COUNT(*) >= 3
ORDER BY patient_id;
```
<!-- resultat:30 -->
```text
+------------+-------+
| patient_id | nb_ei |
+------------+-------+
| 28         | 3     |
| 55         | 3     |
| 59         | 3     |
| 68         | 3     |
| 76         | 3     |
| 77         | 3     |
| 109        | 3     |
| 115        | 3     |
| 158        | 3     |
| 176        | 3     |
| 210        | 3     |
| 225        | 3     |
+------------+-------+
12 lignes
```
<!-- /resultat -->

**Ex 3.18**

```sql
SELECT type_visite,
       COUNT(*) AS visites_echues,
       SUM(CASE WHEN date_realisee IS NULL THEN 1 ELSE 0 END) AS manquees,
       ROUND(100 * SUM(CASE WHEN date_realisee IS NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS taux_manquees_pct
FROM visite
WHERE date_prevue < '2026-06-30'
  AND type_visite <> 'V0'
GROUP BY type_visite
ORDER BY type_visite;
```
<!-- resultat -->
```text
+-------------+----------------+----------+-------------------+
| type_visite | visites_echues | manquees | taux_manquees_pct |
+-------------+----------------+----------+-------------------+
| V1          | 210            | 14       | 6.7               |
| V2          | 205            | 22       | 10.7              |
| V3          | 194            | 13       | 6.7               |
| V4          | 155            | 7        | 4.5               |
| V5          | 143            | 14       | 9.8               |
| V6          | 88             | 7        | 8.0               |
+-------------+----------------+----------+-------------------+
6 lignes
```
<!-- /resultat -->

On exclut `V0`, toujours réalisée par définition (c'est la visite d'inclusion).

**Ex 3.19**

```sql
SELECT code, titre
FROM etude
WHERE id NOT IN (SELECT etude_id FROM patient);
```
<!-- resultat -->
```text
+---------+-----------------------------------------------+
| code    | titre                                         |
+---------+-----------------------------------------------+
| DERM-05 | Efficacité de la crème DM-5 dans le psoriasis |
+---------+-----------------------------------------------+
1 ligne
```
<!-- /resultat -->

**Ex 3.20**

```sql
SELECT nom, prenom, specialite
FROM investigateur
WHERE id NOT IN (SELECT investigateur_principal_id FROM etude_centre);
```
<!-- resultat -->
```text
+---------+--------+------------------+
| nom     | prenom | specialite       |
+---------+--------+------------------+
| Bonnet  | Paul   | Médecine interne |
| Sánchez | Javier | Médecine interne |
+---------+--------+------------------+
2 lignes
```
<!-- /resultat -->

**Ex 3.21**

```sql
SELECT code_patient
FROM patient
WHERE id IN (
    SELECT patient_id
    FROM visite
    WHERE id IN (SELECT visite_id FROM mesure WHERE parametre = 'poids' AND valeur > 100)
)
ORDER BY code_patient;
```
<!-- resultat:20 -->
```text
+-------------------+
| code_patient      |
+-------------------+
| CARDIO-01-C01-007 |
| CARDIO-01-C02-005 |
| CARDIO-01-C03-009 |
| DIAB-02-C05-002   |
| DIAB-02-C05-007   |
| NEURO-04-C01-009  |
| ONCO-03-C04-010   |
+-------------------+
7 lignes
```
<!-- /resultat -->

*(Trouver le **dernier** relevé de chaque patient est plus délicat : ce sera traité au module 7 avec les fonctions de fenêtrage.)*

**Ex 3.22**

```sql
SELECT ec.etude_id, ec.centre_id, ec.objectif_inclusions,
       (SELECT COUNT(date_inclusion) FROM patient p
         WHERE p.etude_id = ec.etude_id AND p.centre_id = ec.centre_id) AS inclus
FROM etude_centre ec
WHERE (SELECT COUNT(date_inclusion) FROM patient p
        WHERE p.etude_id = ec.etude_id AND p.centre_id = ec.centre_id)
      < ec.objectif_inclusions / 2;
```
<!-- resultat -->
```text
+----------+-----------+---------------------+--------+
| etude_id | centre_id | objectif_inclusions | inclus |
+----------+-----------+---------------------+--------+
| 2        | 3         | 20                  | 9      |
| 2        | 7         | 15                  | 6      |
| 3        | 4         | 20                  | 7      |
| 3        | 6         | 20                  | 4      |
| 5        | 1         | 50                  | 0      |
| 5        | 8         | 50                  | 0      |
+----------+-----------+---------------------+--------+
6 lignes
```
<!-- /resultat -->

On répète la sous-requête dans le `WHERE` car l'alias `inclus` n'y est pas encore connu (ordre d'exécution, 3.7). Avec une sous-requête dans le `FROM`, on éviterait la répétition :

```sql
SELECT *
FROM (
    SELECT ec.etude_id, ec.centre_id, ec.objectif_inclusions,
           (SELECT COUNT(date_inclusion) FROM patient p
             WHERE p.etude_id = ec.etude_id AND p.centre_id = ec.centre_id) AS inclus
    FROM etude_centre ec
) AS t
WHERE inclus < objectif_inclusions / 2;
```
<!-- resultat -->
```text
+----------+-----------+---------------------+--------+
| etude_id | centre_id | objectif_inclusions | inclus |
+----------+-----------+---------------------+--------+
| 2        | 3         | 20                  | 9      |
| 2        | 7         | 15                  | 6      |
| 3        | 4         | 20                  | 7      |
| 3        | 6         | 20                  | 4      |
| 5        | 1         | 50                  | 0      |
| 5        | 8         | 50                  | 0      |
+----------+-----------+---------------------+--------+
6 lignes
```
<!-- /resultat -->

**Ex 3.23**

```sql
SELECT terme,
       COUNT(*) AS nb,
       ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM evenement_indesirable), 1) AS part_pct
FROM evenement_indesirable
GROUP BY terme
ORDER BY nb DESC, terme
LIMIT 8;
```
<!-- resultat -->
```text
+------------------------+----+----------+
| terme                  | nb | part_pct |
+------------------------+----+----------+
| Douleur abdominale     | 34 | 16.3     |
| Vertiges               | 24 | 11.5     |
| Fatigue                | 23 | 11.1     |
| Céphalées              | 20 | 9.6      |
| Infection respiratoire | 17 | 8.2      |
| Insomnie               | 17 | 8.2      |
| Œdème des chevilles    | 17 | 8.2      |
| Nausées                | 16 | 7.7      |
+------------------------+----+----------+
8 lignes
```
<!-- /resultat -->
