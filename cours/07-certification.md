# Module 7 — Préparation à la certification et bonus « indicateurs »

> **Objectif** : consolider les acquis pour l'examen (SQL standard), s'entraîner en conditions réelles, et découvrir des techniques avancées très utiles pour produire des indicateurs.
> **Durée indicative** : 4 h

---

## 7.1 L'examen en bref

| | |
|---|---|
| **Certification** | « Langage SQL : Exploiter une base de données relationnelle » (RS7205, Éditions ENI) |
| **Format** | en ligne, à distance |
| **Contenu** | des **cas pratiques** et des **questions** QCM (plusieurs bonnes réponses possibles) / QCU (une seule) |
| **Langage évalué** | le **SQL standard**, sans référence à un SGBD particulier |

**Conseils**
- Lisez chaque question **deux fois** : un « NOT », un « sauf », un « au moins » changent tout.
- Dans un QCM, chaque proposition est à évaluer **indépendamment**.
- Méfiez-vous des syntaxes **propres à MySQL** (`LIMIT`, `CONCAT`, `DATEDIFF`, `AUTO_INCREMENT`…) quand la question porte sur le standard : la fiche 7.2 les résume.
- Pour une requête à écrire : partez du `FROM` (quelles tables ?), puis `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `ORDER BY`.

---

## 7.2 Fiche de synthèse

### La requête `SELECT` complète

```
SELECT [DISTINCT] colonnes, expressions, agrégats [AS alias]       ⑤
FROM table [AS] t                                                  ①
     [INNER | LEFT | RIGHT | FULL] JOIN autre a ON condition         ①
WHERE condition sur les lignes                                     ②
GROUP BY colonnes                                                  ③
HAVING condition sur les groupes                                   ④
ORDER BY colonnes [ASC | DESC]                                     ⑥
LIMIT n  /  FETCH FIRST n ROWS ONLY                                ⑦
                                       ① … ⑦ = ordre logique d'exécution
```

### Les autres instructions

```
INSERT INTO t (c1, c2) VALUES (v1, v2), (v3, v4);
INSERT INTO t (c1, c2) SELECT … ;
UPDATE t SET c1 = v1, c2 = v2 WHERE … ;
DELETE FROM t WHERE … ;

CREATE TABLE t (c1 TYPE [NOT NULL] [DEFAULT v], …, CONSTRAINT … PRIMARY KEY (…), …);
ALTER TABLE t ADD c TYPE;   ALTER TABLE t DROP COLUMN c;
DROP TABLE t;
CREATE VIEW v AS SELECT … ;          DROP VIEW v;

START TRANSACTION;  …  COMMIT;   |   ROLLBACK;
```

### Standard vs MySQL : le tableau à connaître

| Thème | SQL standard | MySQL |
|---|---|---|
| Limiter les lignes | `FETCH FIRST n ROWS ONLY`, `OFFSET n ROWS` | `LIMIT n OFFSET m` |
| Concaténer | `a \|\| b` | `CONCAT(a, b)` (`\|\|` = OU logique) |
| Numérotation auto | `GENERATED ALWAYS AS IDENTITY` | `AUTO_INCREMENT` |
| Jointure complète | `FULL OUTER JOIN` | non supporté → `LEFT JOIN … UNION … RIGHT JOIN` |
| Créer une table depuis une requête | `SELECT … INTO t` (SQL Server) / `CREATE TABLE t AS SELECT` | `CREATE TABLE t AS SELECT` |
| Différence / intersection | `EXCEPT`, `INTERSECT` | depuis 8.0.31 ; sinon `NOT IN` / `IN` |
| Délimiter un identifiant | `"nom"` | `` `nom` `` |
| Extraire une partie de date | `EXTRACT(YEAR FROM d)` | aussi `YEAR(d)`, `MONTH(d)`… |
| Écart entre deux dates | selon SGBD | `DATEDIFF`, `TIMESTAMPDIFF` |
| Date du jour | `CURRENT_DATE` | aussi `CURDATE()` |
| Remplacer NULL | `COALESCE(a, b)` | aussi `IFNULL(a, b)` |
| Condition | `CASE WHEN … END` | aussi `IF(cond, a, b)` |
| Modifier une colonne | `ALTER TABLE t ALTER COLUMN …` | `ALTER TABLE t MODIFY COLUMN …` |
| Booléen | `BOOLEAN` | alias de `TINYINT(1)` |
| Vue matérialisée | `CREATE MATERIALIZED VIEW` (selon SGBD) | n'existe pas |
| Fusion insert/update | `MERGE` | `INSERT … ON DUPLICATE KEY UPDATE` |

### Les 10 pièges qui coûtent des points

1. `= NULL` au lieu de `IS NULL`.
2. `NOT IN` avec une sous-requête qui contient un NULL.
3. `COUNT(*)` vs `COUNT(colonne)`.
4. `AND` / `OR` sans parenthèses.
5. Agrégat dans `WHERE` au lieu de `HAVING`.
6. Colonne du `SELECT` absente du `GROUP BY`.
7. Alias du `SELECT` utilisé dans le `WHERE`.
8. Filtre sur la table de droite d'un `LEFT JOIN` placé dans le `WHERE`.
9. `UNION` (dédoublonne) vs `UNION ALL` (garde tout).
10. `BETWEEN` : bornes **incluses**.

---

## 7.3 Examen blanc

👉 [`quiz/examen-blanc.md`](../quiz/examen-blanc.md) — un cas pratique et 30 questions. Faites-le en temps limité (**1 h 30**), sans le cours, puis corrigez-vous avec [`quiz/examen-blanc-corrige.md`](../quiz/examen-blanc-corrige.md).

---

## 7.4 Bonus : les fonctions de fenêtrage

### Concept

Un agrégat avec `GROUP BY` **réduit** les lignes : une ligne par groupe. Une **fonction de fenêtrage** (`… OVER (…)`) calcule sur un groupe de lignes **sans les regrouper** : chaque ligne garde son détail **et** reçoit le résultat du calcul. Standard SQL, disponible depuis MySQL 8.

```
fonction() OVER (
    PARTITION BY colonnes     ← les « groupes » (facultatif)
    ORDER BY colonnes         ← l'ordre dans chaque groupe (pour les rangs, cumuls…)
)
```

### Visuel

```
   GROUP BY etude_id : 1 ligne par étude          OVER (PARTITION BY etude_id) : toutes les lignes gardées
  ┌──────────┬──────┐                             ┌──────────────┬──────────┬──────────────────────┐
  │ etude_id │ nb   │                             │ code_patient │ etude_id │ nb_dans_mon_etude    │
  ├──────────┼──────┤                             ├──────────────┼──────────┼──────────────────────┤
  │ 1        │ 136  │                             │ CARDIO-…-001 │ 1        │ 136                  │
  │ 2        │  64  │                             │ CARDIO-…-002 │ 1        │ 136                  │
  └──────────┴──────┘                             │ …            │ …        │ …                    │
                                                  │ DIAB-…-001   │ 2        │  64                  │
                                                  └──────────────┴──────────┴──────────────────────┘
```

### Fonctions principales

| Fonction | Rôle |
|---|---|
| `ROW_NUMBER()` | numéro 1, 2, 3… dans la partition |
| `RANK()` / `DENSE_RANK()` | rang, avec gestion des ex æquo (1, 1, 3 / 1, 1, 2) |
| `SUM(x) OVER (… ORDER BY …)` | **cumul** progressif |
| `AVG(x) OVER (…)`, `COUNT(*) OVER (…)` | agrégat sans regroupement |
| `LAG(x)` / `LEAD(x)` | valeur de la ligne **précédente** / **suivante** |

### Exemples

**Chaque patient du centre 6, avec le nombre de patients screenés de son étude dans ce centre** :

```sql
SELECT code_patient, etude_id,
       COUNT(*) OVER (PARTITION BY etude_id) AS screenes_etude
FROM patient
WHERE centre_id = 6
ORDER BY etude_id, code_patient
LIMIT 4;
```
<!-- resultat -->
```text
+-------------------+----------+----------------+
| code_patient      | etude_id | screenes_etude |
+-------------------+----------+----------------+
| CARDIO-01-C06-001 | 1        | 21             |
| CARDIO-01-C06-002 | 1        | 21             |
| CARDIO-01-C06-003 | 1        | 21             |
| CARDIO-01-C06-004 | 1        | 21             |
+-------------------+----------+----------------+
4 lignes
```
<!-- /resultat -->

La fenêtre est calculée **après** le `WHERE` : elle ne « voit » que les patients du centre 6 (21 pour CARDIO-01 dans ce centre, et non les 136 de l'étude).

**Le cumul des inclusions** (courbe de recrutement) pour DIAB-02 :

```sql
WITH par_mois AS (
    SELECT DATE_FORMAT(date_inclusion, '%Y-%m') AS mois, COUNT(*) AS inclusions
    FROM patient
    WHERE etude_id = 2 AND date_inclusion IS NOT NULL
    GROUP BY DATE_FORMAT(date_inclusion, '%Y-%m')
)
SELECT mois, inclusions,
       SUM(inclusions) OVER (ORDER BY mois) AS cumul
FROM par_mois
ORDER BY mois;
```
<!-- resultat:20 -->
```text
+---------+------------+-------+
| mois    | inclusions | cumul |
+---------+------------+-------+
| 2025-03 | 6          | 6     |
| 2025-04 | 4          | 10    |
| 2025-05 | 5          | 15    |
| 2025-06 | 2          | 17    |
| 2025-07 | 5          | 22    |
| 2025-08 | 3          | 25    |
| 2025-09 | 1          | 26    |
| 2025-10 | 3          | 29    |
| 2025-11 | 1          | 30    |
| 2025-12 | 6          | 36    |
| 2026-01 | 4          | 40    |
| 2026-02 | 2          | 42    |
| 2026-03 | 2          | 44    |
| 2026-04 | 2          | 46    |
| 2026-05 | 2          | 48    |
| 2026-06 | 1          | 49    |
+---------+------------+-------+
16 lignes
```
<!-- /resultat -->

**Le classement des centres par étude** :

```sql
SELECT e.code AS etude, c.nom AS centre, COUNT(p.date_inclusion) AS inclus,
       RANK() OVER (PARTITION BY e.code ORDER BY COUNT(p.date_inclusion) DESC) AS rang
FROM patient p
JOIN etude e  ON p.etude_id  = e.id
JOIN centre c ON p.centre_id = c.id
GROUP BY e.code, c.nom
ORDER BY etude, rang, centre;
```
<!-- resultat:20 -->
```text
+-----------+-----------------------------+--------+------+
| etude     | centre                      | inclus | rang |
+-----------+-----------------------------+--------+------+
| CARDIO-01 | Clinique du Val de Loire    | 33     | 1    |
| CARDIO-01 | Hôpital Saint-Roch          | 26     | 2    |
| CARDIO-01 | CHU Atlantique              | 21     | 3    |
| CARDIO-01 | Clinique du Léman           | 18     | 4    |
| CARDIO-01 | Centre Hospitalier du Rhône | 14     | 5    |
| DIAB-02   | Clinique des Flandres       | 19     | 1    |
| DIAB-02   | Clinique du Val de Loire    | 15     | 2    |
| DIAB-02   | Hôpital Saint-Roch          | 9      | 3    |
| DIAB-02   | Hospital del Sol            | 6      | 4    |
| NEURO-04  | CHU Atlantique              | 15     | 1    |
| NEURO-04  | Clinique du Val de Loire    | 15     | 1    |
| ONCO-03   | CHU Atlantique              | 10     | 1    |
| ONCO-03   | Centre Hospitalier du Rhône | 7      | 2    |
| ONCO-03   | Clinique du Léman           | 4      | 3    |
+-----------+-----------------------------+--------+------+
14 lignes
```
<!-- /resultat -->

**Le dernier relevé de poids de chaque patient** — un grand classique : numéroter les relevés du plus récent au plus ancien, puis garder le n° 1.

```sql
WITH releves AS (
    SELECT p.code_patient, v.date_realisee, m.valeur,
           ROW_NUMBER() OVER (PARTITION BY p.id ORDER BY v.date_realisee DESC) AS n
    FROM mesure m
    JOIN visite  v ON m.visite_id  = v.id
    JOIN patient p ON v.patient_id = p.id
    WHERE m.parametre = 'poids'
)
SELECT code_patient, date_realisee AS dernier_releve, valeur AS dernier_poids
FROM releves
WHERE n = 1
ORDER BY dernier_poids DESC, code_patient
LIMIT 5;
```
<!-- resultat -->
```text
+-------------------+----------------+---------------+
| code_patient      | dernier_releve | dernier_poids |
+-------------------+----------------+---------------+
| NEURO-04-C01-009  | 2023-06-20     | 109.6         |
| CARDIO-01-C01-007 | 2025-01-21     | 104           |
| DIAB-02-C05-007   | 2026-03-15     | 102.3         |
| ONCO-03-C04-010   | 2026-05-26     | 102.2         |
| CARDIO-01-C03-009 | 2025-03-19     | 100.4         |
+-------------------+----------------+---------------+
5 lignes
```
<!-- /resultat -->

**L'évolution d'une visite à l'autre avec `LAG`** — la tension d'un patient, et la variation depuis la visite précédente :

```sql
SELECT v.type_visite, v.date_realisee, m.valeur AS pas,
       m.valeur - LAG(m.valeur) OVER (ORDER BY v.date_realisee) AS variation
FROM mesure m
JOIN visite v ON m.visite_id = v.id
WHERE v.patient_id = 3 AND m.parametre = 'pas'
ORDER BY v.date_realisee;
```
<!-- resultat -->
```text
+-------------+---------------+-----+-----------+
| type_visite | date_realisee | pas | variation |
+-------------+---------------+-----+-----------+
| V0          | 2024-05-18    | 140 | NULL      |
| V1          | 2024-06-01    | 137 | -3        |
| V3          | 2024-07-20    | 141 | 4         |
| V4          | 2024-08-09    | 134 | -7        |
| V5          | 2024-11-09    | 136 | 2         |
| V6          | 2025-04-22    | 123 | -13       |
+-------------+---------------+-----+-----------+
6 lignes
```
<!-- /resultat -->

---

## 7.5 Bonus : le tableau croisé en SQL

Excel a ses tableaux croisés dynamiques ; en SQL, on « pivote » avec un **agrégat conditionnel** : une colonne par valeur, grâce à `SUM(CASE …)`.

```sql
SELECT e.code AS etude,
       SUM(CASE WHEN ei.grade = 1 THEN 1 ELSE 0 END) AS grade_1,
       SUM(CASE WHEN ei.grade = 2 THEN 1 ELSE 0 END) AS grade_2,
       SUM(CASE WHEN ei.grade = 3 THEN 1 ELSE 0 END) AS grade_3,
       SUM(CASE WHEN ei.grade = 4 THEN 1 ELSE 0 END) AS grade_4,
       COUNT(*)                                       AS total
FROM evenement_indesirable ei
JOIN patient p ON ei.patient_id = p.id
JOIN etude   e ON p.etude_id    = e.id
GROUP BY e.code
ORDER BY e.code;
```
<!-- resultat -->
```text
+-----------+---------+---------+---------+---------+-------+
| etude     | grade_1 | grade_2 | grade_3 | grade_4 | total |
+-----------+---------+---------+---------+---------+-------+
| CARDIO-01 | 56      | 34      | 13      | 4       | 107   |
| DIAB-02   | 22      | 16      | 6       | 3       | 47    |
| NEURO-04  | 15      | 6       | 6       | 1       | 28    |
| ONCO-03   | 8       | 12      | 3       | 3       | 26    |
+-----------+---------+---------+---------+---------+-------+
4 lignes
```
<!-- /resultat -->

```
   lignes                                       colonnes (pivot)
  ┌─────────┬───────┬────┐                     ┌─────────┬─────────┬─────────┬─────┐
  │ etude   │ grade │ nb │                     │ etude   │ grade_1 │ grade_2 │ …   │
  ├─────────┼───────┼────┤      SUM(CASE…)     ├─────────┼─────────┼─────────┼─────┤
  │ CARDIO  │ 1     │ 56 │  ────────────────►  │ CARDIO  │ 56      │ 34      │ …   │
  │ CARDIO  │ 2     │ 34 │                     │ DIAB    │ …       │ …       │ …   │
  │ …       │ …     │ …  │                     └─────────┴─────────┴─────────┴─────┘
  └─────────┴───────┴────┘
```

---

## 7.6 Bonus : du SQL vers Excel (et depuis VBA)

**Exporter un résultat depuis DBeaver** : clic droit sur la grille de résultats → **Exporter les données** → CSV ou Excel (XLSX). Pour un export récurrent, enregistrez la requête dans un fichier `.sql`.

**Brancher Excel sur la base** (données actualisables) :
1. Installer le pilote **MySQL Connector/ODBC** (site officiel de MySQL).
2. Dans Excel : *Données → Obtenir des données → À partir d'autres sources → ODBC* (ou *À partir d'une base de données MySQL* selon la version).
3. Choisir une **vue** (module 6) plutôt qu'une table : les indicateurs arrivent tout calculés.
4. *Actualiser tout* recharge les chiffres.

**Depuis VBA** : une macro peut exécuter une requête SQL via ADO et coller le résultat dans une feuille. Le principe :

```vba
' Référence nécessaire : Microsoft ActiveX Data Objects x.x Library
Dim cn As New ADODB.Connection, rs As New ADODB.Recordset
cn.Open "Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Database=essais_cliniques;User=root;Password=…;"
rs.Open "SELECT * FROM v_synthese_etude", cn
Sheets("Synthèse").Range("A2").CopyFromRecordset rs
rs.Close: cn.Close
```

> 💡 La bonne répartition des rôles : **SQL** pour filtrer, joindre et agréger (là où les données sont) ; **Excel / VBA** pour la mise en forme et la diffusion. Évitez de rapatrier 100 000 lignes dans Excel pour y faire un `RECHERCHEV` : une jointure fait mieux, plus vite.

---

## Quiz

1. Que renvoie `ROW_NUMBER() OVER (PARTITION BY etude_id ORDER BY date_inclusion)` ?
   - a) Le nombre de patients par étude
   - b) Le numéro d'ordre de chaque patient dans son étude, selon sa date d'inclusion
   - c) Une erreur sans `GROUP BY`
   - d) Le numéro de ligne global

2. Quelle est la différence entre `RANK()` et `DENSE_RANK()` pour les valeurs 10, 10, 8 (tri décroissant) ?
   - a) Aucune
   - b) `RANK` : 1, 1, 3 — `DENSE_RANK` : 1, 1, 2
   - c) `RANK` : 1, 2, 3 — `DENSE_RANK` : 1, 1, 2
   - d) `RANK` : 1, 1, 2 — `DENSE_RANK` : 1, 1, 3

3. En SQL standard, comment limiter un résultat aux 10 premières lignes ?
   - a) `LIMIT 10`  - b) `TOP 10`  - c) `FETCH FIRST 10 ROWS ONLY`  - d) `ROWNUM <= 10`

4. Quelle écriture produit une colonne par grade d'EI ?
   - a) `GROUP BY grade`
   - b) `SUM(CASE WHEN grade = 1 THEN 1 ELSE 0 END) AS grade_1, …`
   - c) `PIVOT grade`
   - d) `DISTINCT grade`

<details>
<summary>Réponses</summary>

1. **b**. 2. **b**. 3. **c** (`LIMIT` : MySQL/PostgreSQL ; `TOP` : SQL Server ; `ROWNUM` : Oracle). 4. **b**.
</details>

---

## Le mot de la fin

Vous savez maintenant :
- lire et comprendre la structure d'une base, ses clés et ses contraintes ;
- extraire, filtrer, trier, calculer et agréger ;
- combiner plusieurs tables ;
- modifier les données en sécurité ;
- enregistrer vos indicateurs sous forme de vues réutilisables.

La suite, c'est la pratique : reprenez les besoins que vous aviez notés au module 0 et écrivez-les en SQL. 💪

---

⬅️ [Module 6](06-vues.md) · 🏠 [Plan de la formation](../PLAN.md)
