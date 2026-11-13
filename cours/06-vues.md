# Module 6 — Création de vues

> **Objectif** : enregistrer des requêtes sous forme de **vues** pour les réutiliser simplement, construire une couche d'indicateurs prête pour le reporting, et maîtriser les filtres `LIKE`, `IN`, `IS NULL`, `BETWEEN`.
> **Durée indicative** : 3 h

---

## 6.1 Qu'est-ce qu'une vue ?

### Concept

Une **vue** est une requête `SELECT` **enregistrée dans la base sous un nom**. On l'interroge ensuite **exactement comme une table** — mais elle ne stocke **aucune donnée** : à chaque utilisation, la requête est ré-exécutée sur les données du moment.

```
CREATE VIEW nom_vue AS
SELECT … ;               ← n'importe quelle requête (jointures, agrégats, CASE…)

SELECT * FROM nom_vue WHERE … ;
```

### Visuel

```
         TABLES (les données)                    VUE (une requête enregistrée)
  ┌─────────┐ ┌─────────┐ ┌────────┐          ┌──────────────────────────────────┐
  │ patient │ │  etude  │ │ centre │  ──────► │ v_patient_detail                 │
  └─────────┘ └─────────┘ └────────┘          │  = SELECT … FROM patient         │
                                              │    JOIN etude … JOIN centre …    │
                                              └──────────────────────────────────┘
                                                            │
       l'utilisateur écrit simplement :                     ▼
       SELECT * FROM v_patient_detail WHERE ville = 'Tours';
       et le SGBD exécute la requête complète, sur les données à jour.
```

### Pourquoi des vues ?

| Avantage | Exemple |
|---|---|
| **Simplifier** : on écrit une fois une jointure complexe, on la réutilise partout | `v_patient_detail` au lieu de 3 jointures à chaque fois |
| **Uniformiser** : tout le monde calcule l'indicateur de la même façon | « taux d'échec de screening » défini une seule fois |
| **Sécuriser** : donner accès à certaines colonnes seulement | une vue sans `annee_naissance` pour un prestataire |
| **Brancher des outils** : Excel, Power BI… lisent une vue comme une table | un tableau croisé dynamique branché sur `v_tableau_de_bord_recrutement` |

| | Vue | Table créée par `CREATE TABLE … AS SELECT` |
|---|---|---|
| Stocke des données | non | oui (une copie) |
| Toujours à jour | **oui** | non (photo à l'instant T) |
| Place occupée | quasi nulle | autant que les données |
| Rapidité | recalculée à chaque appel | lecture directe |

---

## 6.2 `CREATE VIEW` simple

### Exemples

**Une vue « patient détaillé »** :

<!-- exec -->
```sql
CREATE VIEW v_patient_detail AS
SELECT p.id            AS patient_id,
       p.code_patient,
       e.code          AS etude,
       e.phase,
       c.nom           AS centre,
       c.ville,
       c.pays,
       p.sexe,
       p.annee_naissance,
       2026 - p.annee_naissance AS age,
       p.date_screening,
       p.date_inclusion,
       p.bras,
       p.date_sortie,
       p.motif_sortie,
       CASE
           WHEN p.date_inclusion IS NULL THEN 'échec de screening'
           WHEN p.date_sortie IS NULL    THEN 'en cours'
           WHEN p.motif_sortie = 'fin d''étude' THEN 'terminé'
           ELSE 'sortie prématurée'
       END AS statut
FROM patient p
JOIN etude  e ON p.etude_id  = e.id
JOIN centre c ON p.centre_id = c.id;
```

**L'utiliser comme une table** :

```sql
SELECT code_patient, etude, centre, age, statut
FROM v_patient_detail
WHERE ville = 'Genève';
```
<!-- resultat:6 -->
```text
+-------------------+-----------+-------------------+-----+--------------------+
| code_patient      | etude     | centre            | age | statut             |
+-------------------+-----------+-------------------+-----+--------------------+
| CARDIO-01-C06-001 | CARDIO-01 | Clinique du Léman | 80  | échec de screening |
| CARDIO-01-C06-002 | CARDIO-01 | Clinique du Léman | 76  | terminé            |
| CARDIO-01-C06-003 | CARDIO-01 | Clinique du Léman | 69  | terminé            |
| CARDIO-01-C06-004 | CARDIO-01 | Clinique du Léman | 56  | terminé            |
| CARDIO-01-C06-005 | CARDIO-01 | Clinique du Léman | 80  | terminé            |
| CARDIO-01-C06-006 | CARDIO-01 | Clinique du Léman | 70  | terminé            |
+-------------------+-----------+-------------------+-----+--------------------+
… 27 lignes au total (6 affichées)
```
<!-- /resultat -->

```sql
SELECT etude, statut, COUNT(*) AS nb
FROM v_patient_detail
GROUP BY etude, statut
ORDER BY etude, nb DESC;
```
<!-- resultat:20 -->
```text
+-----------+--------------------+----+
| etude     | statut             | nb |
+-----------+--------------------+----+
| CARDIO-01 | terminé            | 63 |
| CARDIO-01 | en cours           | 33 |
| CARDIO-01 | échec de screening | 24 |
| CARDIO-01 | sortie prématurée  | 16 |
| DIAB-02   | en cours           | 26 |
| DIAB-02   | terminé            | 18 |
| DIAB-02   | échec de screening | 15 |
| DIAB-02   | sortie prématurée  | 5  |
| NEURO-04  | terminé            | 29 |
| NEURO-04  | échec de screening | 2  |
| NEURO-04  | sortie prématurée  | 1  |
| ONCO-03   | en cours           | 15 |
| ONCO-03   | échec de screening | 9  |
| ONCO-03   | sortie prématurée  | 5  |
| ONCO-03   | terminé            | 1  |
+-----------+--------------------+----+
15 lignes
```
<!-- /resultat -->

Sans la vue, cette dernière requête aurait demandé deux jointures et le `CASE` complet.

**Modifier une vue** : `CREATE OR REPLACE VIEW` (même nom, nouvelle définition).

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_centre_actif AS
SELECT DISTINCT c.id, c.nom, c.ville, c.pays
FROM centre c
JOIN etude_centre ec ON ec.centre_id = c.id
WHERE ec.date_ouverture IS NOT NULL;
```

```sql
SELECT * FROM v_centre_actif ORDER BY id;
```
<!-- resultat -->
```text
+----+-----------------------------+-------------+---------+
| id | nom                         | ville       | pays    |
+----+-----------------------------+-------------+---------+
| 1  | Clinique du Val de Loire    | Tours       | France  |
| 2  | CHU Atlantique              | Nantes      | France  |
| 3  | Hôpital Saint-Roch          | Montpellier | France  |
| 4  | Centre Hospitalier du Rhône | Lyon        | France  |
| 5  | Clinique des Flandres       | Lille       | France  |
| 6  | Clinique du Léman           | Genève      | Suisse  |
| 7  | Hospital del Sol            | Valencia    | Espagne |
+----+-----------------------------+-------------+---------+
7 lignes
```
<!-- /resultat -->

**Lister et supprimer des vues** :

```sql
-- MySQL : lister les vues de la base
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- SQL standard : le dictionnaire de données
SELECT table_name FROM information_schema.views WHERE table_schema = 'essais_cliniques';

-- voir la définition d'une vue (MySQL)
SHOW CREATE VIEW v_patient_detail;

-- supprimer
DROP VIEW v_centre_actif;
DROP VIEW IF EXISTS v_centre_actif;
```

> 💡 Dans DBeaver, les vues apparaissent dans le dossier **Vues** de la base, à côté des **Tables**.

---

## 6.3 Vues complexes : une couche d'indicateurs

### Concept

Le vrai pouvoir des vues : construire un **tableau de bord** sous forme de vues, que n'importe qui (ou n'importe quel outil) peut interroger sans connaître le SQL complexe qui est derrière. On peut aussi bâtir des vues **sur d'autres vues**.

```
   tables ──► v_patient_detail ──┐
                                 ├──► v_tableau_de_bord_recrutement
   tables ───────────────────────┤
                                 ├──► v_tableau_de_bord_visites
                                 └──► v_tableau_de_bord_securite
                                              │
                                              ▼
                            Excel / Power BI / requêtes simples
```

### Exemple 1 — le recrutement par centre

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_tableau_de_bord_recrutement AS
SELECT e.code                                  AS etude,
       c.nom                                   AS centre,
       c.pays,
       ec.date_ouverture,
       ec.objectif_inclusions                  AS objectif,
       COUNT(p.id)                             AS screenes,
       COUNT(p.date_inclusion)                 AS inclus,
       COUNT(p.id) - COUNT(p.date_inclusion)   AS echecs_screening,
       ROUND(100 * COUNT(p.date_inclusion) / ec.objectif_inclusions, 1) AS atteinte_pct
FROM etude_centre ec
JOIN etude  e      ON ec.etude_id  = e.id
JOIN centre c      ON ec.centre_id = c.id
LEFT JOIN patient p ON p.etude_id  = ec.etude_id
                   AND p.centre_id = ec.centre_id
GROUP BY e.code, c.nom, c.pays, ec.date_ouverture, ec.objectif_inclusions;
```

```sql
SELECT * FROM v_tableau_de_bord_recrutement ORDER BY etude, atteinte_pct DESC, centre;
```
<!-- resultat:20 -->
```text
+-----------+-----------------------------+----------+----------------+----------+----------+--------+------------------+--------------+
| etude     | centre                      | pays     | date_ouverture | objectif | screenes | inclus | echecs_screening | atteinte_pct |
+-----------+-----------------------------+----------+----------------+----------+----------+--------+------------------+--------------+
| CARDIO-01 | Clinique du Val de Loire    | France   | 2024-03-15     | 30       | 40       | 33     | 7                | 110.0        |
| CARDIO-01 | Hôpital Saint-Roch          | France   | 2024-05-10     | 25       | 32       | 26     | 6                | 104.0        |
| CARDIO-01 | Clinique du Léman           | Suisse   | 2024-09-01     | 20       | 21       | 18     | 3                | 90.0         |
| CARDIO-01 | CHU Atlantique              | France   | 2024-04-01     | 25       | 25       | 21     | 4                | 84.0         |
| CARDIO-01 | Centre Hospitalier du Rhône | France   | 2024-06-01     | 20       | 18       | 14     | 4                | 70.0         |
| DERM-05   | Centre Médical des Ardennes | Belgique | NULL           | 50       | 0        | 0      | 0                | 0.0          |
| DERM-05   | Clinique du Val de Loire    | France   | NULL           | 50       | 0        | 0      | 0                | 0.0          |
| DIAB-02   | Clinique des Flandres       | France   | 2025-02-15     | 25       | 24       | 19     | 5                | 76.0         |
| DIAB-02   | Clinique du Val de Loire    | France   | 2025-02-01     | 20       | 21       | 15     | 6                | 75.0         |
| DIAB-02   | Hôpital Saint-Roch          | France   | 2025-03-01     | 20       | 11       | 9      | 2                | 45.0         |
| DIAB-02   | Hospital del Sol            | Espagne  | 2025-05-01     | 15       | 8        | 6      | 2                | 40.0         |
| NEURO-04  | CHU Atlantique              | France   | 2023-02-01     | 15       | 16       | 15     | 1                | 100.0        |
| NEURO-04  | Clinique du Val de Loire    | France   | 2023-01-20     | 15       | 16       | 15     | 1                | 100.0        |
| ONCO-03   | CHU Atlantique              | France   | 2025-07-01     | 20       | 14       | 10     | 4                | 50.0         |
| ONCO-03   | Centre Hospitalier du Rhône | France   | 2025-08-15     | 20       | 10       | 7      | 3                | 35.0         |
| ONCO-03   | Clinique du Léman           | Suisse   | 2025-10-01     | 20       | 6        | 4      | 2                | 20.0         |
+-----------+-----------------------------+----------+----------------+----------+----------+--------+------------------+--------------+
16 lignes
```
<!-- /resultat -->

**Une fois la vue créée, les questions deviennent simples** :

```sql
-- les centres en retard (moins de 50 % de l'objectif), parmi ceux qui sont ouverts
SELECT etude, centre, inclus, objectif, atteinte_pct
FROM v_tableau_de_bord_recrutement
WHERE atteinte_pct < 50
  AND date_ouverture IS NOT NULL
ORDER BY atteinte_pct;
```
<!-- resultat -->
```text
+---------+-----------------------------+--------+----------+--------------+
| etude   | centre                      | inclus | objectif | atteinte_pct |
+---------+-----------------------------+--------+----------+--------------+
| ONCO-03 | Clinique du Léman           | 4      | 20       | 20.0         |
| ONCO-03 | Centre Hospitalier du Rhône | 7      | 20       | 35.0         |
| DIAB-02 | Hospital del Sol            | 6      | 15       | 40.0         |
| DIAB-02 | Hôpital Saint-Roch          | 9      | 20       | 45.0         |
+---------+-----------------------------+--------+----------+--------------+
4 lignes
```
<!-- /resultat -->

```sql
-- le total par étude, à partir de la vue
SELECT etude, SUM(objectif) AS objectif, SUM(inclus) AS inclus
FROM v_tableau_de_bord_recrutement
GROUP BY etude
ORDER BY etude;
```
<!-- resultat -->
```text
+-----------+----------+--------+
| etude     | objectif | inclus |
+-----------+----------+--------+
| CARDIO-01 | 120      | 112    |
| DERM-05   | 100      | 0      |
| DIAB-02   | 80       | 49     |
| NEURO-04  | 30       | 30     |
| ONCO-03   | 60       | 21     |
+-----------+----------+--------+
5 lignes
```
<!-- /resultat -->

### Exemple 2 — l'observance des visites

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_tableau_de_bord_visites AS
SELECT e.code AS etude,
       v.type_visite,
       COUNT(*)                                                    AS visites_echues,
       COUNT(v.date_realisee)                                      AS realisees,
       COUNT(*) - COUNT(v.date_realisee)                           AS manquees,
       ROUND(100 * (COUNT(*) - COUNT(v.date_realisee)) / COUNT(*), 1) AS taux_manquees_pct,
       ROUND(AVG(DATEDIFF(v.date_realisee, v.date_prevue)), 1)     AS ecart_moyen_jours
FROM visite v
JOIN patient p ON v.patient_id = p.id
JOIN etude   e ON p.etude_id   = e.id
WHERE v.date_prevue <= '2026-06-30'
GROUP BY e.code, v.type_visite;
```

```sql
SELECT * FROM v_tableau_de_bord_visites WHERE etude = 'CARDIO-01' ORDER BY type_visite;
```
<!-- resultat -->
```text
+-----------+-------------+----------------+-----------+----------+-------------------+-------------------+
| etude     | type_visite | visites_echues | realisees | manquees | taux_manquees_pct | ecart_moyen_jours |
+-----------+-------------+----------------+-----------+----------+-------------------+-------------------+
| CARDIO-01 | V0          | 112            | 112       | 0        | 0.0               | 0.0               |
| CARDIO-01 | V1          | 111            | 103       | 8        | 7.2               | 1.9               |
| CARDIO-01 | V2          | 110            | 98        | 12       | 10.9              | 1.8               |
| CARDIO-01 | V3          | 105            | 97        | 8        | 7.6               | 2.1               |
| CARDIO-01 | V4          | 102            | 97        | 5        | 4.9               | 1.7               |
| CARDIO-01 | V5          | 101            | 93        | 8        | 7.9               | 2.3               |
| CARDIO-01 | V6          | 68             | 63        | 5        | 7.4               | 2.4               |
+-----------+-------------+----------------+-----------+----------+-------------------+-------------------+
7 lignes
```
<!-- /resultat -->

### Exemple 3 — la sécurité par étude et par bras

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_tableau_de_bord_securite AS
SELECT e.code AS etude,
       p.bras,
       COUNT(DISTINCT p.id)                                         AS patients_inclus,
       COUNT(ei.id)                                                 AS nb_ei,
       SUM(CASE WHEN ei.grave THEN 1 ELSE 0 END)                    AS nb_ei_graves,
       COUNT(DISTINCT ei.patient_id)                                AS patients_avec_ei,
       ROUND(100 * COUNT(DISTINCT ei.patient_id) / COUNT(DISTINCT p.id), 1) AS pct_patients_avec_ei
FROM patient p
JOIN etude e ON p.etude_id = e.id
LEFT JOIN evenement_indesirable ei ON ei.patient_id = p.id
WHERE p.date_inclusion IS NOT NULL
GROUP BY e.code, p.bras;
```

```sql
SELECT * FROM v_tableau_de_bord_securite ORDER BY etude, bras;
```
<!-- resultat -->
```text
+-----------+------------+-----------------+-------+--------------+------------------+----------------------+
| etude     | bras       | patients_inclus | nb_ei | nb_ei_graves | patients_avec_ei | pct_patients_avec_ei |
+-----------+------------+-----------------+-------+--------------+------------------+----------------------+
| CARDIO-01 | placebo    | 60              | 40    | 5            | 30               | 50.0                 |
| CARDIO-01 | traitement | 52              | 67    | 6            | 40               | 76.9                 |
| DIAB-02   | placebo    | 26              | 17    | 0            | 13               | 50.0                 |
| DIAB-02   | traitement | 23              | 30    | 6            | 20               | 87.0                 |
| NEURO-04  | placebo    | 16              | 13    | 3            | 11               | 68.8                 |
| NEURO-04  | traitement | 14              | 15    | 2            | 11               | 78.6                 |
| ONCO-03   | placebo    | 12              | 13    | 4            | 10               | 83.3                 |
| ONCO-03   | traitement | 9               | 13    | 0            | 8                | 88.9                 |
+-----------+------------+-----------------+-------+--------------+------------------+----------------------+
8 lignes
```
<!-- /resultat -->

Lecture : dans chaque étude, on compare les bras. Un médicament bien toléré a un profil d'EI proche du placebo.

> Pourquoi `COUNT(DISTINCT p.id)` ? La jointure avec les EI **multiplie** les lignes des patients qui ont plusieurs EI (piège du module 4). `COUNT(DISTINCT)` compte chaque patient une seule fois.

### Exemple 4 — une vue construite sur une vue

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_synthese_etude AS
SELECT r.etude,
       SUM(r.objectif)    AS objectif,
       SUM(r.inclus)      AS inclus,
       ROUND(100 * SUM(r.inclus) / SUM(r.objectif), 1) AS atteinte_pct,
       SUM(r.echecs_screening) AS echecs_screening
FROM v_tableau_de_bord_recrutement r
GROUP BY r.etude;
```

```sql
SELECT * FROM v_synthese_etude ORDER BY atteinte_pct DESC;
```
<!-- resultat -->
```text
+-----------+----------+--------+--------------+------------------+
| etude     | objectif | inclus | atteinte_pct | echecs_screening |
+-----------+----------+--------+--------------+------------------+
| NEURO-04  | 30       | 30     | 100.0        | 2                |
| CARDIO-01 | 120      | 112    | 93.3         | 24               |
| DIAB-02   | 80       | 49     | 61.3         | 15               |
| ONCO-03   | 60       | 21     | 35.0         | 9                |
| DERM-05   | 100      | 0      | 0.0          | 0                |
+-----------+----------+--------+--------------+------------------+
5 lignes
```
<!-- /resultat -->

### Peut-on modifier des données à travers une vue ?

Oui, si la vue est **simple** : une seule table, pas d'agrégat, pas de `DISTINCT`, pas de `GROUP BY`, pas d'`UNION`. On parle de vue **modifiable** (*updatable view*). L'option `WITH CHECK OPTION` interdit alors d'insérer ou de modifier des lignes qui sortiraient de la vue :

```sql
CREATE VIEW v_centre_france AS
SELECT id, nom, ville, pays FROM centre WHERE pays = 'France'
WITH CHECK OPTION;

UPDATE v_centre_france SET ville = 'Tours Nord' WHERE id = 1;     -- ✅ modifie la table centre
INSERT INTO v_centre_france (nom, ville, pays)
VALUES ('Clinique Alpine', 'Lausanne', 'Suisse');                  -- ❌ refusé : hors de la vue
```

En pratique, on utilise les vues surtout **en lecture**.

---

## 6.4 Les filtres en détail : `LIKE`, `IN`, `IS NULL`, `BETWEEN`

Ces opérateurs ont été introduits au module 3 ; voici leurs subtilités, appliquées à nos vues.

### `LIKE` et `NOT LIKE`

| Motif | Correspond à | Exemple |
|---|---|---|
| `'A%'` | commence par A | `centre LIKE 'Clinique%'` |
| `'%A'` | finit par A | `code_patient LIKE '%-001'` |
| `'%A%'` | contient A | `centre LIKE '%Val%'` |
| `'_A%'` | A en 2ᵉ position | |
| `'V_'` | V + exactement 1 caractère | `type_visite LIKE 'V_'` |

```sql
SELECT DISTINCT centre FROM v_tableau_de_bord_recrutement WHERE centre LIKE 'Clinique%' ORDER BY centre;
```
<!-- resultat -->
```text
+--------------------------+
| centre                   |
+--------------------------+
| Clinique des Flandres    |
| Clinique du Léman        |
| Clinique du Val de Loire |
+--------------------------+
3 lignes
```
<!-- /resultat -->

```sql
SELECT DISTINCT centre FROM v_tableau_de_bord_recrutement WHERE centre NOT LIKE '%Clinique%' ORDER BY centre;
```
<!-- resultat -->
```text
+-----------------------------+
| centre                      |
+-----------------------------+
| Centre Hospitalier du Rhône |
| Centre Médical des Ardennes |
| CHU Atlantique              |
| Hôpital Saint-Roch          |
| Hospital del Sol            |
+-----------------------------+
5 lignes
```
<!-- /resultat -->

**Chercher un `%` ou un `_` littéral** : le caractère d'échappement `\` (ou `ESCAPE`) :

```sql
-- les codes qui contiennent vraiment un tiret bas
SELECT code FROM etude WHERE code LIKE '%\_%';
SELECT code FROM etude WHERE code LIKE '%!_%' ESCAPE '!';   -- forme standard
```

### `IN` et `NOT IN`

```sql
SELECT code_patient, etude, pays
FROM v_patient_detail
WHERE pays IN ('Suisse', 'Espagne')
  AND statut NOT IN ('échec de screening', 'terminé')
ORDER BY code_patient;
```
<!-- resultat:6 -->
```text
+-------------------+-----------+--------+
| code_patient      | etude     | pays   |
+-------------------+-----------+--------+
| CARDIO-01-C06-011 | CARDIO-01 | Suisse |
| CARDIO-01-C06-015 | CARDIO-01 | Suisse |
| CARDIO-01-C06-016 | CARDIO-01 | Suisse |
| CARDIO-01-C06-017 | CARDIO-01 | Suisse |
| CARDIO-01-C06-018 | CARDIO-01 | Suisse |
| CARDIO-01-C06-019 | CARDIO-01 | Suisse |
+-------------------+-----------+--------+
… 16 lignes au total (6 affichées)
```
<!-- /resultat -->

### `IS NULL` et `IS NOT NULL`

```sql
-- les patients encore suivis (inclus et non sortis)
SELECT etude, COUNT(*) AS en_cours
FROM v_patient_detail
WHERE date_inclusion IS NOT NULL
  AND date_sortie IS NULL
GROUP BY etude;
```
<!-- resultat -->
```text
+-----------+----------+
| etude     | en_cours |
+-----------+----------+
| CARDIO-01 | 33       |
| DIAB-02   | 26       |
| ONCO-03   | 15       |
+-----------+----------+
3 lignes
```
<!-- /resultat -->

### `BETWEEN` et `NOT BETWEEN`

```sql
SELECT code_patient, age, etude
FROM v_patient_detail
WHERE age BETWEEN 18 AND 30
ORDER BY age, code_patient;
```
<!-- resultat:6 -->
```text
+------------------+-----+----------+
| code_patient     | age | etude    |
+------------------+-----+----------+
| NEURO-04-C01-011 | 22  | NEURO-04 |
| NEURO-04-C02-001 | 22  | NEURO-04 |
| NEURO-04-C02-006 | 25  | NEURO-04 |
| NEURO-04-C01-009 | 27  | NEURO-04 |
| NEURO-04-C02-003 | 27  | NEURO-04 |
| NEURO-04-C02-009 | 27  | NEURO-04 |
+------------------+-----+----------+
… 11 lignes au total (6 affichées)
```
<!-- /resultat -->

```sql
SELECT etude, centre, atteinte_pct
FROM v_tableau_de_bord_recrutement
WHERE atteinte_pct NOT BETWEEN 50 AND 100
ORDER BY atteinte_pct DESC, centre;
```
<!-- resultat:20 -->
```text
+-----------+-----------------------------+--------------+
| etude     | centre                      | atteinte_pct |
+-----------+-----------------------------+--------------+
| CARDIO-01 | Clinique du Val de Loire    | 110.0        |
| CARDIO-01 | Hôpital Saint-Roch          | 104.0        |
| DIAB-02   | Hôpital Saint-Roch          | 45.0         |
| DIAB-02   | Hospital del Sol            | 40.0         |
| ONCO-03   | Centre Hospitalier du Rhône | 35.0         |
| ONCO-03   | Clinique du Léman           | 20.0         |
| DERM-05   | Centre Médical des Ardennes | 0.0          |
| DERM-05   | Clinique du Val de Loire    | 0.0          |
+-----------+-----------------------------+--------------+
8 lignes
```
<!-- /resultat -->

### Récapitulatif

```
  Je cherche…                                     J'écris…
  ─────────────────────────────────────────────   ───────────────────────────────
  une valeur exacte                               col = 'x'
  une valeur parmi une liste                      col IN ('x', 'y', 'z')
  un intervalle (bornes incluses)                 col BETWEEN a AND b
  un morceau de texte                             col LIKE '%x%'
  une valeur absente                              col IS NULL
  le contraire de tout cela                       NOT IN / NOT BETWEEN / NOT LIKE / IS NOT NULL
```

---

## À vous

👉 Exercices : [`exercices/06-vues.md`](../exercices/06-vues.md)

---

## Pièges

- **Une vue n'est pas une copie** : si les données changent, la vue change. C'est voulu ; si vous avez besoin d'une photo figée (archive mensuelle), utilisez `CREATE TABLE … AS SELECT`.
- **`ORDER BY` dans une vue** : autorisé en MySQL mais inutile (l'ordre n'est pas garanti quand on interroge la vue avec d'autres clauses). Triez dans la requête qui **utilise** la vue.
- **Noms de colonnes** : chaque colonne d'une vue doit avoir un nom unique → donnez des **alias** aux expressions (`COUNT(*) AS nb`) et aux colonnes homonymes (`e.code AS etude`, `c.nom AS centre`).
- **`SELECT *` dans une vue** : en MySQL, la liste des colonnes est figée à la création ; une colonne ajoutée ensuite à la table n'apparaît pas dans la vue.
- **Vue sur vue sur vue** : pratique, mais les performances peuvent se dégrader et le débogage devient difficile. Deux niveaux suffisent généralement.
- **Supprimer une table utilisée par une vue** : la vue devient invalide (erreur à son prochain appel).
- **`NOT IN` et NULL** (rappel du module 3) : si la liste contient un NULL, `NOT IN` ne renvoie rien.

> ### ⚖️ Standard vs MySQL
> | Besoin | SQL standard | MySQL |
> |---|---|---|
> | Créer ou remplacer | `CREATE VIEW` (+ `DROP` avant) ; `CREATE OR REPLACE` selon les SGBD | `CREATE OR REPLACE VIEW` |
> | Option de vérification | `WITH CHECK OPTION` | idem (`WITH [CASCADED\|LOCAL] CHECK OPTION`) |
> | Lister les vues | `information_schema.views` | aussi `SHOW FULL TABLES WHERE Table_type = 'VIEW'` |
> | Voir la définition | `information_schema.views.view_definition` | `SHOW CREATE VIEW v` |
> | Vue matérialisée (stockée) | `CREATE MATERIALIZED VIEW` (PostgreSQL, Oracle) | **n'existe pas** → table + mise à jour manuelle |
> | Casse dans `LIKE` | sensible à la casse en général | insensible avec la collation par défaut (`_ci`) |

---

## Quiz

1. Que contient physiquement une vue ?
   - a) Une copie des données au moment de sa création
   - b) La requête qui la définit (pas de données)
   - c) Un index sur les tables sources
   - d) Une sauvegarde de la base

2. Quelle instruction modifie la définition d'une vue existante en MySQL ?
   - a) `ALTER TABLE v …`
   - b) `UPDATE VIEW v …`
   - c) `CREATE OR REPLACE VIEW v AS …`
   - d) `MODIFY VIEW v …`

3. Une vue contenant un `GROUP BY` est-elle modifiable (`UPDATE` à travers la vue) ?
   - a) Oui, toujours  - b) Non  - c) Oui, avec `WITH CHECK OPTION`  - d) Seulement en SQL standard

4. Quel filtre trouve les codes de visite composés de « V » suivi d'un seul caractère ?
   - a) `LIKE 'V%'`  - b) `LIKE 'V_'`  - c) `= 'V?'`  - d) `IN ('V')`

5. `WHERE atteinte_pct NOT BETWEEN 50 AND 100` garde :
   - a) les valeurs de 50 à 100
   - b) les valeurs strictement inférieures à 50 ou strictement supérieures à 100
   - c) les valeurs inférieures ou égales à 50 ou supérieures ou égales à 100
   - d) les valeurs NULL

<details>
<summary>Réponses</summary>

1. **b**. 2. **c**. 3. **b**. 4. **b**. 5. **b** — et pas les NULL, qui ne sont ni dedans ni dehors.
</details>

---

## Côté métier

Les vues sont le pont entre la base et vos outils habituels :
- Dans **Excel** : *Données → Obtenir des données → À partir d'une base de données → MySQL* (ou via un pilote ODBC), puis choisir la vue. Un clic sur **Actualiser** recharge les chiffres à jour.
- Dans **Power BI** : même principe, chaque vue devient une table du modèle.
- Pour vos collègues : « interrogez `v_tableau_de_bord_recrutement` » est plus simple (et plus sûr) que de leur transmettre une requête de 30 lignes.

Conseil d'organisation : préfixez vos vues (`v_`), regroupez les indicateurs d'un même thème, et **documentez** dans un commentaire de tête ce que calcule chaque colonne.

---

⬅️ [Module 5](05-mise-a-jour.md) · ➡️ [Module 7 — Certification et bonus](07-certification.md)
