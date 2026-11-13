# Corrigés — Module 5 : Mise à jour des données

> Les corrigés s'enchaînent : exécutez-les dans l'ordre sur une base fraîchement rechargée.

**Ex 5.1**

```sql
INSERT INTO centre (nom, ville) VALUES ('Clinique Océane', 'Biarritz');
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

```sql
SELECT * FROM centre WHERE ville = 'Biarritz';
```
<!-- resultat -->
```text
+----+-----------------+----------+--------+
| id | nom             | ville    | pays   |
+----+-----------------+----------+--------+
| 9  | Clinique Océane | Biarritz | France |
+----+-----------------+----------+--------+
1 ligne
```
<!-- /resultat -->

**Ex 5.2**

```sql
SELECT id FROM centre WHERE nom = 'Clinique Océane';   -- → 9
```
<!-- resultat -->
```text
+----+
| id |
+----+
| 9  |
+----+
1 ligne
```
<!-- /resultat -->

```sql
INSERT INTO investigateur (nom, prenom, specialite, email, centre_id)
VALUES ('Kaci', 'Nadia', 'Oncologie', 'nadia.kaci@oceane-centre9.example', 9);
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

Variante sans identifiant en dur :

```sql
INSERT INTO investigateur (nom, prenom, specialite, email, centre_id)
SELECT 'Kaci', 'Nadia', 'Oncologie', 'nadia.kaci@oceane-centre9.example', id
FROM centre WHERE nom = 'Clinique Océane';
```

**Ex 5.3**

```sql
INSERT INTO etude_centre (etude_id, centre_id, investigateur_principal_id, date_ouverture, objectif_inclusions)
SELECT e.id, c.id, i.id, '2026-07-01', 10
FROM etude e, centre c, investigateur i
WHERE e.code  = 'ONCO-03'
  AND c.nom   = 'Clinique Océane'
  AND i.email = 'nadia.kaci@oceane-centre9.example';
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

Chaque table ne renvoie qu'une ligne : leur produit cartésien donne exactement la ligne à insérer.

```sql
SELECT * FROM etude_centre WHERE etude_id = 3;
```
<!-- resultat -->
```text
+----------+-----------+----------------------------+----------------+---------------------+
| etude_id | centre_id | investigateur_principal_id | date_ouverture | objectif_inclusions |
+----------+-----------+----------------------------+----------------+---------------------+
| 3        | 2         | 5                          | 2025-07-01     | 20                  |
| 3        | 4         | 10                         | 2025-08-15     | 20                  |
| 3        | 6         | 14                         | 2025-10-01     | 20                  |
| 3        | 9         | 19                         | 2026-07-01     | 10                  |
+----------+-----------+----------------------------+----------------+---------------------+
4 lignes
```
<!-- /resultat -->

**Ex 5.4**

```sql
UPDATE etude
SET date_debut = '2026-09-01',
    statut     = 'recrutement'
WHERE code = 'DERM-05';
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

**Ex 5.5**

```sql
UPDATE etude_centre
SET date_ouverture = '2026-09-15'
WHERE etude_id = (SELECT id FROM etude WHERE code = 'DERM-05');
```
<!-- resultat -->
```text
Requête OK, 2 lignes affectées
```
<!-- /resultat -->

**Ex 5.6**

```sql
SELECT id, date_survenue FROM evenement_indesirable
WHERE grade = 1 AND date_resolution IS NULL;
```
<!-- resultat -->
```text
+-----+---------------+
| id  | date_survenue |
+-----+---------------+
| 24  | 2025-12-22    |
| 27  | 2025-09-04    |
| 46  | 2026-06-05    |
| 90  | 2025-11-10    |
| 98  | 2026-06-25    |
| 103 | 2025-07-07    |
| 132 | 2026-06-28    |
| 144 | 2026-06-13    |
| 150 | 2026-06-29    |
| 158 | 2026-05-05    |
| 162 | 2026-06-13    |
| 169 | 2026-06-26    |
+-----+---------------+
12 lignes
```
<!-- /resultat -->

```sql
UPDATE evenement_indesirable
SET date_resolution = DATE_ADD(date_survenue, INTERVAL 30 DAY)
WHERE grade = 1 AND date_resolution IS NULL;
```
<!-- resultat -->
```text
Requête OK, 12 lignes affectées
```
<!-- /resultat -->

**Ex 5.7**

```sql
UPDATE patient
SET date_sortie  = '2026-06-15',
    motif_sortie = 'perdu de vue'
WHERE code_patient = 'DIAB-02-C07-008'
  AND date_sortie IS NULL;
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

**Ex 5.8**

```sql
SELECT v.id, v.type_visite, v.date_prevue
FROM visite v
WHERE v.patient_id = (SELECT id FROM patient WHERE code_patient = 'DIAB-02-C07-008')
  AND v.date_prevue > '2026-06-30';
```
<!-- resultat -->
```text
+------+-------------+-------------+
| id   | type_visite | date_prevue |
+------+-------------+-------------+
| 1062 | V5          | 2026-08-28  |
| 1063 | V6          | 2027-02-12  |
+------+-------------+-------------+
2 lignes
```
<!-- /resultat -->

```sql
DELETE FROM visite
WHERE patient_id = (SELECT id FROM patient WHERE code_patient = 'DIAB-02-C07-008')
  AND date_prevue > '2026-06-30';
```
<!-- resultat -->
```text
Requête OK, 2 lignes affectées
```
<!-- /resultat -->

Pas de mesure à supprimer avant : une visite future n'est pas réalisée, donc n'a pas de mesure.

**Ex 5.9**

<!-- exec -->
```sql
START TRANSACTION;
```

```sql
-- 1. les mesures de ses visites
DELETE FROM mesure
WHERE visite_id IN (SELECT id FROM visite
                    WHERE patient_id = (SELECT id FROM patient WHERE code_patient = 'NEURO-04-C02-016'));
```
<!-- resultat -->
```text
Requête OK, 12 lignes affectées
```
<!-- /resultat -->

```sql
-- 2. ses visites
DELETE FROM visite
WHERE patient_id = (SELECT id FROM patient WHERE code_patient = 'NEURO-04-C02-016');
```
<!-- resultat -->
```text
Requête OK, 4 lignes affectées
```
<!-- /resultat -->

```sql
-- 3. ses événements indésirables
DELETE FROM evenement_indesirable
WHERE patient_id = (SELECT id FROM patient WHERE code_patient = 'NEURO-04-C02-016');
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

```sql
-- 4. le patient lui-même
DELETE FROM patient WHERE code_patient = 'NEURO-04-C02-016';
```
<!-- resultat -->
```text
Requête OK, 1 ligne affectée
```
<!-- /resultat -->

```sql
-- 5. vérification avant de valider
SELECT COUNT(*) AS reste FROM patient WHERE code_patient = 'NEURO-04-C02-016';
```
<!-- resultat -->
```text
+-------+
| reste |
+-------+
| 0     |
+-------+
1 ligne
```
<!-- /resultat -->

<!-- exec -->
```sql
COMMIT;
```

**Ex 5.10**

<!-- exec -->
```sql
CREATE TABLE objectif_mensuel (
    etude_id INT     NOT NULL,
    mois     CHAR(7) NOT NULL,
    objectif INT     NOT NULL,
    CONSTRAINT pk_objectif_mensuel       PRIMARY KEY (etude_id, mois),
    CONSTRAINT fk_objectif_mensuel_etude FOREIGN KEY (etude_id) REFERENCES etude (id)
);
```

```sql
INSERT INTO objectif_mensuel (etude_id, mois, objectif)
SELECT DISTINCT etude_id, DATE_FORMAT(date_inclusion, '%Y-%m'), 5
FROM patient
WHERE etude_id = 2 AND YEAR(date_inclusion) = 2026;
```
<!-- resultat -->
```text
Requête OK, 6 lignes affectées
```
<!-- /resultat -->

```sql
SELECT o.mois, o.objectif, COUNT(p.id) AS realise
FROM objectif_mensuel o
LEFT JOIN patient p ON p.etude_id = o.etude_id
                   AND DATE_FORMAT(p.date_inclusion, '%Y-%m') = o.mois
GROUP BY o.mois, o.objectif
ORDER BY o.mois;
```
<!-- resultat -->
```text
+---------+----------+---------+
| mois    | objectif | realise |
+---------+----------+---------+
| 2026-01 | 5        | 4       |
| 2026-02 | 5        | 2       |
| 2026-03 | 5        | 2       |
| 2026-04 | 5        | 2       |
| 2026-05 | 5        | 2       |
| 2026-06 | 5        | 1       |
+---------+----------+---------+
6 lignes
```
<!-- /resultat -->

**Ex 5.11** — `date_realisee = NULL` vaut toujours NULL (inconnu) : **aucune ligne n'est supprimée**, sans message d'erreur. La forme correcte est `WHERE date_realisee IS NULL`.

Mais attention : cela supprimerait aussi les **visites futures** (pas encore faites, c'est normal) et les **visites manquées**, qui sont une information précieuse pour la qualité de l'étude (taux de visites manquées !). Avant de supprimer des données, demandez-vous toujours si elles ne servent pas à un indicateur.
