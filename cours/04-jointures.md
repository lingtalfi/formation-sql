# Module 4 — Requêtes complexes multi-tables

> **Objectif** : combiner les données de plusieurs tables avec les jointures (`INNER`, `LEFT`, `RIGHT`, `FULL`, auto-jointure, `CROSS`), les alias, `UNION`, les tables temporaires et les CTE.
> **Durée indicative** : 8 h

---

## 4.1 Pourquoi joindre ?

### Concept

Une base bien conçue range chaque information **une seule fois**, dans sa table (module 2). Le patient connaît l'**identifiant** de son étude (`etude_id = 1`), mais pas son code (`CARDIO-01`). Pour afficher les deux ensemble, on **joint** les tables : on met bout à bout les lignes qui se correspondent, grâce à la condition **clé étrangère = clé primaire**.

### Visuel — une jointure

```
   patient                                      etude
  ┌────┬───────────────────┬──────────┐        ┌────┬───────────┬───────┐
  │ id │ code_patient      │ etude_id │        │ id │ code      │ phase │
  ├────┼───────────────────┼──────────┤        ├────┼───────────┼───────┤
  │ 1  │ CARDIO-01-C01-001 │    1  ───┼───────►│ 1  │ CARDIO-01 │ III   │
  │ 137│ DIAB-02-C01-001   │    2  ───┼───────►│ 2  │ DIAB-02   │ II    │
  └────┴───────────────────┴──────────┘        └────┴───────────┴───────┘

             patient JOIN etude ON patient.etude_id = etude.id

  ┌────┬───────────────────┬──────────┬────┬───────────┬───────┐
  │ id │ code_patient      │ etude_id │ id │ code      │ phase │
  ├────┼───────────────────┼──────────┼────┼───────────┼───────┤
  │ 1  │ CARDIO-01-C01-001 │ 1        │ 1  │ CARDIO-01 │ III   │
  │ 137│ DIAB-02-C01-001   │ 2        │ 2  │ DIAB-02   │ II    │
  └────┴───────────────────┴──────────┴────┴───────────┴───────┘
        ◄──── colonnes de patient ────►◄── colonnes de etude ──►
```

### Ce qui se passe sans condition de jointure

Sans `ON`, chaque ligne de la première table est associée à **chaque** ligne de la seconde : c'est le **produit cartésien**. 262 patients × 5 études = 1 310 lignes, dont l'immense majorité n'a aucun sens.

```sql
SELECT COUNT(*) AS nb_lignes FROM patient CROSS JOIN etude;
```
<!-- resultat -->
```text
+-----------+
| nb_lignes |
+-----------+
| 1310      |
+-----------+
1 ligne
```
<!-- /resultat -->

> 💡 Une jointure = un produit cartésien **filtré** par la condition `ON`. Si votre résultat a soudain des milliers de lignes de trop, une condition de jointure manque ou est fausse.

---

## 4.2 `INNER JOIN` : les lignes qui se correspondent

### Concept

```
SELECT …
FROM table_a
INNER JOIN table_b ON table_a.cle_etrangere = table_b.cle_primaire
```

`INNER JOIN` (ou simplement `JOIN`) ne garde que les lignes qui ont une correspondance **des deux côtés**.

### Visuel

```
        table A          table B
       ┌───────┐       ┌───────┐
       │       │███████│       │       INNER JOIN = l'intersection :
       │   A   │███████│   B   │       les lignes de A qui ont une
       │       │███████│       │       correspondance dans B (et réciproquement)
       └───────┘       └───────┘
```

### Exemples

**Le code de l'étude de chaque patient** :

```sql
SELECT patient.code_patient, etude.code, etude.phase
FROM patient
INNER JOIN etude ON patient.etude_id = etude.id;
```
<!-- resultat:4 -->
```text
+-------------------+-----------+-------+
| code_patient      | code      | phase |
+-------------------+-----------+-------+
| CARDIO-01-C01-001 | CARDIO-01 | III   |
| CARDIO-01-C01-002 | CARDIO-01 | III   |
| CARDIO-01-C01-003 | CARDIO-01 | III   |
| CARDIO-01-C01-004 | CARDIO-01 | III   |
+-------------------+-----------+-------+
… 262 lignes au total (4 affichées)
```
<!-- /resultat -->

**Avec des alias de table** (plus court, et indispensable dès qu'on a plusieurs tables) :

```sql
SELECT p.code_patient, e.code AS etude, c.nom AS centre, c.ville
FROM patient p
JOIN etude  e ON p.etude_id  = e.id
JOIN centre c ON p.centre_id = c.id
WHERE p.date_inclusion IS NOT NULL;
```
<!-- resultat:4 -->
```text
+-------------------+-----------+--------------------------+-------+
| code_patient      | etude     | centre                   | ville |
+-------------------+-----------+--------------------------+-------+
| CARDIO-01-C01-001 | CARDIO-01 | Clinique du Val de Loire | Tours |
| CARDIO-01-C01-002 | CARDIO-01 | Clinique du Val de Loire | Tours |
| CARDIO-01-C01-003 | CARDIO-01 | Clinique du Val de Loire | Tours |
| CARDIO-01-C01-004 | CARDIO-01 | Clinique du Val de Loire | Tours |
+-------------------+-----------+--------------------------+-------+
… 212 lignes au total (4 affichées)
```
<!-- /resultat -->

Chaque `JOIN` ajoute une table à la « chaîne » :

```
   patient p ──(p.etude_id = e.id)──► etude e
       │
       └─────(p.centre_id = c.id)──► centre c
```

**Jointure + agrégation** — le nombre d'inclus par étude, avec le **code** de l'étude :

```sql
SELECT e.code, COUNT(p.date_inclusion) AS inclus, e.objectif_inclusions AS objectif
FROM etude e
JOIN patient p ON p.etude_id = e.id
GROUP BY e.code, e.objectif_inclusions
ORDER BY e.code;
```
<!-- resultat -->
```text
+-----------+--------+----------+
| code      | inclus | objectif |
+-----------+--------+----------+
| CARDIO-01 | 112    | 120      |
| DIAB-02   | 49     | 80       |
| NEURO-04  | 30     | 30       |
| ONCO-03   | 21     | 60       |
+-----------+--------+----------+
4 lignes
```
<!-- /resultat -->

Remarquez que **DERM-05 n'apparaît pas** : elle n'a aucun patient, donc aucune correspondance → `INNER JOIN` l'écarte. (Solution en 4.3.)

**Quatre tables** — l'évolution de la tension (PAS) des patients de CARDIO-01, par bras et par visite :

```
  mesure m ──► visite v ──► patient p ──► etude e
```

```sql
SELECT p.bras, v.type_visite, ROUND(AVG(m.valeur), 1) AS pas_moyenne, COUNT(*) AS nb_mesures
FROM mesure  m
JOIN visite  v ON m.visite_id  = v.id
JOIN patient p ON v.patient_id = p.id
JOIN etude   e ON p.etude_id   = e.id
WHERE e.code = 'CARDIO-01'
  AND m.parametre = 'pas'
GROUP BY p.bras, v.type_visite
ORDER BY p.bras, v.type_visite;
```
<!-- resultat:20 -->
```text
+------------+-------------+-------------+------------+
| bras       | type_visite | pas_moyenne | nb_mesures |
+------------+-------------+-------------+------------+
| placebo    | V0          | 149.6       | 60         |
| placebo    | V1          | 150.4       | 53         |
| placebo    | V2          | 148.9       | 54         |
| placebo    | V3          | 148.6       | 49         |
| placebo    | V4          | 147.6       | 52         |
| placebo    | V5          | 148.0       | 49         |
| placebo    | V6          | 146.7       | 33         |
| traitement | V0          | 150.7       | 52         |
| traitement | V1          | 149.3       | 50         |
| traitement | V2          | 149.5       | 44         |
| traitement | V3          | 148.5       | 48         |
| traitement | V4          | 146.5       | 45         |
| traitement | V5          | 141.9       | 44         |
| traitement | V6          | 136.6       | 30         |
+------------+-------------+-------------+------------+
14 lignes
```
<!-- /resultat -->

On voit l'effet du médicament : la tension baisse nettement plus dans le bras `traitement` que dans le bras `placebo`.

**Les EI graves avec le contexte complet** :

```sql
SELECT e.code AS etude, c.ville, p.code_patient, p.bras, ei.terme, ei.grade, ei.date_survenue
FROM evenement_indesirable ei
JOIN patient p ON ei.patient_id = p.id
JOIN etude   e ON p.etude_id    = e.id
JOIN centre  c ON p.centre_id   = c.id
WHERE ei.grave = TRUE
ORDER BY ei.date_survenue DESC
LIMIT 6;
```
<!-- resultat -->
```text
+-----------+-------------+-------------------+------------+--------------------+-------+---------------+
| etude     | ville       | code_patient      | bras       | terme              | grade | date_survenue |
+-----------+-------------+-------------------+------------+--------------------+-------+---------------+
| CARDIO-01 | Genève      | CARDIO-01-C06-016 | traitement | Vertiges           | 4     | 2026-06-18    |
| ONCO-03   | Lyon        | ONCO-03-C04-008   | placebo    | Anémie             | 4     | 2026-06-11    |
| DIAB-02   | Lille       | DIAB-02-C05-008   | traitement | Douleur abdominale | 3     | 2026-05-31    |
| CARDIO-01 | Nantes      | CARDIO-01-C02-025 | placebo    | Céphalées          | 3     | 2026-04-09    |
| CARDIO-01 | Montpellier | CARDIO-01-C03-028 | traitement | Vertiges           | 3     | 2026-03-03    |
| DIAB-02   | Tours       | DIAB-02-C01-008   | traitement | Diarrhée           | 3     | 2026-02-21    |
+-----------+-------------+-------------------+------------+--------------------+-------+---------------+
6 lignes
```
<!-- /resultat -->

**Jointure sur une clé composée** — le nom de l'investigateur principal de chaque participation :

```sql
SELECT e.code AS etude, c.nom AS centre,
       CONCAT(i.prenom, ' ', i.nom) AS investigateur_principal,
       ec.date_ouverture
FROM etude_centre ec
JOIN etude         e ON ec.etude_id  = e.id
JOIN centre        c ON ec.centre_id = c.id
JOIN investigateur i ON ec.investigateur_principal_id = i.id
ORDER BY e.code, c.nom;
```
<!-- resultat:20 -->
```text
+-----------+-----------------------------+-------------------------+----------------+
| etude     | centre                      | investigateur_principal | date_ouverture |
+-----------+-----------------------------+-------------------------+----------------+
| CARDIO-01 | CHU Atlantique              | Thomas Moreau           | 2024-04-01     |
| CARDIO-01 | Centre Hospitalier du Rhône | Manon Girard            | 2024-06-01     |
| CARDIO-01 | Clinique du Léman           | Anna Müller             | 2024-09-01     |
| CARDIO-01 | Clinique du Val de Loire    | Claire Martin           | 2024-03-15     |
| CARDIO-01 | Hôpital Saint-Roch          | Antoine Garcia          | 2024-05-10     |
| DERM-05   | Centre Médical des Ardennes | Marc Dubois             | NULL           |
| DERM-05   | Clinique du Val de Loire    | Lucas Robert            | NULL           |
| DIAB-02   | Clinique des Flandres       | Emma Lambert            | 2025-02-15     |
| DIAB-02   | Clinique du Val de Loire    | Hugo Bernard            | 2025-02-01     |
| DIAB-02   | Hospital del Sol            | Carmen López            | 2025-05-01     |
| DIAB-02   | Hôpital Saint-Roch          | Léa Roux                | 2025-03-01     |
| NEURO-04  | CHU Atlantique              | Camille Lefèvre         | 2023-02-01     |
| NEURO-04  | Clinique du Val de Loire    | Inès Petit              | 2023-01-20     |
| ONCO-03   | CHU Atlantique              | Sophie Durand           | 2025-07-01     |
| ONCO-03   | Centre Hospitalier du Rhône | Julien Fournier         | 2025-08-15     |
| ONCO-03   | Clinique du Léman           | Nicolas Favre           | 2025-10-01     |
+-----------+-----------------------------+-------------------------+----------------+
16 lignes
```
<!-- /resultat -->

### L'ancienne syntaxe (à savoir lire)

On rencontre encore des jointures écrites dans le `WHERE` :

```sql
SELECT p.code_patient, e.code
FROM patient p, etude e          -- produit cartésien…
WHERE p.etude_id = e.id;         -- …filtré dans le WHERE
```

C'est équivalent à `INNER JOIN`, mais moins lisible (on mélange conditions de jointure et filtres) et plus risqué (oublier une condition = produit cartésien). **Préférez `JOIN … ON`.**

---

## 4.3 `LEFT JOIN` / `RIGHT JOIN` : garder les lignes sans correspondance

### Concept

`LEFT [OUTER] JOIN` garde **toutes les lignes de la table de gauche**, même sans correspondance à droite ; les colonnes de droite sont alors remplies de **NULL**.

```
SELECT …
FROM table_gauche g
LEFT JOIN table_droite d ON g.id = d.gauche_id
```

### Visuel

```
        table A          table B
       ┌───────┐       ┌───────┐
       │███████│███████│       │       LEFT JOIN = tout A
       │███A███│███████│   B   │       + ce qui correspond dans B
       │███████│███████│       │       (NULL quand rien ne correspond)
       └───────┘       └───────┘

 centre (gauche)          patient (droite)            Résultat LEFT JOIN
 ┌────┬─────────┐        ┌────┬───────────┐        ┌─────────┬────────────┐
 │ id │ ville   │        │ id │ centre_id │        │ ville   │ patient.id │
 ├────┼─────────┤        ├────┼───────────┤        ├─────────┼────────────┤
 │ 1  │ Tours   │◄──────►│ 1  │ 1         │   →    │ Tours   │ 1          │
 │ 2  │ Nantes  │◄──────►│ 41 │ 2         │        │ Nantes  │ 41         │
 │ 8  │ Liège   │   ✗    │    │           │        │ Liège   │ NULL  ◄── conservé quand même
 └────┴─────────┘        └────┴───────────┘        └─────────┴────────────┘
```

### Exemples

**Toutes les études, avec leur nombre d'inclus (y compris 0)** :

```sql
SELECT e.code, COUNT(p.date_inclusion) AS inclus, e.objectif_inclusions AS objectif
FROM etude e
LEFT JOIN patient p ON p.etude_id = e.id
GROUP BY e.code, e.objectif_inclusions
ORDER BY e.code;
```
<!-- resultat -->
```text
+-----------+--------+----------+
| code      | inclus | objectif |
+-----------+--------+----------+
| CARDIO-01 | 112    | 120      |
| DERM-05   | 0      | 100      |
| DIAB-02   | 49     | 80       |
| NEURO-04  | 30     | 30       |
| ONCO-03   | 21     | 60       |
+-----------+--------+----------+
5 lignes
```
<!-- /resultat -->

DERM-05 est maintenant présente, avec 0 inclus.

**Tous les centres et leur nombre de patients screenés** — attention à ce qu'on compte :

```sql
SELECT c.nom,
       COUNT(*)    AS faux_compte,    -- compte aussi la ligne « vide » de Liège !
       COUNT(p.id) AS nb_patients     -- ne compte que les vrais patients
FROM centre c
LEFT JOIN patient p ON p.centre_id = c.id
GROUP BY c.nom
ORDER BY nb_patients DESC;
```
<!-- resultat -->
```text
+-----------------------------+-------------+-------------+
| nom                         | faux_compte | nb_patients |
+-----------------------------+-------------+-------------+
| Clinique du Val de Loire    | 77          | 77          |
| CHU Atlantique              | 55          | 55          |
| Hôpital Saint-Roch          | 43          | 43          |
| Centre Hospitalier du Rhône | 28          | 28          |
| Clinique du Léman           | 27          | 27          |
| Clinique des Flandres       | 24          | 24          |
| Hospital del Sol            | 8           | 8           |
| Centre Médical des Ardennes | 1           | 0           |
+-----------------------------+-------------+-------------+
8 lignes
```
<!-- /resultat -->

> ⚠️ Avec un `LEFT JOIN`, comptez une colonne **de la table de droite** (`COUNT(p.id)`), jamais `COUNT(*)`.

**Trouver ce qui manque : `LEFT JOIN … WHERE droite.id IS NULL`** — les investigateurs qui ne sont investigateur principal d'aucune étude :

```sql
SELECT i.nom, i.prenom, i.specialite
FROM investigateur i
LEFT JOIN etude_centre ec ON ec.investigateur_principal_id = i.id
WHERE ec.etude_id IS NULL;
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

```
   investigateur   LEFT JOIN etude_centre          WHERE ec.etude_id IS NULL
  ┌──────────┐    ┌──────────┬──────────┐        ┌──────────┐
  │ Martin   │ ─► │ Martin   │ CARDIO-01│        │          │
  │ Bonnet   │ ─► │ Bonnet   │ NULL     │  ───►  │ Bonnet   │  ← ceux qui n'ont
  │ Sánchez  │ ─► │ Sánchez  │ NULL     │        │ Sánchez  │    PAS de correspondance
  └──────────┘    └──────────┴──────────┘        └──────────┘
```

C'est l'équivalent en jointure du `NOT EXISTS` vu au module 3.

**Les patients inclus et leurs EI, y compris ceux qui n'en ont pas** :

```sql
SELECT p.code_patient, ei.terme, ei.grade
FROM patient p
LEFT JOIN evenement_indesirable ei ON ei.patient_id = p.id
WHERE p.date_inclusion IS NOT NULL
ORDER BY p.code_patient
LIMIT 8;
```
<!-- resultat -->
```text
+-------------------+---------------------+-------+
| code_patient      | terme               | grade |
+-------------------+---------------------+-------+
| CARDIO-01-C01-001 | Œdème des chevilles | 2     |
| CARDIO-01-C01-002 | NULL                | NULL  |
| CARDIO-01-C01-003 | NULL                | NULL  |
| CARDIO-01-C01-004 | NULL                | NULL  |
| CARDIO-01-C01-006 | Nausées             | 2     |
| CARDIO-01-C01-007 | NULL                | NULL  |
| CARDIO-01-C01-009 | NULL                | NULL  |
| CARDIO-01-C01-010 | Céphalées           | 1     |
+-------------------+---------------------+-------+
8 lignes
```
<!-- /resultat -->

### Le piège : condition dans `ON` ou dans `WHERE` ?

On veut **tous les centres** avec leur nombre d'EI **graves**.

```sql
-- ❌ le filtre dans le WHERE supprime les centres sans EI grave (le LEFT JOIN redevient un INNER JOIN)
SELECT c.nom, COUNT(ei.id) AS nb_ei_graves
FROM centre c
LEFT JOIN patient p                ON p.centre_id   = c.id
LEFT JOIN evenement_indesirable ei ON ei.patient_id = p.id
WHERE ei.grave = TRUE
GROUP BY c.nom
ORDER BY nb_ei_graves DESC;
```
<!-- resultat -->
```text
+-----------------------------+--------------+
| nom                         | nb_ei_graves |
+-----------------------------+--------------+
| CHU Atlantique              | 8            |
| Clinique du Val de Loire    | 7            |
| Hôpital Saint-Roch          | 4            |
| Clinique des Flandres       | 3            |
| Clinique du Léman           | 2            |
| Centre Hospitalier du Rhône | 2            |
+-----------------------------+--------------+
6 lignes
```
<!-- /resultat -->

```sql
-- ✅ le filtre dans le ON : il s'applique AVANT de compléter avec des NULL
SELECT c.nom, COUNT(ei.id) AS nb_ei_graves
FROM centre c
LEFT JOIN patient p                ON p.centre_id   = c.id
LEFT JOIN evenement_indesirable ei ON ei.patient_id = p.id AND ei.grave = TRUE
GROUP BY c.nom
ORDER BY nb_ei_graves DESC;
```
<!-- resultat -->
```text
+-----------------------------+--------------+
| nom                         | nb_ei_graves |
+-----------------------------+--------------+
| CHU Atlantique              | 8            |
| Clinique du Val de Loire    | 7            |
| Hôpital Saint-Roch          | 4            |
| Clinique des Flandres       | 3            |
| Clinique du Léman           | 2            |
| Centre Hospitalier du Rhône | 2            |
| Hospital del Sol            | 0            |
| Centre Médical des Ardennes | 0            |
+-----------------------------+--------------+
8 lignes
```
<!-- /resultat -->

> Règle : dans un `LEFT JOIN`, une condition sur la table **de droite** se place dans le **`ON`** ; une condition sur la table **de gauche** se place dans le **`WHERE`**.

### `RIGHT JOIN`

`RIGHT JOIN` est le miroir : il garde toutes les lignes de la table **de droite**. `A RIGHT JOIN B` = `B LEFT JOIN A`. En pratique, on écrit presque toujours des `LEFT JOIN` (on lit de gauche à droite, en partant de la table « principale »).

```sql
-- équivalent du premier exemple de LEFT JOIN
SELECT e.code, COUNT(p.date_inclusion) AS inclus
FROM patient p
RIGHT JOIN etude e ON p.etude_id = e.id
GROUP BY e.code
ORDER BY e.code;
```
<!-- resultat -->
```text
+-----------+--------+
| code      | inclus |
+-----------+--------+
| CARDIO-01 | 112    |
| DERM-05   | 0      |
| DIAB-02   | 49     |
| NEURO-04  | 30     |
| ONCO-03   | 21     |
+-----------+--------+
5 lignes
```
<!-- /resultat -->

---

## 4.4 `FULL OUTER JOIN` (standard) et son émulation en MySQL

### Concept

`FULL OUTER JOIN` garde **toutes les lignes des deux tables** ; NULL de chaque côté quand il n'y a pas de correspondance.

```
        table A          table B
       ┌───────┐       ┌───────┐
       │███████│███████│███████│       FULL OUTER JOIN = tout A + tout B
       │███A███│███████│███B███│
       │███████│███████│███████│
       └───────┘       └───────┘
```

**MySQL ne connaît pas `FULL OUTER JOIN`** (c'est l'une des questions classiques de l'examen sur le SQL standard). On l'émule avec l'union d'un `LEFT JOIN` et d'un `RIGHT JOIN` :

```
  A FULL OUTER JOIN B   ≡   (A LEFT JOIN B)  UNION  (A RIGHT JOIN B)
```

### Exemple — comparer deux séries mensuelles

On veut comparer, mois par mois en 2025, les inclusions de DIAB-02 et d'ONCO-03. Certains mois n'ont d'inclusion que dans une des deux études.

```sql
-- SQL STANDARD (PostgreSQL, SQL Server, Oracle…) — refusé par MySQL
SELECT COALESCE(d.mois, o.mois) AS mois, d.nb AS diab, o.nb AS onco
FROM      (SELECT DATE_FORMAT(date_inclusion, '%Y-%m') AS mois, COUNT(*) AS nb
             FROM patient WHERE etude_id = 2 AND YEAR(date_inclusion) = 2025 GROUP BY mois) d
FULL OUTER JOIN
          (SELECT DATE_FORMAT(date_inclusion, '%Y-%m') AS mois, COUNT(*) AS nb
             FROM patient WHERE etude_id = 3 AND YEAR(date_inclusion) = 2025 GROUP BY mois) o
       ON d.mois = o.mois
ORDER BY mois;
```

```sql
-- ÉMULATION MySQL : LEFT JOIN  UNION  RIGHT JOIN
SELECT d.mois, d.nb AS diab, o.nb AS onco
FROM      (SELECT DATE_FORMAT(date_inclusion, '%Y-%m') AS mois, COUNT(*) AS nb
             FROM patient WHERE etude_id = 2 AND YEAR(date_inclusion) = 2025 GROUP BY mois) d
LEFT JOIN (SELECT DATE_FORMAT(date_inclusion, '%Y-%m') AS mois, COUNT(*) AS nb
             FROM patient WHERE etude_id = 3 AND YEAR(date_inclusion) = 2025 GROUP BY mois) o
       ON d.mois = o.mois
UNION
SELECT o.mois, d.nb AS diab, o.nb AS onco
FROM      (SELECT DATE_FORMAT(date_inclusion, '%Y-%m') AS mois, COUNT(*) AS nb
             FROM patient WHERE etude_id = 2 AND YEAR(date_inclusion) = 2025 GROUP BY mois) d
RIGHT JOIN (SELECT DATE_FORMAT(date_inclusion, '%Y-%m') AS mois, COUNT(*) AS nb
             FROM patient WHERE etude_id = 3 AND YEAR(date_inclusion) = 2025 GROUP BY mois) o
       ON d.mois = o.mois
ORDER BY mois;
```
<!-- resultat:15 -->
```text
ERREUR DE GÉNÉRATION : 1st ORDER BY term does not match any column in the result set
```
<!-- /resultat -->

Les NULL montrent les mois sans inclusion dans l'une des études. (La répétition des sous-requêtes est pénible : les **CTE** de la section 4.8 règlent ce problème.)

---

## 4.5 Auto-jointure et `CROSS JOIN`

### L'auto-jointure : joindre une table avec elle-même

Chaque investigateur peut avoir un **superviseur**, qui est… un autre investigateur. Pour afficher les deux noms côte à côte, on utilise **deux fois** la table, avec **deux alias** différents.

```
     investigateur i (« le subordonné »)          investigateur s (« le superviseur »)
   ┌────┬─────────┬────────────────┐            ┌────┬─────────┐
   │ id │ nom     │ superviseur_id │            │ id │ nom     │
   ├────┼─────────┼────────────────┤            ├────┼─────────┤
   │ 1  │ Martin  │ NULL           │      ┌────►│ 1  │ Martin  │
   │ 2  │ Bernard │ 1  ────────────┼──────┘     │ …  │ …       │
   └────┴─────────┴────────────────┘            └────┴─────────┘
```

```sql
SELECT CONCAT(i.prenom, ' ', i.nom) AS investigateur,
       CONCAT(s.prenom, ' ', s.nom) AS superviseur
FROM investigateur i
LEFT JOIN investigateur s ON i.superviseur_id = s.id
ORDER BY i.id;
```
<!-- resultat:20 -->
```text
+-----------------+-----------------+
| investigateur   | superviseur     |
+-----------------+-----------------+
| Claire Martin   | NULL            |
| Hugo Bernard    | Claire Martin   |
| Inès Petit      | Claire Martin   |
| Lucas Robert    | Claire Martin   |
| Sophie Durand   | NULL            |
| Thomas Moreau   | Sophie Durand   |
| Camille Lefèvre | Sophie Durand   |
| Antoine Garcia  | NULL            |
| Léa Roux        | Antoine Garcia  |
| Julien Fournier | NULL            |
| Manon Girard    | Julien Fournier |
| Paul Bonnet     | Julien Fournier |
| Emma Lambert    | NULL            |
| Nicolas Favre   | NULL            |
| Anna Müller     | Nicolas Favre   |
| Carmen López    | NULL            |
| Javier Sánchez  | Carmen López    |
| Marc Dubois     | NULL            |
+-----------------+-----------------+
18 lignes
```
<!-- /resultat -->

Le `LEFT JOIN` conserve les chefs de service (qui n'ont pas de superviseur → NULL).

**Combien de personnes chaque chef supervise-t-il ?**

```sql
SELECT CONCAT(s.prenom, ' ', s.nom) AS superviseur, COUNT(i.id) AS nb_supervises
FROM investigateur s
JOIN investigateur i ON i.superviseur_id = s.id
GROUP BY s.id, s.prenom, s.nom
ORDER BY nb_supervises DESC, superviseur;
```
<!-- resultat -->
```text
+-----------------+---------------+
| superviseur     | nb_supervises |
+-----------------+---------------+
| Claire Martin   | 3             |
| Julien Fournier | 2             |
| Sophie Durand   | 2             |
| Antoine Garcia  | 1             |
| Carmen López    | 1             |
| Nicolas Favre   | 1             |
+-----------------+---------------+
6 lignes
```
<!-- /resultat -->

### `CROSS JOIN` : toutes les combinaisons

Le produit cartésien est parfois **voulu** : pour construire une grille de toutes les combinaisons possibles, puis voir lesquelles existent.

**La matrice études × centres** :

```sql
SELECT e.code, c.ville,
       CASE WHEN ec.etude_id IS NULL THEN '' ELSE 'X' END AS participe
FROM etude e
CROSS JOIN centre c
LEFT JOIN etude_centre ec ON ec.etude_id = e.id AND ec.centre_id = c.id
WHERE e.code IN ('CARDIO-01', 'DIAB-02')
ORDER BY e.code, c.id;
```
<!-- resultat:20 -->
```text
+-----------+-------------+-----------+
| code      | ville       | participe |
+-----------+-------------+-----------+
| CARDIO-01 | Tours       | X         |
| CARDIO-01 | Nantes      | X         |
| CARDIO-01 | Montpellier | X         |
| CARDIO-01 | Lyon        | X         |
| CARDIO-01 | Lille       |           |
| CARDIO-01 | Genève      | X         |
| CARDIO-01 | Valencia    |           |
| CARDIO-01 | Liège       |           |
| DIAB-02   | Tours       | X         |
| DIAB-02   | Nantes      |           |
| DIAB-02   | Montpellier | X         |
| DIAB-02   | Lyon        |           |
| DIAB-02   | Lille       | X         |
| DIAB-02   | Genève      |           |
| DIAB-02   | Valencia    | X         |
| DIAB-02   | Liège       |           |
+-----------+-------------+-----------+
16 lignes
```
<!-- /resultat -->

---

## 4.6 Alias de tables, `UNION` et `UNION ALL`

### Les alias de tables

```sql
FROM patient AS p          -- ou simplement : FROM patient p
JOIN etude e ON p.etude_id = e.id
```

- Ils **raccourcissent** l'écriture.
- Ils sont **obligatoires** pour joindre une table avec elle-même.
- Ils lèvent les **ambiguïtés** : `id` existe dans les deux tables, il faut écrire `p.id` ou `e.id`.

```sql
-- ❌ ERROR 1052 (23000): Column 'id' in field list is ambiguous
SELECT id, code FROM patient p JOIN etude e ON p.etude_id = e.id;
```

> 💡 Bonne pratique : dès qu'il y a une jointure, **préfixez toutes les colonnes** par leur alias, même celles qui ne sont pas ambiguës.

### `UNION` : empiler des résultats

Une jointure met des tables **côte à côte** (plus de colonnes). `UNION` met des résultats **l'un sous l'autre** (plus de lignes).

```
   JOIN : côte à côte                     UNION : l'un sous l'autre
  ┌─────┬─────┐  ┌─────┬─────┐          ┌───────────┐
  │  A  │     │ +│  B  │     │          │ requête 1 │
  └─────┴─────┘  └─────┴─────┘          ├───────────┤
  ┌─────┬─────┬─────┬─────┐             │ requête 2 │
  │  A        │  B        │             └───────────┘
  └─────┴─────┴─────┴─────┘
```

Règles : même **nombre de colonnes**, types **compatibles**, noms de colonnes pris dans la **première** requête, `ORDER BY` unique **à la fin**.

| | Doublons | Vitesse |
|---|---|---|
| `UNION` | supprimés | plus lent (il faut dédoublonner) |
| `UNION ALL` | conservés | plus rapide |

**La chronologie d'un patient** — visites réalisées et EI dans une seule liste :

```sql
SELECT v.date_realisee AS date, CONCAT('Visite ', v.type_visite) AS evenement
FROM visite v
WHERE v.patient_id = 16 AND v.date_realisee IS NOT NULL
UNION ALL
SELECT ei.date_survenue, CONCAT('EI : ', ei.terme, ' (grade ', ei.grade, ')')
FROM evenement_indesirable ei
WHERE ei.patient_id = 16
ORDER BY date;
```
<!-- resultat:20 -->
```text
+------------+-----------------------------------+
| date       | evenement                         |
+------------+-----------------------------------+
| 2025-04-02 | Visite V0                         |
| 2025-04-17 | Visite V1                         |
| 2025-04-23 | EI : Fatigue (grade 1)            |
| 2025-05-04 | Visite V2                         |
| 2025-06-01 | Visite V3                         |
| 2025-06-09 | EI : Douleur abdominale (grade 4) |
| 2025-06-26 | Visite V4                         |
+------------+-----------------------------------+
7 lignes
```
<!-- /resultat -->

**`UNION` qui dédoublonne** — toutes les villes où l'on trouve un centre ou un investigateur principal (la même ville n'apparaît qu'une fois) :

```sql
SELECT c.ville FROM centre c
UNION
SELECT c.ville
FROM etude_centre ec
JOIN investigateur i ON ec.investigateur_principal_id = i.id
JOIN centre c        ON i.centre_id = c.id
ORDER BY ville;
```
<!-- resultat -->
```text
+-------------+
| ville       |
+-------------+
| Genève      |
| Lille       |
| Liège       |
| Lyon        |
| Montpellier |
| Nantes      |
| Tours       |
| Valencia    |
+-------------+
8 lignes
```
<!-- /resultat -->

---

## 4.7 Tables temporaires et `INTO`

### Concept

Pour une analyse en plusieurs étapes, il est pratique de **stocker un résultat intermédiaire** dans une table, puis de l'interroger comme n'importe quelle table.

| Instruction | Effet | Durée de vie |
|---|---|---|
| `CREATE TEMPORARY TABLE t AS SELECT …` | crée une table temporaire remplie par la requête | jusqu'à la **fin de la session** (déconnexion) ; invisible des autres utilisateurs |
| `CREATE TABLE t AS SELECT …` | crée une **vraie** table remplie par la requête | permanente |
| `INSERT INTO t SELECT …` | ajoute le résultat dans une table **existante** | — |
| `SELECT … INTO nouvelle_table FROM …` | **SQL standard / SQL Server** : crée la table | **non supporté par MySQL** |

### Exemples

**Étape 1 : une table temporaire des inclus par centre**

<!-- exec -->
```sql
CREATE TEMPORARY TABLE tmp_inclus_centre AS
SELECT p.etude_id, p.centre_id, COUNT(p.date_inclusion) AS inclus
FROM patient p
GROUP BY p.etude_id, p.centre_id;
```

**Étape 2 : l'utiliser comme une table normale**

```sql
SELECT e.code, c.nom, t.inclus, ec.objectif_inclusions,
       ROUND(100 * t.inclus / ec.objectif_inclusions) AS atteinte_pct
FROM tmp_inclus_centre t
JOIN etude_centre ec ON ec.etude_id = t.etude_id AND ec.centre_id = t.centre_id
JOIN etude  e ON e.id = t.etude_id
JOIN centre c ON c.id = t.centre_id
ORDER BY atteinte_pct DESC;
```
<!-- resultat:20 -->
```text
+-----------+-----------------------------+--------+---------------------+--------------+
| code      | nom                         | inclus | objectif_inclusions | atteinte_pct |
+-----------+-----------------------------+--------+---------------------+--------------+
| CARDIO-01 | Clinique du Val de Loire    | 33     | 30                  | 110.0        |
| CARDIO-01 | Hôpital Saint-Roch          | 26     | 25                  | 104.0        |
| NEURO-04  | Clinique du Val de Loire    | 15     | 15                  | 100.0        |
| NEURO-04  | CHU Atlantique              | 15     | 15                  | 100.0        |
| CARDIO-01 | Clinique du Léman           | 18     | 20                  | 90.0         |
| CARDIO-01 | CHU Atlantique              | 21     | 25                  | 84.0         |
| DIAB-02   | Clinique des Flandres       | 19     | 25                  | 76.0         |
| DIAB-02   | Clinique du Val de Loire    | 15     | 20                  | 75.0         |
| CARDIO-01 | Centre Hospitalier du Rhône | 14     | 20                  | 70.0         |
| ONCO-03   | CHU Atlantique              | 10     | 20                  | 50.0         |
| DIAB-02   | Hôpital Saint-Roch          | 9      | 20                  | 45.0         |
| DIAB-02   | Hospital del Sol            | 6      | 15                  | 40.0         |
| ONCO-03   | Centre Hospitalier du Rhône | 7      | 20                  | 35.0         |
| ONCO-03   | Clinique du Léman           | 4      | 20                  | 20.0         |
+-----------+-----------------------------+--------+---------------------+--------------+
14 lignes
```
<!-- /resultat -->

> 💡 Dans DBeaver, chaque éditeur SQL a sa propre session : une table temporaire créée dans un onglet n'est pas visible dans un autre.

**Une table permanente d'archive** :

```sql
CREATE TABLE archive_ei_graves AS
SELECT ei.*, p.code_patient
FROM evenement_indesirable ei
JOIN patient p ON p.id = ei.patient_id
WHERE ei.grave = TRUE;
```

**Ajouter des lignes à une table existante** :

```sql
INSERT INTO archive_ei_graves
SELECT ei.*, p.code_patient
FROM evenement_indesirable ei
JOIN patient p ON p.id = ei.patient_id
WHERE ei.grade = 3 AND ei.grave = FALSE;
```

**`SELECT … INTO`** — à connaître pour l'examen :

```sql
-- SQL standard / SQL Server : crée la table archive_ei_graves et la remplit
SELECT ei.*, p.code_patient
INTO archive_ei_graves
FROM evenement_indesirable ei
JOIN patient p ON p.id = ei.patient_id
WHERE ei.grave = TRUE;

-- Équivalent MySQL :
CREATE TABLE archive_ei_graves AS
SELECT … ;
```

> En MySQL, `SELECT … INTO` existe mais avec un autre sens : ranger une valeur dans une **variable** (`SELECT COUNT(*) INTO @nb FROM patient;`) ou écrire un **fichier** (`INTO OUTFILE`).

---

## 4.8 Les CTE : `WITH` pour découper une requête en étapes

### Concept

Une **CTE** (*Common Table Expression*) est une sous-requête **nommée**, déclarée en tête de requête avec `WITH`. On peut ensuite l'utiliser comme une table, plusieurs fois. C'est une table temporaire qui ne vit que le temps d'une requête — et c'est **la** façon la plus lisible de construire un indicateur complexe. (Standard SQL, disponible depuis MySQL 8.)

```
WITH
  etape1 AS ( SELECT … ),
  etape2 AS ( SELECT … FROM etape1 … )
SELECT …
FROM etape2 …;
```

### Exemples

**Le FULL OUTER JOIN de 4.4, réécrit avec des CTE** :

```sql
WITH diab AS (
    SELECT DATE_FORMAT(date_inclusion, '%Y-%m') AS mois, COUNT(*) AS nb
    FROM patient WHERE etude_id = 2 AND YEAR(date_inclusion) = 2025 GROUP BY mois
), onco AS (
    SELECT DATE_FORMAT(date_inclusion, '%Y-%m') AS mois, COUNT(*) AS nb
    FROM patient WHERE etude_id = 3 AND YEAR(date_inclusion) = 2025 GROUP BY mois
)
SELECT d.mois, d.nb AS diab, o.nb AS onco FROM diab d LEFT JOIN onco o ON d.mois = o.mois
UNION
SELECT o.mois, d.nb, o.nb FROM diab d RIGHT JOIN onco o ON d.mois = o.mois
ORDER BY mois;
```
<!-- resultat:15 -->
```text
ERREUR DE GÉNÉRATION : 1st ORDER BY term does not match any column in the result set
```
<!-- /resultat -->

**Un tableau de bord par étude en 3 étapes** :

```sql
WITH recrutement AS (
    SELECT etude_id,
           COUNT(*)              AS screenes,
           COUNT(date_inclusion) AS inclus
    FROM patient
    GROUP BY etude_id
), securite AS (
    SELECT p.etude_id,
           COUNT(*)                                AS nb_ei,
           SUM(CASE WHEN ei.grave THEN 1 ELSE 0 END) AS nb_eig
    FROM evenement_indesirable ei
    JOIN patient p ON p.id = ei.patient_id
    GROUP BY p.etude_id
)
SELECT e.code,
       e.objectif_inclusions                                AS objectif,
       COALESCE(r.inclus, 0)                                AS inclus,
       ROUND(100 * COALESCE(r.inclus, 0) / e.objectif_inclusions) AS atteinte_pct,
       COALESCE(s.nb_ei, 0)                                 AS nb_ei,
       COALESCE(s.nb_eig, 0)                                AS nb_ei_graves
FROM etude e
LEFT JOIN recrutement r ON r.etude_id = e.id
LEFT JOIN securite    s ON s.etude_id = e.id
ORDER BY e.code;
```
<!-- resultat -->
```text
+-----------+----------+--------+--------------+-------+--------------+
| code      | objectif | inclus | atteinte_pct | nb_ei | nb_ei_graves |
+-----------+----------+--------+--------------+-------+--------------+
| CARDIO-01 | 120      | 112    | 93.0         | 107   | 11           |
| DERM-05   | 100      | 0      | 0.0          | 0     | 0            |
| DIAB-02   | 80       | 49     | 61.0         | 47    | 6            |
| NEURO-04  | 30       | 30     | 100.0        | 28    | 5            |
| ONCO-03   | 60       | 21     | 35.0         | 26    | 4            |
+-----------+----------+--------+--------------+-------+--------------+
5 lignes
```
<!-- /resultat -->

---

## À vous

👉 Exercices : [`exercices/04-jointures.md`](../exercices/04-jointures.md)

---

## Pièges

- **Oublier une condition de jointure** → produit cartésien, résultats gonflés.
- **Joindre sur la mauvaise colonne** (`p.id = e.id` au lieu de `p.etude_id = e.id`) : pas d'erreur, résultat faux. Vérifiez toujours le nombre de lignes obtenu.
- **`INNER JOIN` qui fait disparaître des lignes** : les études sans patient, les centres sans EI… Si « il en manque », pensez `LEFT JOIN`.
- **Filtre sur la table de droite dans le `WHERE`** : transforme le `LEFT JOIN` en `INNER JOIN` (cf. 4.3).
- **`COUNT(*)` après un `LEFT JOIN`** : compte 1 pour les lignes sans correspondance.
- **La multiplication des lignes (« fan-out »)** : joindre un patient à ses visites **et** à ses EI dans la même requête crée *visites × EI* lignes par patient. Les comptes et les sommes deviennent faux :

```sql
-- ❌ nb_visites et nb_ei sont multipliés l'un par l'autre
SELECT p.code_patient, COUNT(v.id) AS nb_visites, COUNT(ei.id) AS nb_ei
FROM patient p
LEFT JOIN visite v                 ON v.patient_id  = p.id
LEFT JOIN evenement_indesirable ei ON ei.patient_id = p.id
WHERE p.id = 16
GROUP BY p.code_patient;
```
<!-- resultat -->
```text
+-------------------+------------+-------+
| code_patient      | nb_visites | nb_ei |
+-------------------+------------+-------+
| CARDIO-01-C01-016 | 10         | 10    |
+-------------------+------------+-------+
1 ligne
```
<!-- /resultat -->

```sql
-- ✅ COUNT(DISTINCT …) (ou agréger chaque table séparément dans des CTE)
SELECT p.code_patient, COUNT(DISTINCT v.id) AS nb_visites, COUNT(DISTINCT ei.id) AS nb_ei
FROM patient p
LEFT JOIN visite v                 ON v.patient_id  = p.id
LEFT JOIN evenement_indesirable ei ON ei.patient_id = p.id
WHERE p.id = 16
GROUP BY p.code_patient;
```
<!-- resultat -->
```text
+-------------------+------------+-------+
| code_patient      | nb_visites | nb_ei |
+-------------------+------------+-------+
| CARDIO-01-C01-016 | 5          | 2     |
+-------------------+------------+-------+
1 ligne
```
<!-- /resultat -->

> `COUNT(DISTINCT)` sauve les comptages, mais **pas les sommes ni les moyennes** : pour celles-là, agrégez chaque table à part (CTE ou sous-requêtes) avant de joindre.

> ### ⚖️ Standard vs MySQL
> | Besoin | SQL standard | MySQL |
> |---|---|---|
> | Jointure complète | `FULL OUTER JOIN` | **non supporté** → `LEFT JOIN … UNION … RIGHT JOIN` |
> | Créer une table depuis une requête | `SELECT … INTO t FROM …` (SQL Server) / `CREATE TABLE t AS SELECT …` | `CREATE TABLE t AS SELECT …` |
> | Table temporaire | `CREATE [GLOBAL\|LOCAL] TEMPORARY TABLE …` | `CREATE TEMPORARY TABLE …` |
> | `INTERSECT` / `EXCEPT` | oui | seulement depuis MySQL 8.0.31 (sinon `IN` / `NOT IN`) |
> | CTE (`WITH`) | oui | depuis MySQL 8.0 |
> | Jointure naturelle | `NATURAL JOIN`, `JOIN … USING (col)` | idem (à éviter : fragile) |

---

## Quiz

1. Quelle jointure garde toutes les études, même celles qui n'ont aucun patient ?
   - a) `etude e INNER JOIN patient p ON …`
   - b) `etude e LEFT JOIN patient p ON …`
   - c) `patient p LEFT JOIN etude e ON …`
   - d) `etude e CROSS JOIN patient p`

2. Combien de lignes renvoie un `CROSS JOIN` entre une table de 8 lignes et une table de 5 lignes ?
   - a) 8  - b) 13  - c) 40  - d) 5

3. Comment obtenir l'équivalent d'un `FULL OUTER JOIN` en MySQL ?
   - a) `INNER JOIN` + `UNION ALL`
   - b) `LEFT JOIN` + `UNION` + `RIGHT JOIN`
   - c) `CROSS JOIN` + `WHERE`
   - d) C'est impossible

4. Quelle est la différence entre `UNION` et `UNION ALL` ?
   - a) `UNION ALL` supprime les doublons
   - b) `UNION` supprime les doublons, `UNION ALL` les conserve
   - c) `UNION` ne fonctionne qu'avec deux requêtes
   - d) Aucune

5. Pour lister les centres **sans** patient, on peut écrire :
   - a) `FROM centre c JOIN patient p ON … WHERE p.id IS NULL`
   - b) `FROM centre c LEFT JOIN patient p ON p.centre_id = c.id WHERE p.id IS NULL`
   - c) `FROM centre c LEFT JOIN patient p ON p.centre_id = c.id WHERE p.id IS NOT NULL`
   - d) `FROM patient p LEFT JOIN centre c ON … WHERE c.id IS NULL`

6. Quelle syntaxe crée une table à partir d'une requête en **SQL Server / SQL standard**, mais pas en MySQL ?
   - a) `CREATE TABLE t AS SELECT …`
   - b) `INSERT INTO t SELECT …`
   - c) `SELECT … INTO t FROM …`
   - d) `CREATE VIEW t AS SELECT …`

<details>
<summary>Réponses</summary>

1. **b**. 2. **c** (8 × 5). 3. **b**. 4. **b**. 5. **b** — avec un `INNER JOIN` (a), les centres sans patient sont déjà éliminés. 6. **c**.
</details>

---

## Côté métier

Les jointures sont ce qui transforme une base en **outil d'analyse** :
- « Les inclusions par **ville** » : `patient` + `centre`.
- « Les EI graves par **promoteur** » : `evenement_indesirable` + `patient` + `etude`.
- « Les centres **en retard** sur leur objectif » : `etude_centre` + agrégat de `patient`.
- « Ce qui **manque** » (centres sans patient, visites sans mesure…) : `LEFT JOIN … IS NULL`.

Méthode pour une requête complexe : **1)** repérer les tables nécessaires sur le schéma, **2)** écrire les jointures et vérifier le nombre de lignes, **3)** ajouter les filtres, **4)** agréger, **5)** si ça devient illisible, découper en CTE.

---

⬅️ [Module 3](03-requetes-simples.md) · ➡️ [Module 5 — Mise à jour des données](05-mise-a-jour.md)
