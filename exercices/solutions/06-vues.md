# Corrigés — Module 6 : Création de vues

On recrée d'abord les vues du cours utilisées ici.

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_tableau_de_bord_recrutement AS
SELECT e.code AS etude, c.nom AS centre, c.pays, ec.date_ouverture,
       ec.objectif_inclusions AS objectif,
       COUNT(p.id) AS screenes, COUNT(p.date_inclusion) AS inclus,
       COUNT(p.id) - COUNT(p.date_inclusion) AS echecs_screening,
       ROUND(100 * COUNT(p.date_inclusion) / ec.objectif_inclusions, 1) AS atteinte_pct
FROM etude_centre ec
JOIN etude e ON ec.etude_id = e.id
JOIN centre c ON ec.centre_id = c.id
LEFT JOIN patient p ON p.etude_id = ec.etude_id AND p.centre_id = ec.centre_id
GROUP BY e.code, c.nom, c.pays, ec.date_ouverture, ec.objectif_inclusions;
```

**Ex 6.1**

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_investigateur_detail AS
SELECT i.id,
       CONCAT(i.prenom, ' ', UPPER(i.nom)) AS investigateur,
       i.specialite,
       c.nom   AS centre,
       c.ville,
       c.pays,
       CONCAT(s.prenom, ' ', UPPER(s.nom)) AS superviseur
FROM investigateur i
JOIN centre c ON i.centre_id = c.id
LEFT JOIN investigateur s ON i.superviseur_id = s.id;
```

```sql
SELECT * FROM v_investigateur_detail ORDER BY id;
```
<!-- resultat:5 -->
```text
+----+---------------+--------------+--------------------------+--------+--------+---------------+
| id | investigateur | specialite   | centre                   | ville  | pays   | superviseur   |
+----+---------------+--------------+--------------------------+--------+--------+---------------+
| 1  | Claire MARTIN | Cardiologie  | Clinique du Val de Loire | Tours  | France | NULL          |
| 2  | Hugo BERNARD  | Diabétologie | Clinique du Val de Loire | Tours  | France | Claire MARTIN |
| 3  | Inès PETIT    | Neurologie   | Clinique du Val de Loire | Tours  | France | Claire MARTIN |
| 4  | Lucas ROBERT  | Dermatologie | Clinique du Val de Loire | Tours  | France | Claire MARTIN |
| 5  | Sophie DURAND | Oncologie    | CHU Atlantique           | Nantes | France | NULL          |
+----+---------------+--------------+--------------------------+--------+--------+---------------+
… 18 lignes au total (5 affichées)
```
<!-- /resultat -->

`CONCAT` renvoie NULL si un argument est NULL : les chefs ont donc bien un superviseur NULL.

**Ex 6.2**

```sql
SELECT investigateur, specialite, ville, pays
FROM v_investigateur_detail
WHERE pays <> 'France'
ORDER BY pays, investigateur;
```
<!-- resultat -->
```text
+----------------+------------------+----------+----------+
| investigateur  | specialite       | ville    | pays     |
+----------------+------------------+----------+----------+
| Marc DUBOIS    | Dermatologie     | Liège    | Belgique |
| Carmen LÓPEZ   | Diabétologie     | Valencia | Espagne  |
| Javier SÁNCHEZ | Médecine interne | Valencia | Espagne  |
| Anna MÜLLER    | Cardiologie      | Genève   | Suisse   |
| Nicolas FAVRE  | Oncologie        | Genève   | Suisse   |
+----------------+------------------+----------+----------+
5 lignes
```
<!-- /resultat -->

**Ex 6.3**

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_ei_detail AS
SELECT ei.id,
       e.code AS etude,
       p.code_patient,
       p.bras,
       c.ville,
       ei.terme,
       ei.grade,
       CASE WHEN ei.grave THEN 'oui' ELSE 'non' END AS grave,
       ei.date_survenue,
       DATEDIFF(ei.date_resolution, ei.date_survenue) AS duree_jours,
       CASE WHEN ei.date_resolution IS NULL THEN 'en cours' ELSE 'résolu' END AS statut
FROM evenement_indesirable ei
JOIN patient p ON ei.patient_id = p.id
JOIN etude   e ON p.etude_id    = e.id
JOIN centre  c ON p.centre_id   = c.id;
```

```sql
SELECT * FROM v_ei_detail ORDER BY id LIMIT 5;
```
<!-- resultat -->
```text
+----+-----------+-------------------+------------+-------+---------------------+-------+-------+---------------+-------------+--------+
| id | etude     | code_patient      | bras       | ville | terme               | grade | grave | date_survenue | duree_jours | statut |
+----+-----------+-------------------+------------+-------+---------------------+-------+-------+---------------+-------------+--------+
| 1  | CARDIO-01 | CARDIO-01-C01-001 | placebo    | Tours | Œdème des chevilles | 2     | non   | 2024-06-11    | 4           | résolu |
| 2  | CARDIO-01 | CARDIO-01-C01-006 | placebo    | Tours | Nausées             | 2     | non   | 2024-12-15    | 25          | résolu |
| 3  | CARDIO-01 | CARDIO-01-C01-010 | placebo    | Tours | Céphalées           | 1     | non   | 2025-03-29    | 4           | résolu |
| 4  | CARDIO-01 | CARDIO-01-C01-010 | placebo    | Tours | Toux                | 1     | non   | 2025-02-14    | 18          | résolu |
| 5  | CARDIO-01 | CARDIO-01-C01-012 | traitement | Tours | Hypotension         | 1     | non   | 2025-04-27    | 9           | résolu |
+----+-----------+-------------------+------------+-------+---------------------+-------+-------+---------------+-------------+--------+
5 lignes
```
<!-- /resultat -->

**Ex 6.4**

```sql
SELECT id, etude, code_patient, terme, grade, date_survenue
FROM v_ei_detail
WHERE (terme LIKE '%douleur%' OR terme LIKE 'Vert%')
  AND date_survenue BETWEEN '2026-01-01' AND '2026-06-30'
ORDER BY date_survenue, id;
```
<!-- resultat:20 -->
```text
+-----+-----------+-------------------+--------------------+-------+---------------+
| id  | etude     | code_patient      | terme              | grade | date_survenue |
+-----+-----------+-------------------+--------------------+-------+---------------+
| 119 | DIAB-02   | DIAB-02-C01-018   | Vertiges           | 1     | 2026-01-14    |
| 152 | DIAB-02   | DIAB-02-C07-001   | Douleur abdominale | 3     | 2026-01-24    |
| 40  | CARDIO-01 | CARDIO-01-C02-019 | Douleur abdominale | 3     | 2026-02-14    |
| 22  | CARDIO-01 | CARDIO-01-C01-031 | Douleur abdominale | 2     | 2026-02-21    |
| 147 | DIAB-02   | DIAB-02-C05-019   | Douleur abdominale | 2     | 2026-03-01    |
| 79  | CARDIO-01 | CARDIO-01-C03-028 | Vertiges           | 3     | 2026-03-03    |
| 18  | CARDIO-01 | CARDIO-01-C01-029 | Douleur abdominale | 2     | 2026-03-13    |
| 19  | CARDIO-01 | CARDIO-01-C01-029 | Douleur abdominale | 2     | 2026-03-16    |
| 180 | ONCO-03   | ONCO-03-C06-004   | Vertiges           | 2     | 2026-03-27    |
| 78  | CARDIO-01 | CARDIO-01-C03-026 | Vertiges           | 1     | 2026-04-06    |
| 113 | DIAB-02   | DIAB-02-C01-014   | Douleur abdominale | 2     | 2026-04-29    |
| 158 | ONCO-03   | ONCO-03-C02-005   | Vertiges           | 1     | 2026-05-05    |
| 139 | DIAB-02   | DIAB-02-C05-008   | Douleur abdominale | 3     | 2026-05-31    |
| 95  | CARDIO-01 | CARDIO-01-C04-017 | Douleur abdominale | 3     | 2026-06-06    |
| 131 | DIAB-02   | DIAB-02-C03-011   | Vertiges           | 1     | 2026-06-09    |
| 170 | ONCO-03   | ONCO-03-C04-007   | Douleur abdominale | 1     | 2026-06-14    |
| 164 | ONCO-03   | ONCO-03-C02-014   | Vertiges           | 1     | 2026-06-17    |
| 81  | CARDIO-01 | CARDIO-01-C03-030 | Douleur abdominale | 2     | 2026-06-18    |
| 104 | CARDIO-01 | CARDIO-01-C06-016 | Vertiges           | 4     | 2026-06-18    |
| 175 | ONCO-03   | ONCO-03-C04-010   | Vertiges           | 2     | 2026-06-23    |
+-----+-----------+-------------------+--------------------+-------+---------------+
… 23 lignes au total (20 affichées)
```
<!-- /resultat -->

Les parenthèses autour du `OR` sont indispensables. En MySQL, `LIKE '%douleur%'` trouve aussi « Douleur » (collation insensible à la casse).

**Ex 6.5**

```sql
SELECT grade, COUNT(*) AS nb_resolus, ROUND(AVG(duree_jours), 1) AS duree_moyenne
FROM v_ei_detail
WHERE statut = 'résolu'
GROUP BY grade
ORDER BY grade;
```
<!-- resultat -->
```text
+-------+------------+---------------+
| grade | nb_resolus | duree_moyenne |
+-------+------------+---------------+
| 1     | 89         | 16.7          |
| 2     | 60         | 14.9          |
| 3     | 28         | 15.8          |
| 4     | 11         | 13.9          |
+-------+------------+---------------+
4 lignes
```
<!-- /resultat -->

**Ex 6.6**

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_inclusions_mensuelles AS
SELECT e.code AS etude,
       DATE_FORMAT(p.date_inclusion, '%Y-%m') AS mois,
       COUNT(*) AS inclusions
FROM patient p
JOIN etude e ON p.etude_id = e.id
WHERE p.date_inclusion IS NOT NULL
GROUP BY e.code, DATE_FORMAT(p.date_inclusion, '%Y-%m');
```

```sql
SELECT m.etude, m.mois, m.inclusions
FROM v_inclusions_mensuelles m
WHERE m.inclusions = (SELECT MAX(m2.inclusions)
                      FROM v_inclusions_mensuelles m2
                      WHERE m2.etude = m.etude)
ORDER BY m.etude, m.mois;
```
<!-- resultat -->
```text
+-----------+---------+------------+
| etude     | mois    | inclusions |
+-----------+---------+------------+
| CARDIO-01 | 2025-08 | 16         |
| DIAB-02   | 2025-03 | 6          |
| DIAB-02   | 2025-12 | 6          |
| NEURO-04  | 2023-04 | 9          |
| ONCO-03   | 2026-03 | 5          |
+-----------+---------+------------+
5 lignes
```
<!-- /resultat -->

En cas d'égalité, plusieurs mois peuvent sortir pour une même étude.

**Ex 6.7**

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_derniere_visite AS
SELECT p.id AS patient_id,
       p.code_patient,
       p.date_sortie,
       v.type_visite,
       v.date_realisee AS date_derniere_visite
FROM patient p
JOIN visite v ON v.patient_id = p.id
WHERE p.date_inclusion IS NOT NULL
  AND v.date_realisee = (SELECT MAX(v2.date_realisee)
                         FROM visite v2
                         WHERE v2.patient_id = p.id);
```

```sql
SELECT code_patient, type_visite, date_derniere_visite,
       DATEDIFF('2026-06-30', date_derniere_visite) AS jours_depuis
FROM v_derniere_visite
WHERE date_sortie IS NULL
  AND DATEDIFF('2026-06-30', date_derniere_visite) > 120
ORDER BY jours_depuis DESC;
```
<!-- resultat:20 -->
```text
+-------------------+-------------+----------------------+--------------+
| code_patient      | type_visite | date_derniere_visite | jours_depuis |
+-------------------+-------------+----------------------+--------------+
| CARDIO-01-C02-011 | V4          | 2024-12-20           | 557          |
| CARDIO-01-C01-007 | V5          | 2025-01-21           | 525          |
| CARDIO-01-C03-008 | V5          | 2025-03-15           | 472          |
| CARDIO-01-C03-009 | V5          | 2025-03-19           | 468          |
| DIAB-02-C05-008   | V5          | 2025-10-06           | 267          |
| CARDIO-01-C06-018 | V4          | 2025-11-16           | 226          |
| CARDIO-01-C03-024 | V5          | 2025-11-21           | 221          |
| ONCO-03-C02-004   | V4          | 2025-12-03           | 209          |
| DIAB-02-C05-010   | V5          | 2025-12-11           | 201          |
| CARDIO-01-C06-015 | V5          | 2026-01-18           | 163          |
| CARDIO-01-C01-030 | V5          | 2026-01-22           | 159          |
| CARDIO-01-C04-013 | V5          | 2026-01-23           | 158          |
| CARDIO-01-C01-029 | V5          | 2026-01-25           | 156          |
| CARDIO-01-C02-023 | V5          | 2026-01-25           | 156          |
| CARDIO-01-C06-017 | V5          | 2026-01-30           | 151          |
| DIAB-02-C01-012   | V5          | 2026-01-30           | 151          |
| CARDIO-01-C06-016 | V5          | 2026-02-01           | 149          |
| CARDIO-01-C01-032 | V5          | 2026-02-02           | 148          |
| CARDIO-01-C04-015 | V5          | 2026-02-02           | 148          |
| CARDIO-01-C01-031 | V5          | 2026-02-03           | 147          |
+-------------------+-------------+----------------------+--------------+
… 30 lignes au total (20 affichées)
```
<!-- /resultat -->

Ces patients ne sont pas forcément « perdus » : l'intervalle entre V4 (J84) et V5 (J168) dépasse 80 jours, et V5 → V6 près de 170 jours. Un bon indicateur comparerait plutôt la date du jour à la **prochaine visite prévue**.

**Ex 6.8**

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_alerte_centres AS
SELECT etude, centre, inclus, objectif, atteinte_pct,
       ROUND(100 * echecs_screening / screenes, 1) AS taux_echec_pct,
       CASE
           WHEN atteinte_pct < 50 AND 100 * echecs_screening / screenes > 25
                THEN 'recrutement faible et échecs élevés'
           WHEN atteinte_pct < 50 THEN 'recrutement faible'
           ELSE 'échecs de screening élevés'
       END AS motif_alerte
FROM v_tableau_de_bord_recrutement
WHERE date_ouverture IS NOT NULL
  AND (atteinte_pct < 50 OR 100 * echecs_screening / screenes > 25);
```

```sql
SELECT * FROM v_alerte_centres ORDER BY etude, centre;
```
<!-- resultat -->
```text
+---------+-----------------------------+--------+----------+--------------+----------------+-------------------------------------+
| etude   | centre                      | inclus | objectif | atteinte_pct | taux_echec_pct | motif_alerte                        |
+---------+-----------------------------+--------+----------+--------------+----------------+-------------------------------------+
| DIAB-02 | Clinique du Val de Loire    | 15     | 20       | 75.0         | 28.6           | échecs de screening élevés          |
| DIAB-02 | Hôpital Saint-Roch          | 9      | 20       | 45.0         | 18.2           | recrutement faible                  |
| DIAB-02 | Hospital del Sol            | 6      | 15       | 40.0         | 25.0           | recrutement faible                  |
| ONCO-03 | Centre Hospitalier du Rhône | 7      | 20       | 35.0         | 30.0           | recrutement faible et échecs élevés |
| ONCO-03 | CHU Atlantique              | 10     | 20       | 50.0         | 28.6           | échecs de screening élevés          |
| ONCO-03 | Clinique du Léman           | 4      | 20       | 20.0         | 33.3           | recrutement faible et échecs élevés |
+---------+-----------------------------+--------+----------+--------------+----------------+-------------------------------------+
6 lignes
```
<!-- /resultat -->

`date_ouverture IS NOT NULL` écarte aussi les centres sans patient, ce qui évite une division par zéro (`screenes` = 0). (En MySQL, une division par zéro renvoie NULL plutôt qu'une erreur.)

**Ex 6.9** — Non : une vue est **toujours recalculée** sur les données actuelles, elle ne garde pas l'historique. Il faut une **table** d'historique, alimentée chaque mois par un `INSERT … SELECT` depuis la vue :

<!-- exec -->
```sql
CREATE TABLE historique_recrutement (
    date_photo     DATE         NOT NULL,
    etude          VARCHAR(20)  NOT NULL,
    centre         VARCHAR(100) NOT NULL,
    objectif       INT          NOT NULL,
    inclus         INT          NOT NULL,
    atteinte_pct   DECIMAL(5,1) NULL,
    CONSTRAINT pk_historique_recrutement PRIMARY KEY (date_photo, etude, centre)
);
```

```sql
-- à exécuter le 1er de chaque mois (ici, la photo du 30/06/2026)
INSERT INTO historique_recrutement (date_photo, etude, centre, objectif, inclus, atteinte_pct)
SELECT '2026-06-30', etude, centre, objectif, inclus, atteinte_pct
FROM v_tableau_de_bord_recrutement;
```
<!-- resultat -->
```text
Requête OK, 16 lignes affectées
```
<!-- /resultat -->

On peut ensuite suivre l'évolution d'un centre de mois en mois avec un simple `SELECT … FROM historique_recrutement WHERE centre = … ORDER BY date_photo`. L'exécution mensuelle peut être automatisée (planificateur d'événements MySQL, ou outil externe).
