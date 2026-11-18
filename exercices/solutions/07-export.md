# Corrigés — Module 7 : Préparer ses données pour Excel et Power BI

**Ex 7.1**

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_export_ei AS
SELECT ei.id                                            AS ei_id,
       e.code                                           AS etude,
       c.nom                                            AS centre,
       c.pays,
       p.code_patient,
       p.bras,
       ei.terme,
       ei.grade,
       CASE WHEN ei.grave THEN 1 ELSE 0 END             AS grave,
       ei.date_survenue,
       ei.date_resolution,
       DATEDIFF(ei.date_resolution, ei.date_survenue)   AS duree_jours
FROM evenement_indesirable ei
JOIN patient p ON ei.patient_id = p.id
JOIN etude   e ON p.etude_id    = e.id
JOIN centre  c ON p.centre_id   = c.id;
```

```sql
SELECT * FROM v_export_ei ORDER BY ei_id LIMIT 3;
```
<!-- resultat -->
```text
+-------+-----------+--------------------------+--------+-------------------+---------+---------------------+-------+-------+---------------+-----------------+-------------+
| ei_id | etude     | centre                   | pays   | code_patient      | bras    | terme               | grade | grave | date_survenue | date_resolution | duree_jours |
+-------+-----------+--------------------------+--------+-------------------+---------+---------------------+-------+-------+---------------+-----------------+-------------+
| 1     | CARDIO-01 | Clinique du Val de Loire | France | CARDIO-01-C01-001 | placebo | Œdème des chevilles | 2     | 0     | 2024-06-11    | 2024-06-15      | 4           |
| 2     | CARDIO-01 | Clinique du Val de Loire | France | CARDIO-01-C01-006 | placebo | Nausées             | 2     | 0     | 2024-12-15    | 2025-01-09      | 25          |
| 3     | CARDIO-01 | Clinique du Val de Loire | France | CARDIO-01-C01-010 | placebo | Céphalées           | 1     | 0     | 2025-03-29    | 2025-04-02      | 4           |
+-------+-----------+--------------------------+--------+-------------------+---------+---------------------+-------+-------+---------------+-----------------+-------------+
3 lignes
```
<!-- /resultat -->

`grave` en 1/0 plutôt que `TRUE`/`FALSE` ou `'oui'`/`'non'` : l'outil peut directement en faire la **somme** (nombre d'EI graves) ou la **moyenne** (proportion d'EI graves).

**Ex 7.2** — Avec un Excel réglé en français, on observe généralement :
- toutes les valeurs dans la colonne A (séparateur `,` au lieu de `;`) — ou, si le séparateur est bon :
- des accents abîmés (`CÃ©phalÃ©es`) si le fichier est en UTF-8 sans BOM ;
- des dates alignées à gauche : ce sont des **textes**, `=ANNEE(…)` renvoie `#VALEUR!` ;
- selon les réglages, des nombres eux aussi lus comme du texte.

Le fichier n'est pas « faux » : c'est Excel qui devine mal, faute d'information sur les types (voir le tableau des symptômes en 7.7).

**Ex 7.3** — Points clés : *Origine du fichier* = `65001 : Unicode (UTF-8)` ; *Délimiteur* = celui du fichier ; pour les colonnes de dates : clic droit → **Modifier le type → Utilisation des paramètres régionaux…** → *Date*, **Anglais (États-Unis)** (si les dates sont au format `AAAA-MM-JJ` ou `AAAA-MM-JJ hh:mm:ss`, choisir alors *Date/Heure* puis *Date*). Après chargement, les dates sont alignées à droite et les formules fonctionnent. Les étapes étant enregistrées, il suffit ensuite de remplacer le CSV et de cliquer sur **Actualiser**.

**Ex 7.4** — L'export XLSX conserve les types : dates et nombres sont reconnus immédiatement, les accents sont corrects. En revanche, c'est une photo à l'instant T : pour des données à jour, il faut refaire l'export (contrairement à la connexion directe de l'exercice 7.6).

**Ex 7.5**

<!-- exec -->
```sql
CREATE OR REPLACE VIEW v_kpi_inclusions_mensuelles AS
SELECT e.code                                                          AS etude,
       STR_TO_DATE(DATE_FORMAT(p.date_inclusion, '%Y-%m-01'), '%Y-%m-%d') AS mois,
       p.bras,
       COUNT(*)                                                        AS inclusions
FROM patient p
JOIN etude e ON p.etude_id = e.id
WHERE p.date_inclusion IS NOT NULL
GROUP BY e.code, STR_TO_DATE(DATE_FORMAT(p.date_inclusion, '%Y-%m-01'), '%Y-%m-%d'), p.bras;
```

```sql
SELECT * FROM v_kpi_inclusions_mensuelles
WHERE etude = 'DIAB-02' AND mois >= '2026-01-01'
ORDER BY mois, bras;
```
<!-- resultat:20 -->
```text
+---------+------------+------------+------------+
| etude   | mois       | bras       | inclusions |
+---------+------------+------------+------------+
| DIAB-02 | 2026-01-01 | placebo    | 2          |
| DIAB-02 | 2026-01-01 | traitement | 2          |
| DIAB-02 | 2026-02-01 | placebo    | 2          |
| DIAB-02 | 2026-03-01 | placebo    | 2          |
| DIAB-02 | 2026-04-01 | placebo    | 1          |
| DIAB-02 | 2026-04-01 | traitement | 1          |
| DIAB-02 | 2026-05-01 | placebo    | 2          |
| DIAB-02 | 2026-06-01 | traitement | 1          |
+---------+------------+------------+------------+
8 lignes
```
<!-- /resultat -->

`DATE_FORMAT(…, '%Y-%m-01')` ramène chaque date au 1er du mois, mais renvoie du **texte** ; `STR_TO_DATE` le reconvertit en **date**. Excel et Power BI reçoivent ainsi une vraie colonne de dates, utilisable pour un axe chronologique ou un filtre par période.

**Ex 7.6** — Pas de corrigé SQL : vérifiez simplement qu'après **Actualiser**, le graphique reflète la modification faite dans la base. C'est tout l'intérêt de la connexion directe à une vue.

**Ex 7.7**
- a) **Vue SQL** : c'est une règle métier, elle doit être la même pour tout le monde et pour tous les rapports.
- b) **Outil** (mesure DAX dans Power BI, ou TCD dans Excel) : le résultat dépend des filtres choisis à l'écran. La vue fournit les ingrédients (une ligne par EI, `grave` = 1/0) et l'outil calcule `moyenne(grave)` dans le contexte du filtre.
- c) **Vue SQL** : calcul simple, ligne par ligne, utile partout (cf. `duree_jours` dans `v_export_ei`).
- d) **Outil** : c'est de la mise en forme (mise en forme conditionnelle). La vue peut toutefois fournir le seuil ou un indicateur `en_retard` (1/0) si la règle doit être partagée.
