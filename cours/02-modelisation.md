# Module 2 — Modélisation et intégrité

> **Objectif** : choisir les bons types de données, concevoir une base relationnelle (MCD → MLD → tables), poser les contraintes qui garantissent la cohérence des données, et savoir sauvegarder / restaurer une base.
> **Durée indicative** : 5 h

---

## 2.1 Choisir les types de données

### Concept

Chaque colonne a un **type** : il fixe ce qu'on peut y stocker, la place occupée et les opérations possibles (on additionne des nombres, on compare des dates…). Un bon type est la **première contrainte d'intégrité** : impossible de stocker « douze » dans une colonne `INT`.

### Visuel — les familles de types

```
                          TYPES DE DONNÉES
       ┌──────────────────┬──────┴─────────┬───────────────────┐
   NUMÉRIQUES           TEXTE         DATES / HEURES         BOOLÉEN
       │                  │                │                   │
  ┌────┴─────┐       ┌────┴────┐      ┌────┼────────┐          │
 entiers   décimaux  CHAR(n) VARCHAR(n) DATE TIME DATETIME   BOOLEAN
 INT       DECIMAL(p,s)  fixe   variable                    (TRUE/FALSE)
 SMALLINT  (exact)               TEXT (long)
 TINYINT   FLOAT/DOUBLE
 BIGINT    (approché)
```

| Type | Contenu | Exemple dans la base | Quand l'utiliser |
|---|---|---|---|
| `INT` | Entier (±2 milliards) | `patient.id`, `objectif_inclusions` | Identifiants, compteurs |
| `SMALLINT` / `TINYINT` | Petits entiers | `annee_naissance`, `grade` | Valeurs bornées (gain de place) |
| `DECIMAL(p,s)` | Décimal **exact** : *p* chiffres dont *s* après la virgule | `mesure.valeur DECIMAL(7,2)` → jusqu'à 99999.99 | Montants, mesures : **toujours** pour l'argent |
| `FLOAT` / `DOUBLE` | Décimal **approché** | — | Calcul scientifique (jamais pour de l'argent) |
| `CHAR(n)` | Texte de longueur **fixe** | `sexe CHAR(1)` | Codes de longueur constante |
| `VARCHAR(n)` | Texte de longueur **variable**, max *n* | `nom VARCHAR(50)` | La plupart des textes |
| `TEXT` | Texte long | — | Commentaires libres, descriptions |
| `DATE` | Date `AAAA-MM-JJ` | `date_inclusion` | Dates sans heure |
| `DATETIME` / `TIMESTAMP` | Date + heure | — | Horodatage d'un événement |
| `BOOLEAN` | Vrai / faux | `grave` | Indicateurs oui/non |

### Exemples de choix raisonnés

| Donnée | ❌ Mauvais choix | ✅ Bon choix | Pourquoi |
|---|---|---|---|
| Code postal `01500` | `INT` | `CHAR(5)` | `INT` perdrait le zéro initial ; on ne calcule pas sur un code postal |
| Prix `12,99 €` | `FLOAT` | `DECIMAL(10,2)` | `FLOAT` donne 12.9899997… |
| Date d'inclusion | `VARCHAR(10)` | `DATE` | Avec un texte, impossible de calculer un délai ou de trier correctement « 2/1/2025 » et « 10/12/2024 » |
| Numéro de téléphone | `INT` | `VARCHAR(20)` | `+33 6…`, zéros initiaux, espaces |
| Âge | `INT` | *ne pas le stocker !* | Il change chaque année : on stocke la **date / année de naissance** et on calcule l'âge |

### La valeur NULL

`NULL` = **absence de valeur** (inconnue, non applicable, pas encore renseignée). Chaque colonne est déclarée :
- `NOT NULL` : valeur obligatoire ;
- `NULL` (par défaut) : valeur facultative.

Dans notre base, les NULL ont un **sens métier** précis (`date_inclusion` NULL = échec de screening). Documentez toujours ce que signifie un NULL dans vos colonnes.

---

## 2.2 Du MCD au MLD puis aux tables

### Concept

Concevoir une base se fait en trois niveaux (méthode **Merise**, très utilisée en France) :

```
 ┌───────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
 │ MCD                       │    │ MLD                      │    │ MPD                      │
 │ Modèle Conceptuel         │ ─► │ Modèle Logique           │ ─► │ Modèle Physique          │
 │ « de quoi parle-t-on ? »  │    │ « quelles tables ? »     │    │ « quel code SQL ? »      │
 │ entités, associations,    │    │ tables, colonnes,        │    │ CREATE TABLE, types,     │
 │ cardinalités              │    │ clés primaires/étrangères│    │ contraintes, index       │
 │ (indépendant de l'outil)  │    │                          │    │ (propre au SGBD)         │
 └───────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

**Vocabulaire du MCD**

| Terme | Définition | Exemple |
|---|---|---|
| **Entité** | Un « objet » du métier, décrit par des propriétés | ÉTUDE, CENTRE, PATIENT |
| **Identifiant** | Propriété qui distingue chaque occurrence | n° d'étude |
| **Association** | Un lien entre entités, nommé par un verbe | un centre *participe à* une étude |
| **Cardinalités** | Combien de fois, au minimum et au maximum, une occurrence participe à l'association | (0,n), (1,1)… |

### Visuel — le MCD de notre base (extrait)

```
 ┌─────────────┐                                     ┌─────────────┐
 │   ÉTUDE     │ 0,n      ╭──────────────────╮  0,n  │   CENTRE    │
 │─────────────│──────────│   PARTICIPER     │───────│─────────────│
 │ id_etude    │          │ date_ouverture   │       │ id_centre   │
 │ code        │          │ objectif         │       │ nom         │
 │ titre       │          ╰──────────────────╯       │ ville       │
 │ phase       │                                     │ pays        │
 └─────────────┘                                     └─────────────┘
       │ 0,n                                               │ 0,n
       │           ╭───────────╮                           │
       └───────────│  INCLURE  │                           │
                   ╰───────────╯                           │
                         │ 1,1                             │
                   ┌─────────────┐  1,1  ╭──────────╮      │
                   │  PATIENT    │───────│ RECRUTER │──────┘
                   │─────────────│       ╰──────────╯
                   │ id_patient  │
                   │ code        │
                   │ sexe        │
                   └─────────────┘
```

Lecture des cardinalités (on lit **depuis l'entité**, vers l'association) :
- **ÉTUDE — 0,n — PARTICIPER** : une étude se déroule dans **0 à n** centres (0 : pas encore de centre).
- **CENTRE — 0,n — PARTICIPER** : un centre participe à **0 à n** études.
- **PATIENT — 1,1 — INCLURE** : un patient appartient à **une et une seule** étude.
- **ÉTUDE — 0,n — INCLURE** : une étude a **0 à n** patients.

### Les règles de passage MCD → MLD

```
 RÈGLE 1 : chaque entité devient une table ; son identifiant devient la clé primaire.

 RÈGLE 2 : association « 1,1 ── x,n » (un-à-plusieurs)
           → la clé du côté « n » descend comme CLÉ ÉTRANGÈRE dans la table du côté « 1,1 »

     ETUDE (0,n) ── INCLURE ── (1,1) PATIENT     ⟹   patient(…, #etude_id)

 RÈGLE 3 : association « x,n ── x,n » (plusieurs-à-plusieurs)
           → elle devient une TABLE D'ASSOCIATION, dont la clé primaire est
             composée des deux clés étrangères ; ses propriétés deviennent des colonnes

     ETUDE (0,n) ── PARTICIPER ── (0,n) CENTRE   ⟹   etude_centre(#etude_id, #centre_id,
                                                                    date_ouverture, objectif)
```

### Le MLD obtenu

Notation : clé primaire **soulignée** (ici entre `_ _`), clé étrangère précédée de `#`.

```
etude          (_id_, code, titre, phase, aire_therapeutique, promoteur, date_debut, …)
centre         (_id_, nom, ville, pays)
investigateur  (_id_, nom, prenom, specialite, email, #centre_id, #superviseur_id)
etude_centre   (_#etude_id, #centre_id_, #investigateur_principal_id, date_ouverture, objectif_inclusions)
patient        (_id_, code_patient, #etude_id, #centre_id, sexe, annee_naissance, …)
visite         (_id_, #patient_id, type_visite, date_prevue, date_realisee)
evenement_indesirable (_id_, #patient_id, date_survenue, terme, grade, grave, …)
mesure         (_id_, #visite_id, parametre, valeur, unite)
```

---

## 2.3 Les contraintes d'intégrité

### Concept

Une **contrainte** est une règle que le SGBD **vérifie à chaque écriture**. Si une instruction la viole, elle est **refusée**. C'est ce qui fait qu'une base reste fiable même avec beaucoup d'utilisateurs.

| Contrainte | Garantit que… | Exemple dans la base |
|---|---|---|
| `PRIMARY KEY` | chaque ligne est unique et identifiable (unique + non NULL) | `etude.id` |
| `FOREIGN KEY … REFERENCES` | la valeur existe dans la table référencée (**intégrité référentielle**) | `patient.etude_id → etude.id` |
| `UNIQUE` | pas de doublon (NULL autorisé) | `etude.code`, `investigateur.email` |
| `NOT NULL` | la valeur est obligatoire | `patient.sexe` |
| `CHECK (condition)` | la valeur respecte une règle | `sexe IN ('F','M')`, `grade BETWEEN 1 AND 5` |
| `DEFAULT valeur` | valeur utilisée si on n'en fournit pas | `centre.pays DEFAULT 'France'` |

### Visuel — l'intégrité référentielle

```
     etude (table PARENT)                    patient (table ENFANT)
   ┌────┬───────────┐                   ┌────┬──────────────┬──────────┐
   │ id │ code      │                   │ id │ code_patient │ etude_id │
   ├────┼───────────┤                   ├────┼──────────────┼──────────┤
   │ 1  │ CARDIO-01 │ ◄──────────────── │ 1  │ CARDIO-…-001 │ 1        │  ✔
   │ 2  │ DIAB-02   │ ◄──────────────── │ 90 │ DIAB-…-001   │ 2        │  ✔
   └────┴───────────┘          ✗        │ ?? │ XXX-…-001    │ 99       │  ✘ refusé : l'étude 99
                                        └────┴──────────────┴──────────┘     n'existe pas

   et dans l'autre sens : supprimer l'étude 1 est REFUSÉ tant que des patients y font référence
```

### Exemples — voir les contraintes en action

Essayez ces instructions : elles doivent **toutes échouer**. Lisez attentivement les messages d'erreur, c'est une compétence en soi.

**1. Valeur interdite par un CHECK**

```sql
INSERT INTO patient (code_patient, etude_id, centre_id, sexe, annee_naissance, date_screening)
VALUES ('TEST-001', 1, 1, 'X', 1980, '2026-06-01');
```

```text
ERROR 3819 (HY000): Check constraint 'ck_patient_sexe' is violated.
```

**2. Doublon sur une colonne UNIQUE**

```sql
INSERT INTO etude (code, titre, phase, aire_therapeutique, promoteur, objectif_inclusions)
VALUES ('CARDIO-01', 'Doublon', 'II', 'Cardiologie', 'Test', 10);
```

```text
ERROR 1062 (23000): Duplicate entry 'CARDIO-01' for key 'etude.uq_etude_code'
```

**3. Clé étrangère vers une ligne inexistante**

```sql
INSERT INTO patient (code_patient, etude_id, centre_id, sexe, annee_naissance, date_screening)
VALUES ('TEST-002', 99, 1, 'F', 1980, '2026-06-01');
```

```text
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails
(`essais_cliniques`.`patient`, CONSTRAINT `fk_patient_etude` FOREIGN KEY (`etude_id`) REFERENCES `etude` (`id`))
```

**4. Supprimer une ligne « parent » encore référencée**

```sql
DELETE FROM centre WHERE id = 1;
```

```text
ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails
(`essais_cliniques`.`investigateur`, CONSTRAINT `fk_investigateur_centre` …)
```

**5. Valeur obligatoire absente**

```sql
INSERT INTO centre (nom, ville) VALUES (NULL, 'Rennes');
```

```text
ERROR 1048 (23000): Column 'nom' cannot be null
```

**6. Et la valeur par défaut ?** Celle-ci **réussit** : `pays` n'est pas fourni, il prend sa valeur `DEFAULT 'France'`.

```sql
INSERT INTO centre (nom, ville) VALUES ('Clinique de Bretagne', 'Rennes');
SELECT * FROM centre WHERE ville = 'Rennes';
```
<!-- resultat -->
```text
+----+----------------------+--------+--------+
| id | nom                  | ville  | pays   |
+----+----------------------+--------+--------+
| 9  | Clinique de Bretagne | Rennes | France |
+----+----------------------+--------+--------+
1 ligne
```
<!-- /resultat -->

> 🔄 Pour retirer ce centre de test : `DELETE FROM centre WHERE ville = 'Rennes';` (ou [remettez la base à zéro](00-accueil.md#remettre-la-base-à-zéro)).

**7. Une contrainte composée** — un patient doit appartenir à un centre **qui participe à son étude** : c'est la clé étrangère composée `fk_patient_etude_centre (etude_id, centre_id) → etude_centre`. Le centre 8 (Liège) ne participe pas à CARDIO-01 :

```sql
INSERT INTO patient (code_patient, etude_id, centre_id, sexe, annee_naissance, date_screening)
VALUES ('TEST-003', 1, 8, 'M', 1970, '2026-06-01');
```

```text
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails
(`essais_cliniques`.`patient`, CONSTRAINT `fk_patient_etude_centre` …)
```

### Que se passe-t-il quand on supprime un parent ? `ON DELETE`

Quand on déclare une clé étrangère, on peut choisir le comportement :

| Option | Effet si on supprime le parent | Usage |
|---|---|---|
| `RESTRICT` / `NO ACTION` (défaut) | **Refusé** tant qu'il existe des enfants | Le plus sûr : c'est le choix de notre base |
| `CASCADE` | Les enfants sont **supprimés aussi** | Données « détail » sans valeur seule (lignes d'une commande) |
| `SET NULL` | La clé étrangère des enfants passe à NULL | Lien facultatif (ex. superviseur parti) |

```sql
-- exemple de déclaration
CONSTRAINT fk_mesure_visite FOREIGN KEY (visite_id)
    REFERENCES visite (id)
    ON DELETE CASCADE      -- supprimer une visite supprime ses mesures
    ON UPDATE CASCADE      -- si l'id de la visite change, il est répercuté
```

> ⚠️ `CASCADE` est puissant et dangereux : un `DELETE` peut effacer des milliers de lignes en chaîne.

---

## 2.4 Créer, modifier, supprimer des tables (LDD)

### `CREATE TABLE`

Syntaxe générale :

```
CREATE TABLE nom_table (
    colonne1  TYPE  [NOT NULL] [DEFAULT valeur],
    colonne2  TYPE  …,
    …,
    CONSTRAINT nom_contrainte PRIMARY KEY (colonne),
    CONSTRAINT nom_contrainte FOREIGN KEY (colonne) REFERENCES autre_table (colonne),
    CONSTRAINT nom_contrainte UNIQUE (colonne),
    CONSTRAINT nom_contrainte CHECK (condition)
);
```

> 💡 Nommer ses contraintes (`CONSTRAINT ck_patient_sexe …`) est facultatif mais rend les messages d'erreur bien plus clairs.

**Exemple** — notre base doit maintenant gérer les **médicaments** étudiés. On crée la table :

```sql
CREATE TABLE medicament (
    id            INT          NOT NULL AUTO_INCREMENT,
    code          VARCHAR(10)  NOT NULL,
    dci           VARCHAR(100) NOT NULL,          -- nom de la molécule
    forme         VARCHAR(30)  NOT NULL DEFAULT 'comprimé',
    dosage_mg     DECIMAL(8,2) NULL,
    CONSTRAINT pk_medicament      PRIMARY KEY (id),
    CONSTRAINT uq_medicament_code UNIQUE (code),
    CONSTRAINT ck_medicament_dose CHECK (dosage_mg > 0)
);
```

`AUTO_INCREMENT` : MySQL attribue automatiquement le prochain numéro à chaque insertion.

### `ALTER TABLE`

```sql
-- ajouter une colonne
ALTER TABLE etude ADD COLUMN medicament_id INT NULL;

-- ajouter une contrainte
ALTER TABLE etude
    ADD CONSTRAINT fk_etude_medicament FOREIGN KEY (medicament_id) REFERENCES medicament (id);

-- modifier le type d'une colonne (MySQL)
ALTER TABLE medicament MODIFY COLUMN dci VARCHAR(150) NOT NULL;

-- renommer une colonne
ALTER TABLE medicament RENAME COLUMN dci TO molecule;

-- supprimer une contrainte puis une colonne
ALTER TABLE etude DROP FOREIGN KEY fk_etude_medicament;
ALTER TABLE etude DROP COLUMN medicament_id;
```

### `DROP TABLE` et `TRUNCATE`

```sql
DROP TABLE medicament;            -- supprime la table ET ses données, définitivement
DROP TABLE IF EXISTS medicament;  -- sans erreur si elle n'existe pas
```

> ⚠️ Il n'y a **pas de corbeille**. Un `DROP` est irréversible (d'où la section 2.6 sur les sauvegardes).

---

## 2.5 La normalisation en pratique

### Concept

**Normaliser**, c'est organiser les tables pour que **chaque information soit stockée une seule fois, au bon endroit**. On parle de « formes normales ». Retenez-en l'esprit avec trois règles :

| Forme | Règle (simplifiée) | Exemple de violation |
|---|---|---|
| **1FN** | Une case = **une seule valeur** (pas de liste) | `centres = 'Tours, Nantes, Lyon'` dans `etude` |
| **2FN** | Dans une table à clé composée, chaque colonne dépend de **toute** la clé | `etude_centre(etude_id, centre_id, ville_du_centre)` : la ville ne dépend que du centre |
| **3FN** | Une colonne ne dépend **que de la clé**, pas d'une autre colonne | `patient(…, centre_id, nom_centre)` : `nom_centre` dépend de `centre_id` |

### Visuel — corriger une violation de 1FN

```
 ✘  etude                                 ✔  etude            etude_centre        centre
 ┌───────────┬───────────────────┐        ┌────┬─────────┐   ┌───────┬────────┐   ┌────┬────────┐
 │ code      │ centres           │        │ id │ code    │   │etude_id│centre_id│  │ id │ ville  │
 ├───────────┼───────────────────┤   ⟹    ├────┼─────────┤   ├───────┼────────┤   ├────┼────────┤
 │ CARDIO-01 │ Tours,Nantes,Lyon │        │ 1  │CARDIO-01│   │ 1     │ 1      │   │ 1  │ Tours  │
 └───────────┴───────────────────┘        └────┴─────────┘   │ 1     │ 2      │   │ 2  │ Nantes │
   impossible de compter les centres,                        │ 1     │ 4      │   │ 4  │ Lyon   │
   de filtrer « études à Lyon »…                             └───────┴────────┘   └────┴────────┘
```

> 💡 **Dénormaliser** volontairement existe (tables d'entrepôt de données, exports pour Excel) : c'est justement ce que l'on fera avec les **vues** au module 6, sans dupliquer les données.

---

## 2.6 Sauvegarde et restauration

### Concept

Une **sauvegarde** (« dump ») est un fichier `.sql` contenant les instructions pour **recréer** la structure et les données. Le fichier `db/essais_cliniques.sql` que vous avez chargé est exactement cela.

### Avec DBeaver

- **Sauvegarder** : clic droit sur la base → **Outils → Dump database** → choisir le dossier → *Démarrer*.
- **Restaurer** : clic droit sur la connexion → **Outils → Restore database** → choisir le fichier `.sql`. (Ou : ouvrir le fichier et l'exécuter avec **Alt + X**, comme au module 0.)

### En ligne de commande (outils fournis avec MySQL)

```bash
# sauvegarder toute la base (structure + données)
mysqldump -u root -p essais_cliniques > sauvegarde_2026-06-30.sql

# sauvegarder la structure seulement
mysqldump -u root -p --no-data essais_cliniques > structure.sql

# sauvegarder une seule table
mysqldump -u root -p essais_cliniques patient > patient.sql

# restaurer
mysql -u root -p essais_cliniques < sauvegarde_2026-06-30.sql
```

### Copie rapide d'une table avant une manipulation risquée

```sql
CREATE TABLE patient_sauvegarde AS SELECT * FROM patient;
```

(Cette syntaxe est détaillée au module 4. Attention : elle copie les données mais **pas** les clés ni les contraintes.)

---

## À vous

👉 Exercices : [`exercices/02-modelisation.md`](../exercices/02-modelisation.md)

---

## Pièges

- **Stocker des nombres dans du texte** (`VARCHAR`) : le tri devient alphabétique (`'10' < '9'`) et les calculs impossibles ou faux.
- **`FLOAT` pour des montants** : arrondis invisibles. Utilisez `DECIMAL`.
- **Stocker une donnée calculable** (âge, total) : elle devient fausse dès que la source change.
- **Oublier l'ordre de création** : on crée la table **parent** avant la table **enfant** (la clé étrangère doit pointer vers une table existante), et on les supprime dans l'ordre inverse.
- **`UNIQUE` n'interdit pas NULL** : plusieurs lignes peuvent avoir NULL dans une colonne UNIQUE.
- **Une clé étrangère doit avoir le même type** que la clé primaire référencée (`INT` → `INT`).

> ### ⚖️ Standard vs MySQL
> | Besoin | SQL standard | MySQL |
> |---|---|---|
> | Numérotation automatique | `id INT GENERATED ALWAYS AS IDENTITY` | `id INT AUTO_INCREMENT` |
> | Booléen | `BOOLEAN` | `BOOLEAN` = alias de `TINYINT(1)` (stocke 0 / 1) |
> | Modifier une colonne | `ALTER TABLE t ALTER COLUMN c …` | `ALTER TABLE t MODIFY COLUMN c …` |
> | Supprimer une clé étrangère | `ALTER TABLE t DROP CONSTRAINT fk` | `ALTER TABLE t DROP FOREIGN KEY fk` (MySQL ≥ 8.0.19 accepte aussi `DROP CONSTRAINT`) |
> | Liste de valeurs autorisées | `CHECK (col IN (…))` | idem, ou le type non standard `ENUM('F','M')` |
> | `CHECK` | toujours vérifié | vérifié seulement depuis MySQL **8.0.16** (ignoré avant !) |

---

## Quiz

1. Quel type choisir pour stocker un montant en euros ?
   - a) `FLOAT`  - b) `INT`  - c) `DECIMAL(10,2)`  - d) `VARCHAR(10)`

2. Une association plusieurs-à-plusieurs (0,n — 0,n) entre deux entités devient, dans le MLD :
   - a) une clé étrangère dans l'une des deux tables
   - b) une table d'association dont la clé primaire est composée des deux clés étrangères
   - c) une colonne contenant une liste de valeurs
   - d) une fusion des deux tables

3. Quelle contrainte empêche d'enregistrer un patient dans une étude qui n'existe pas ?
   - a) `UNIQUE`  - b) `CHECK`  - c) `FOREIGN KEY`  - d) `DEFAULT`

4. Que fait `ON DELETE CASCADE` sur `mesure.visite_id` ?
   - a) Interdit de supprimer une visite qui a des mesures
   - b) Supprime automatiquement les mesures quand on supprime leur visite
   - c) Met `visite_id` à NULL dans les mesures
   - d) Supprime la visite quand on supprime une de ses mesures

5. Laquelle de ces structures viole la première forme normale ?
   - a) `patient(id, code, etude_id)`
   - b) `etude(id, code, liste_centres)` avec `liste_centres = 'Tours;Lyon'`
   - c) `centre(id, nom, ville, pays)`
   - d) `etude_centre(etude_id, centre_id, date_ouverture)`

<details>
<summary>Réponses</summary>

1. **c**. 2. **b**. 3. **c**. 4. **b**. 5. **b** — une case contient plusieurs valeurs.
</details>

---

## Côté métier

En tant qu'utilisateur (et non concepteur) d'une base, ce module vous sert surtout à :
- **lire un schéma** pour savoir comment relier les tables dans vos requêtes ;
- **comprendre un message d'erreur** quand une insertion est refusée ;
- **dialoguer avec les informaticiens** (« il faudrait une contrainte UNIQUE sur le code patient », « cette colonne devrait être en DATE ») ;
- et surtout : **ne jamais travailler sans sauvegarde** avant une modification.

---

⬅️ [Module 1](01-concepts.md) · ➡️ [Module 3 — Requêtes simples](03-requetes-simples.md)
