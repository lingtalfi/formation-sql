# Corrigés — Module 1 : Concepts fondamentaux

**Ex 1.1**

```sql
SELECT * FROM investigateur;
```
<!-- resultat:20 -->
```text
+----+----------+---------+------------------+--------------------------------------------+-----------+----------------+
| id | nom      | prenom  | specialite       | email                                      | centre_id | superviseur_id |
+----+----------+---------+------------------+--------------------------------------------+-----------+----------------+
| 1  | Martin   | Claire  | Cardiologie      | claire.martin@loire-centre1.example        | 1         | NULL           |
| 2  | Bernard  | Hugo    | Diabétologie     | hugo.bernard@loire-centre1.example         | 1         | 1              |
| 3  | Petit    | Inès    | Neurologie       | ines.petit@loire-centre1.example           | 1         | 1              |
| 4  | Robert   | Lucas   | Dermatologie     | lucas.robert@loire-centre1.example         | 1         | 1              |
| 5  | Durand   | Sophie  | Oncologie        | sophie.durand@atlantique-centre2.example   | 2         | NULL           |
| 6  | Moreau   | Thomas  | Cardiologie      | thomas.moreau@atlantique-centre2.example   | 2         | 5              |
| 7  | Lefèvre  | Camille | Neurologie       | camille.lefevre@atlantique-centre2.example | 2         | 5              |
| 8  | Garcia   | Antoine | Cardiologie      | antoine.garcia@saint-roch-centre3.example  | 3         | NULL           |
| 9  | Roux     | Léa     | Diabétologie     | lea.roux@saint-roch-centre3.example        | 3         | 8              |
| 10 | Fournier | Julien  | Oncologie        | julien.fournier@rhone-centre4.example      | 4         | NULL           |
| 11 | Girard   | Manon   | Cardiologie      | manon.girard@rhone-centre4.example         | 4         | 10             |
| 12 | Bonnet   | Paul    | Médecine interne | paul.bonnet@rhone-centre4.example          | 4         | 10             |
| 13 | Lambert  | Emma    | Diabétologie     | emma.lambert@flandres-centre5.example      | 5         | NULL           |
| 14 | Favre    | Nicolas | Oncologie        | nicolas.favre@leman-centre6.example        | 6         | NULL           |
| 15 | Müller   | Anna    | Cardiologie      | anna.muller@leman-centre6.example          | 6         | 14             |
| 16 | López    | Carmen  | Diabétologie     | carmen.lopez@sol-centre7.example           | 7         | NULL           |
| 17 | Sánchez  | Javier  | Médecine interne | javier.sanchez@sol-centre7.example         | 7         | 16             |
| 18 | Dubois   | Marc    | Dermatologie     | marc.dubois@ardennes-centre8.example       | 8         | NULL           |
+----+----------+---------+------------------+--------------------------------------------+-----------+----------------+
18 lignes
```
<!-- /resultat -->

**Ex 1.2**

```sql
SELECT nom, prenom, specialite FROM investigateur;
```
<!-- resultat:5 -->
```text
+---------+--------+--------------+
| nom     | prenom | specialite   |
+---------+--------+--------------+
| Martin  | Claire | Cardiologie  |
| Bernard | Hugo   | Diabétologie |
| Petit   | Inès   | Neurologie   |
| Robert  | Lucas  | Dermatologie |
| Durand  | Sophie | Oncologie    |
+---------+--------+--------------+
… 18 lignes au total (5 affichées)
```
<!-- /resultat -->

**Ex 1.3**

```sql
SELECT * FROM etude_centre;
```
<!-- resultat:20 -->
```text
+----------+-----------+----------------------------+----------------+---------------------+
| etude_id | centre_id | investigateur_principal_id | date_ouverture | objectif_inclusions |
+----------+-----------+----------------------------+----------------+---------------------+
| 1        | 1         | 1                          | 2024-03-15     | 30                  |
| 1        | 2         | 6                          | 2024-04-01     | 25                  |
| 1        | 3         | 8                          | 2024-05-10     | 25                  |
| 1        | 4         | 11                         | 2024-06-01     | 20                  |
| 1        | 6         | 15                         | 2024-09-01     | 20                  |
| 2        | 1         | 2                          | 2025-02-01     | 20                  |
| 2        | 3         | 9                          | 2025-03-01     | 20                  |
| 2        | 5         | 13                         | 2025-02-15     | 25                  |
| 2        | 7         | 16                         | 2025-05-01     | 15                  |
| 3        | 2         | 5                          | 2025-07-01     | 20                  |
| 3        | 4         | 10                         | 2025-08-15     | 20                  |
| 3        | 6         | 14                         | 2025-10-01     | 20                  |
| 4        | 1         | 3                          | 2023-01-20     | 15                  |
| 4        | 2         | 7                          | 2023-02-01     | 15                  |
| 5        | 1         | 4                          | NULL           | 50                  |
| 5        | 8         | 18                         | NULL           | 50                  |
+----------+-----------+----------------------------+----------------+---------------------+
16 lignes
```
<!-- /resultat -->

La clé primaire est **composée** des deux colonnes `(etude_id, centre_id)` : un centre ne participe qu'une fois à une même étude. Ce couple suffit à identifier chaque ligne, une colonne `id` serait redondante. C'est le cas typique d'une **table d'association** entre deux tables (relation plusieurs-à-plusieurs), détaillée au module 2.

**Ex 1.4** — Colonnes NULL-ables de `patient` :

| Colonne | NULL signifie… |
|---|---|
| `date_inclusion` | le patient n'a pas été inclus (échec de screening) |
| `bras` | pas de bras attribué (car pas inclus) |
| `date_sortie` | le patient est toujours dans l'étude |
| `motif_sortie` | idem : pas sorti, donc pas de motif |

**Ex 1.5**

```sql
SELECT code_patient, date_screening, date_inclusion FROM patient;
```
<!-- resultat:8 -->
```text
+-------------------+----------------+----------------+
| code_patient      | date_screening | date_inclusion |
+-------------------+----------------+----------------+
| CARDIO-01-C01-001 | 2024-04-09     | 2024-04-30     |
| CARDIO-01-C01-002 | 2024-04-09     | 2024-04-28     |
| CARDIO-01-C01-003 | 2024-05-04     | 2024-05-18     |
| CARDIO-01-C01-004 | 2024-06-15     | 2024-06-24     |
| CARDIO-01-C01-005 | 2024-06-28     | NULL           |
| CARDIO-01-C01-006 | 2024-07-12     | 2024-07-24     |
| CARDIO-01-C01-007 | 2024-07-17     | 2024-07-30     |
| CARDIO-01-C01-008 | 2024-07-25     | NULL           |
+-------------------+----------------+----------------+
… 262 lignes au total (8 affichées)
```
<!-- /resultat -->

Les patients avec `date_inclusion` à NULL ont été **screenés** mais **pas inclus** : ils ne remplissaient pas les critères de l'étude (échec de screening).

**Ex 1.6** — (a) `etude_centre` ; (b) `investigateur.superviseur_id`, qui fait référence à `investigateur.id` (la table pointe sur elle-même : c'est une **auto-référence**).

**Ex 1.7** — a) LDD (`ALTER TABLE`) · b) LID (`SELECT`) · c) LMD (`INSERT`) · d) LMD (`DELETE`) · e) LDD (`CREATE TABLE`).
