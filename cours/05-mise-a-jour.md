# Module 5 — Mise à jour des données

> **Objectif** : ajouter (`INSERT`), modifier (`UPDATE`) et supprimer (`DELETE`) des lignes, en ciblant précisément les lignes concernées avec `WHERE`, et travailler **sans risque** grâce aux transactions.
> **Durée indicative** : 3 h
> 🔄 Ce module modifie la base. Rechargez `db/essais_cliniques.sql` à la fin (ou à tout moment en cas d'erreur).

---

## 5.1 `INSERT` : ajouter des lignes

### Concept

```
INSERT INTO table (colonne1, colonne2, …)
VALUES (valeur1, valeur2, …);
```

- On **liste les colonnes** que l'on remplit ; les autres prennent leur valeur **par défaut** (`DEFAULT`), ou NULL, ou — pour une clé `AUTO_INCREMENT` — le prochain numéro.
- Les valeurs sont données **dans le même ordre** que les colonnes.
- Toutes les **contraintes** (module 2) sont vérifiées : type, NOT NULL, UNIQUE, CHECK, clés étrangères.

### Visuel

```
  INSERT INTO patient (code_patient, etude_id, centre_id, sexe, …) VALUES ('DIAB-02-C03-012', 2, 3, 'F', …)

   patient                                                            
  ┌─────┬───────────────────┬──────────┬───────────┬──────┬─────┐
  │ id  │ code_patient      │ etude_id │ centre_id │ sexe │ …   │
  ├─────┼───────────────────┼──────────┼───────────┼──────┼─────┤
  │ …   │ …                 │ …        │ …         │ …    │     │
  │ 262 │ NEURO-04-C02-016  │ 4        │ 2         │ M    │     │
  │ 263 │ DIAB-02-C03-012   │ 2        │ 3         │ F    │     │ ◄── nouvelle ligne
  └─────┴───────────────────┴──────────┴───────────┴──────┴─────┘
     ▲ attribué automatiquement (AUTO_INCREMENT)
```

### Exemples

**Une nouvelle patiente screenée dans DIAB-02 à Montpellier** :

```sql
INSERT INTO patient (code_patient, etude_id, centre_id, sexe, annee_naissance, date_screening)
VALUES ('DIAB-02-C03-012', 2, 3, 'F', 1972, '2026-06-30');
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

Les colonnes non citées (`date_inclusion`, `bras`, `date_sortie`, `motif_sortie`) valent NULL. Vérifions :

```sql
SELECT * FROM patient WHERE code_patient = 'DIAB-02-C03-012';
```
<!-- resultat -->
```text
+-----+-----------------+----------+-----------+------+-----------------+----------------+----------------+------+-------------+--------------+
| id  | code_patient    | etude_id | centre_id | sexe | annee_naissance | date_screening | date_inclusion | bras | date_sortie | motif_sortie |
+-----+-----------------+----------+-----------+------+-----------------+----------------+----------------+------+-------------+--------------+
| 263 | DIAB-02-C03-012 | 2        | 3         | F    | 1972            | 2026-06-30     | NULL           | NULL | NULL        | NULL         |
+-----+-----------------+----------+-----------+------+-----------------+----------------+----------------+------+-------------+--------------+
1 ligne
```
<!-- /resultat -->

**Plusieurs lignes en une instruction** — deux EI déclarés pour le patient 16 :

```sql
INSERT INTO evenement_indesirable (patient_id, date_survenue, terme, grade, lien_traitement)
VALUES (16, '2026-06-20', 'Céphalées', 1, 'possible'),
       (16, '2026-06-25', 'Nausées',   2, 'probable');
```
<!-- resultat -->
```text
Requête OK, 2 lignes affectées
```
<!-- /resultat -->

`grave` prend sa valeur par défaut (`FALSE`) et `date_resolution` reste NULL.

**Récupérer l'identifiant attribué** — utile pour insérer ensuite des lignes « enfants » :

```sql
SELECT LAST_INSERT_ID();   -- MySQL : dernier id AUTO_INCREMENT créé dans la session
```

**`INSERT … SELECT` : insérer le résultat d'une requête**. Créons une table de suivi des alertes de sécurité, et remplissons-la avec les EI graves survenus en 2026 :

<!-- exec -->
```sql
CREATE TABLE alerte (
    id            INT          NOT NULL AUTO_INCREMENT,
    ei_id         INT          NOT NULL,
    code_patient  VARCHAR(20)  NOT NULL,
    message       VARCHAR(200) NOT NULL,
    date_creation DATE         NOT NULL,
    CONSTRAINT pk_alerte PRIMARY KEY (id),
    CONSTRAINT fk_alerte_ei FOREIGN KEY (ei_id) REFERENCES evenement_indesirable (id)
);
```

```sql
INSERT INTO alerte (ei_id, code_patient, message, date_creation)
SELECT ei.id, p.code_patient,
       CONCAT('EI grave : ', ei.terme, ' (grade ', ei.grade, ')'),
       '2026-06-30'
FROM evenement_indesirable ei
JOIN patient p ON p.id = ei.patient_id
WHERE ei.grave = TRUE AND ei.date_survenue >= '2026-01-01';
```
<!-- resultat -->
```text
Requête OK, 7 lignes affectées
```
<!-- /resultat -->

```sql
SELECT * FROM alerte;
```
<!-- resultat -->
```text
+----+-------+-------------------+------------------------------------------+---------------+
| id | ei_id | code_patient      | message                                  | date_creation |
+----+-------+-------------------+------------------------------------------+---------------+
| 1  | 48    | CARDIO-01-C02-025 | EI grave : Céphalées (grade 3)           | 2026-06-30    |
| 2  | 79    | CARDIO-01-C03-028 | EI grave : Vertiges (grade 3)            | 2026-06-30    |
| 3  | 93    | CARDIO-01-C04-016 | EI grave : Œdème des chevilles (grade 3) | 2026-06-30    |
| 4  | 104   | CARDIO-01-C06-016 | EI grave : Vertiges (grade 4)            | 2026-06-30    |
| 5  | 110   | DIAB-02-C01-008   | EI grave : Diarrhée (grade 3)            | 2026-06-30    |
| 6  | 139   | DIAB-02-C05-008   | EI grave : Douleur abdominale (grade 3)  | 2026-06-30    |
| 7  | 172   | ONCO-03-C04-008   | EI grave : Anémie (grade 4)              | 2026-06-30    |
+----+-------+-------------------+------------------------------------------+---------------+
7 lignes
```
<!-- /resultat -->

---

## 5.2 `UPDATE` : modifier des lignes

### Concept

```
UPDATE table
SET colonne1 = valeur1,
    colonne2 = valeur2
WHERE condition;          ← SANS WHERE, TOUTES les lignes sont modifiées !
```

### Visuel

```
  UPDATE patient SET date_inclusion = '2026-07-14', bras = 'traitement'
  WHERE code_patient = 'DIAB-02-C03-012'

   AVANT                                                APRÈS
  ┌─────────────────┬────────────────┬──────┐          ┌─────────────────┬────────────────┬────────────┐
  │ code_patient    │ date_inclusion │ bras │          │ code_patient    │ date_inclusion │ bras       │
  ├─────────────────┼────────────────┼──────┤          ├─────────────────┼────────────────┼────────────┤
  │ DIAB-02-C03-011 │ NULL           │ NULL │  ──────► │ DIAB-02-C03-011 │ NULL           │ NULL       │ ← WHERE faux : inchangée
  │ DIAB-02-C03-012 │ NULL           │ NULL │          │ DIAB-02-C03-012 │ 2026-07-14     │ traitement │ ← WHERE vrai : modifiée
  └─────────────────┴────────────────┴──────┘          └─────────────────┴────────────────┴────────────┘
```

### Exemples

> 🛡️ **Réflexe de sécurité** : avant tout `UPDATE` ou `DELETE`, exécutez d'abord un `SELECT` avec **le même `WHERE`**, et vérifiez que ce sont bien les lignes visées.

**Inclure la nouvelle patiente** :

```sql
-- 1. je vérifie la cible
SELECT id, code_patient, date_inclusion, bras FROM patient WHERE code_patient = 'DIAB-02-C03-012';
```
<!-- resultat -->
```text
+-----+-----------------+----------------+------+
| id  | code_patient    | date_inclusion | bras |
+-----+-----------------+----------------+------+
| 263 | DIAB-02-C03-012 | NULL           | NULL |
+-----+-----------------+----------------+------+
1 ligne
```
<!-- /resultat -->

```sql
-- 2. je modifie
UPDATE patient
SET date_inclusion = '2026-07-14',
    bras           = 'traitement'
WHERE code_patient = 'DIAB-02-C03-012';
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

**Corriger une valeur** — la visite V4 du patient 1 a été saisie avec une mauvaise date :

```sql
SELECT id, type_visite, date_prevue, date_realisee FROM visite WHERE patient_id = 1 AND type_visite = 'V4';
```
<!-- resultat -->
```text
+----+-------------+-------------+---------------+
| id | type_visite | date_prevue | date_realisee |
+----+-------------+-------------+---------------+
| 5  | V4          | 2024-07-23  | 2024-07-24    |
+----+-------------+-------------+---------------+
1 ligne
```
<!-- /resultat -->

```sql
UPDATE visite
SET date_realisee = '2024-07-25'
WHERE patient_id = 1 AND type_visite = 'V4';
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

**Calculer la nouvelle valeur à partir de l'ancienne** — le promoteur relève de 10 % l'objectif de tous les centres de DIAB-02 (arrondi à l'entier) :

```sql
UPDATE etude_centre
SET objectif_inclusions = ROUND(objectif_inclusions * 1.1)
WHERE etude_id = 2;
```
<!-- resultat -->
```text
Requête OK, 4 lignes affectées
```
<!-- /resultat -->

```sql
SELECT etude_id, centre_id, objectif_inclusions FROM etude_centre WHERE etude_id = 2;
```
<!-- resultat -->
```text
+----------+-----------+---------------------+
| etude_id | centre_id | objectif_inclusions |
+----------+-----------+---------------------+
| 2        | 1         | 22                  |
| 2        | 3         | 22                  |
| 2        | 5         | 28                  |
| 2        | 7         | 17                  |
+----------+-----------+---------------------+
4 lignes
```
<!-- /resultat -->

**Mise à jour conditionnelle avec `CASE`** — un seul `UPDATE` pour plusieurs règles : on passe les EI de grade 4 en « grave » s'ils ne l'étaient pas, sans toucher aux autres :

```sql
UPDATE evenement_indesirable
SET grave = CASE WHEN grade >= 4 THEN TRUE ELSE grave END
WHERE grade >= 3;
```

```text
Requête OK, 0 ligne affectée
Rows matched: 39  Changed: 0
```

Ici aucune valeur ne change réellement : tous les grades 4 étaient déjà graves. MySQL distingue les lignes **trouvées** par le `WHERE` (*matched*) des lignes réellement **modifiées** (*changed*).

**`UPDATE` avec une sous-requête** — résoudre au 30/06/2026 tous les EI non résolus des patients **sortis** de l'étude :

```sql
SELECT COUNT(*) AS cibles
FROM evenement_indesirable
WHERE date_resolution IS NULL
  AND patient_id IN (SELECT id FROM patient WHERE date_sortie IS NOT NULL);
```
<!-- resultat -->
```text
+--------+
| cibles |
+--------+
| 6      |
+--------+
1 ligne
```
<!-- /resultat -->

```sql
UPDATE evenement_indesirable
SET date_resolution = '2026-06-30'
WHERE date_resolution IS NULL
  AND patient_id IN (SELECT id FROM patient WHERE date_sortie IS NOT NULL);
```
<!-- resultat -->
```text
Requête OK, 6 lignes affectées
```
<!-- /resultat -->

**Clôturer la participation d'un patient** :

```sql
UPDATE patient
SET date_sortie  = '2026-06-30',
    motif_sortie = 'retrait du consentement'
WHERE code_patient = 'CARDIO-01-C06-016'
  AND date_sortie IS NULL;
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

> 💡 `AND date_sortie IS NULL` est une **garde** : si le patient était déjà sorti, on n'écrase pas sa vraie date de sortie.

**Mettre à NULL** :

```sql
UPDATE etude_centre SET date_ouverture = NULL WHERE etude_id = 5;
```

```text
Requête OK, 0 ligne affectée
Rows matched: 2  Changed: 0
```

(Aucune valeur ne change : elles étaient déjà NULL.) Remarquez la syntaxe : on écrit `SET colonne = NULL` (affectation), mais `WHERE colonne IS NULL` (test).

---

## 5.3 `DELETE` et `TRUNCATE` : supprimer des lignes

### Concept

```
DELETE FROM table
WHERE condition;          ← SANS WHERE, TOUTES les lignes sont supprimées !

TRUNCATE TABLE table;     ← vide entièrement la table (plus rapide, remet l'AUTO_INCREMENT à 1)
```

| | `DELETE FROM t WHERE …` | `DELETE FROM t` | `TRUNCATE TABLE t` | `DROP TABLE t` |
|---|---|---|---|---|
| Supprime | les lignes ciblées | toutes les lignes | toutes les lignes | **la table elle-même** |
| Structure conservée | oui | oui | oui | **non** |
| Annulable (transaction) | oui | oui | **non** en MySQL | **non** |
| Famille | LMD | LMD | LDD | LDD |

### Exemples

**Supprimer les alertes d'un patient** :

```sql
SELECT * FROM alerte WHERE code_patient = 'CARDIO-01-C06-016';
```
<!-- resultat -->
```text
+----+-------+-------------------+-------------------------------+---------------+
| id | ei_id | code_patient      | message                       | date_creation |
+----+-------+-------------------+-------------------------------+---------------+
| 4  | 104   | CARDIO-01-C06-016 | EI grave : Vertiges (grade 4) | 2026-06-30    |
+----+-------+-------------------+-------------------------------+---------------+
1 ligne
```
<!-- /resultat -->

```sql
DELETE FROM alerte WHERE code_patient = 'CARDIO-01-C06-016';
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

**Supprimer avec une sous-requête** — les deux EI de test insérés en 5.1 :

```sql
DELETE FROM evenement_indesirable
WHERE patient_id = 16
  AND date_survenue >= '2026-06-20'
  AND id NOT IN (SELECT ei_id FROM alerte);
```
<!-- resultat -->
```text
Requête OK, 2 lignes affectées
```
<!-- /resultat -->

**Les clés étrangères protègent les données** : impossible de supprimer un patient qui a des visites.

```sql
DELETE FROM patient WHERE id = 16;
```

```text
ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails
(`essais_cliniques`.`visite`, CONSTRAINT `fk_visite_patient` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`id`))
```

Pour supprimer un patient, il faut d'abord supprimer ses « enfants », **dans l'ordre inverse des dépendances** :

```
   mesure ──► visite ──► patient ◄── evenement_indesirable ◄── alerte
   1. mesures   2. visites     4. patient   3. EI (et d'abord leurs alertes)
```

La patiente `DIAB-02-C03-012` créée en 5.1 n'a ni visite ni EI : elle peut être supprimée directement.

```sql
DELETE FROM patient WHERE code_patient = 'DIAB-02-C03-012';
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

**Vider une table** :

```sql
TRUNCATE TABLE alerte;
```

---

## 5.4 Les transactions : le filet de sécurité

### Concept

Une **transaction** regroupe plusieurs instructions en un bloc **tout ou rien** :
- `START TRANSACTION` : début du bloc ;
- `COMMIT` : on **valide** définitivement toutes les modifications ;
- `ROLLBACK` : on **annule** tout depuis le début du bloc.

Tant que le `COMMIT` n'est pas fait, les modifications ne sont visibles que de votre session, et vous pouvez revenir en arrière.

### Visuel

```
  START TRANSACTION
        │
        ├── UPDATE …   ┐
        ├── DELETE …   │  modifications « en attente »
        ├── INSERT …   ┘  (visibles de moi seul)
        │
        ├──► COMMIT   ──►  ✅ tout est enregistré définitivement
        │
        └──► ROLLBACK ──►  ↩️ tout est annulé, comme si rien ne s'était passé
```

**Mode « auto-commit »** : par défaut, MySQL et DBeaver valident **chaque instruction immédiatement** (un `COMMIT` implicite après chaque requête). `START TRANSACTION` suspend ce comportement jusqu'au `COMMIT` ou au `ROLLBACK`. Dans DBeaver, on peut aussi basculer en mode **transaction manuelle** (bouton *Auto-Commit* de la barre d'outils) : les boutons *Commit* et *Rollback* apparaissent alors.

### Exemple — l'erreur qu'on rattrape

<!-- exec -->
```sql
START TRANSACTION;
```

```sql
-- oups : on a oublié le WHERE !
DELETE FROM mesure;
```
<!-- resultat -->
```text
Requête OK, 3674 lignes affectées
```
<!-- /resultat -->

```sql
SELECT COUNT(*) AS nb_mesures FROM mesure;
```
<!-- resultat -->
```text
+------------+
| nb_mesures |
+------------+
| 0          |
+------------+
1 ligne
```
<!-- /resultat -->

```sql
ROLLBACK;
SELECT COUNT(*) AS nb_mesures FROM mesure;
```
<!-- resultat -->
```text
+------------+
| nb_mesures |
+------------+
| 3674       |
+------------+
1 ligne
```
<!-- /resultat -->

Ouf : les mesures sont revenues.

### Exemple — une opération en plusieurs étapes, tout ou rien

Transférer un patient d'un centre à un autre impose de modifier le patient **et** de tracer l'opération. Si l'une des deux étapes échoue, on ne veut pas de demi-mesure.

```sql
START TRANSACTION;

UPDATE patient SET centre_id = 3 WHERE code_patient = 'CARDIO-01-C01-001';
-- … autres instructions liées …

-- tout s'est bien passé ?
COMMIT;
-- un problème ?
-- ROLLBACK;
```

> ⚠️ Les instructions de **structure** (`CREATE`, `ALTER`, `DROP`, `TRUNCATE`) provoquent en MySQL un `COMMIT` **automatique** : elles ne peuvent pas être annulées par `ROLLBACK`.

---

## À vous

👉 Exercices : [`exercices/05-mise-a-jour.md`](../exercices/05-mise-a-jour.md)

---

## Pièges

- **`UPDATE` ou `DELETE` sans `WHERE`** : toute la table est touchée. Toujours tester le `WHERE` avec un `SELECT` d'abord, ou travailler dans une transaction.
- **`WHERE` trop large** : `WHERE patient_id = 16` au lieu de `WHERE id = 42` supprime tous les EI du patient au lieu d'un seul. Comparez le nombre de lignes affectées à ce que vous attendiez.
- **Oublier la liste des colonnes dans `INSERT`** : `INSERT INTO centre VALUES (…)` impose de fournir toutes les colonnes dans l'ordre exact de la table, et casse si la structure évolue.
- **Ordre de suppression** : enfants d'abord, parents ensuite (clés étrangères).
- **`UPDATE` d'une table en lisant la même table dans une sous-requête** : MySQL le refuse (`ERROR 1093: You can't specify target table 'x' for update in FROM clause`). Contournement : passer par une table temporaire ou une jointure.
- **Mode « safe updates »** : certains outils (MySQL Workbench) refusent par défaut un `UPDATE`/`DELETE` sans condition sur une clé (`ERROR 1175`). C'est une protection, pas un bug.
- **Apostrophes** dans les valeurs texte : `'retrait du consentement'` passe, `'fin d'étude'` non → `'fin d''étude'`.

> ### ⚖️ Standard vs MySQL
> | Besoin | SQL standard | MySQL |
> |---|---|---|
> | Début de transaction | `START TRANSACTION` (ou `BEGIN`) | idem |
> | `UPDATE` avec jointure | `UPDATE t SET … FROM autre WHERE …` (PostgreSQL / SQL Server) ou `MERGE` | `UPDATE t JOIN autre ON … SET …` |
> | `DELETE` avec jointure | `DELETE FROM t WHERE … IN (SELECT …)` | aussi `DELETE t FROM t JOIN autre ON … WHERE …` |
> | Insérer ou mettre à jour | `MERGE INTO …` | `INSERT … ON DUPLICATE KEY UPDATE …` |
> | `TRUNCATE` annulable | dépend du SGBD (oui en PostgreSQL / SQL Server) | **non** |
> | Dernier id créé | dépend du SGBD (`IDENTITY`, `RETURNING`) | `LAST_INSERT_ID()` |

---

## Quiz

1. Que fait `UPDATE patient SET bras = 'placebo';` ?
   - a) Une erreur : il manque le `WHERE`
   - b) Met le bras à `'placebo'` pour **tous** les patients
   - c) Met le bras à `'placebo'` pour les patients dont le bras est NULL
   - d) Rien

2. Quelle instruction annule toutes les modifications depuis `START TRANSACTION` ?
   - a) `COMMIT`  - b) `UNDO`  - c) `ROLLBACK`  - d) `CANCEL`

3. Quelle instruction ajoute dans `alerte` le résultat d'une requête ?
   - a) `INSERT INTO alerte SELECT …`
   - b) `UPDATE alerte SELECT …`
   - c) `SELECT … INTO alerte` (en MySQL)
   - d) `INSERT alerte VALUES (SELECT …)`

4. Pourquoi `DELETE FROM etude WHERE id = 1` échoue-t-il ?
   - a) Il manque `TABLE`
   - b) Des lignes d'autres tables (patients, participations) font référence à cette étude
   - c) On ne peut pas supprimer avec une condition sur `id`
   - d) La table `etude` est en lecture seule

5. Quelle est la différence entre `DELETE FROM t` et `TRUNCATE TABLE t` en MySQL ?
   - a) Aucune
   - b) `TRUNCATE` supprime aussi la structure de la table
   - c) `TRUNCATE` vide la table plus vite, ne peut pas être annulé et remet le compteur AUTO_INCREMENT à zéro
   - d) `DELETE` ne fonctionne qu'avec un `WHERE`

<details>
<summary>Réponses</summary>

1. **b** — aucune erreur, toute la table est modifiée. 2. **c**. 3. **a**. 4. **b**. 5. **c**.
</details>

---

## Côté métier

En tant qu'analyste, vous aurez rarement le droit de modifier les données de production — et c'est tant mieux. Mais vous utiliserez ces instructions pour :
- **préparer vos propres tables de travail** (`CREATE TABLE … AS SELECT`, `INSERT … SELECT`) ;
- **corriger des données** dans une base de test ou un environnement d'analyse ;
- **alimenter des tables de suivi** (alertes, historiques, objectifs) ;
- comprendre ce que font les applications métier qui écrivent dans la base.

Trois réflexes à garder : **`SELECT` avant `UPDATE`/`DELETE`**, **transaction pour toute opération en plusieurs étapes**, **sauvegarde avant toute opération de masse**.

---

⬅️ [Module 4](04-jointures.md) · ➡️ [Module 6 — Création de vues](06-vues.md)
