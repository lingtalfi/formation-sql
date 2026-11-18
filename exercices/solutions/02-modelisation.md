# Corrigés — Module 2 : Modélisation et intégrité

**Ex 2.1**

| Donnée | Type | Remarque |
|---|---|---|
| a) numéro de lot | `VARCHAR(20)` | contient lettres et tirets |
| b) température | `DECIMAL(3,1)` | exact, 1 décimale (jusqu'à 99.9) |
| c) date et heure | `DATETIME` | |
| d) fumeur | `BOOLEAN` | |
| e) nombre de comprimés | `SMALLINT` ou `INT` | entier positif (ajouter `CHECK (… >= 0)`) |
| f) commentaire | `TEXT` ou `VARCHAR(1000)` | |

**Ex 2.2**
- a) ❌ `grade` = 6 viole `ck_ei_grade` (`grade BETWEEN 1 AND 5`) → `ERROR 3819`.
- b) ✅ `grave` prend sa valeur par défaut `FALSE`, `date_resolution` reste NULL.
- c) ❌ le patient 1 a déjà une visite `V0` : la contrainte `UNIQUE (patient_id, type_visite)` est violée → `ERROR 1062`. *(Si le patient 1 était un échec de screening sans visite, l'insertion réussirait.)*
- d) ❌ DERM-05 est référencée par `etude_centre` → `ERROR 1451` (intégrité référentielle). Bien qu'elle n'ait aucun patient, ses centres prévus y font référence.
- e) ❌ cet email existe déjà (`uq_investigateur_email`) → `ERROR 1062`.

Vérifiez l'email existant :

```sql
SELECT email FROM investigateur WHERE id = 1;
```
<!-- resultat -->
```text
+-------------------------------------+
| email                               |
+-------------------------------------+
| claire.martin@loire-centre1.example |
+-------------------------------------+
1 ligne
```
<!-- /resultat -->

**Ex 2.3 — MCD**

```
 ┌─────────────┐ 0,n  ╭────────────╮ 0,1  ┌──────────────────┐
 │  MONITEUR   │──────│ SURVEILLER │──────│ ÉTUDE_CENTRE (*) │
 │─────────────│      ╰────────────╯      └──────────────────┘
 │ id_moniteur │                                 │ 0,n
 │ nom         │                          ╭──────────────╮
 │ prenom      │                          │   CONCERNER  │
 │ email       │                          ╰──────────────╯
 └─────────────┘                                 │ 1,1
       │ 0,n         ╭──────────╮ 1,1   ┌──────────────────────┐
       └─────────────│ RÉALISER │───────│  VISITE_MONITORING   │
                     ╰──────────╯       │──────────────────────│
                                        │ id                   │
 (*) ÉTUDE_CENTRE est ici traitée       │ date_visite          │
     comme une entité (elle a déjà      │ nb_anomalies         │
     une identité propre dans la base)  └──────────────────────┘
```

MLD :

```
moniteur          (_id_, nom, prenom, email)
etude_centre      (_#etude_id, #centre_id_, …, #moniteur_id)            ← 0,1 : clé étrangère facultative
visite_monitoring (_id_, #moniteur_id, #etude_id, #centre_id, date_visite, nb_anomalies)
```

**Ex 2.4**

```sql
CREATE TABLE moniteur (
    id     INT          NOT NULL AUTO_INCREMENT,
    nom    VARCHAR(50)  NOT NULL,
    prenom VARCHAR(50)  NOT NULL,
    email  VARCHAR(100) NOT NULL,
    CONSTRAINT pk_moniteur       PRIMARY KEY (id),
    CONSTRAINT uq_moniteur_email UNIQUE (email)
);

CREATE TABLE visite_monitoring (
    id           INT  NOT NULL AUTO_INCREMENT,
    moniteur_id  INT  NOT NULL,
    etude_id     INT  NOT NULL,
    centre_id    INT  NOT NULL,
    date_visite  DATE NOT NULL,
    nb_anomalies INT  NOT NULL DEFAULT 0,
    CONSTRAINT pk_visite_monitoring PRIMARY KEY (id),
    CONSTRAINT fk_vm_moniteur       FOREIGN KEY (moniteur_id) REFERENCES moniteur (id),
    CONSTRAINT fk_vm_etude_centre   FOREIGN KEY (etude_id, centre_id) REFERENCES etude_centre (etude_id, centre_id),
    CONSTRAINT ck_vm_anomalies      CHECK (nb_anomalies >= 0)
);

ALTER TABLE etude_centre ADD COLUMN moniteur_id INT NULL;
ALTER TABLE etude_centre
    ADD CONSTRAINT fk_etude_centre_moniteur FOREIGN KEY (moniteur_id) REFERENCES moniteur (id);
```

Ordre : `moniteur` doit exister avant `visite_monitoring` et avant la clé étrangère de `etude_centre`.

**Ex 2.5 — Problèmes repérés**
- `visites_faites` et `ei` contiennent **plusieurs valeurs** par case → violation de la 1FN. Il faut une ligne par visite (table `visite`) et une ligne par EI (table `evenement_indesirable`).
- `promoteur`, `centre`, `ville_centre` sont **répétés** à chaque patient, et déjà **incohérents** (« Laboratoires Alvéa » / « Labo Alvéa », « Clinique du Val de Loire » / « Clinique Val de Loire ») → violation de la 3FN : ces informations dépendent de l'étude ou du centre, pas du patient. Il faut des tables `etude` et `centre`, et le patient n'en garde que les clés (`etude_id`, `centre_id`).
- `grade` est noyé dans le texte de l'EI : il doit être une colonne numérique à part.

C'est exactement la structure de notre base `essais_cliniques`.

**Ex 2.6**

b)
```bash
mysqldump -u root -p essais_cliniques evenement_indesirable > evenement_indesirable.sql
```

c)
<!-- exec -->
```sql
CREATE TABLE visite_copie AS SELECT * FROM visite;
```

```sql
SELECT
    (SELECT COUNT(*) FROM visite)       AS nb_visite,
    (SELECT COUNT(*) FROM visite_copie) AS nb_visite_copie;
```
<!-- resultat -->
```text
+-----------+-----------------+
| nb_visite | nb_visite_copie |
+-----------+-----------------+
| 1308      | 1308            |
+-----------+-----------------+
1 ligne
```
<!-- /resultat -->

```sql
DROP TABLE visite_copie;
```

**Ex 2.7**

a) MCD

```
 ┌───────────────┐ 0,n  ╭──────────────────╮ 0,n  ┌─────────┐
 │   PERSONNE    │──────│    PARTICIPER    │──────│  ÉTUDE  │
 │───────────────│      │──────────────────│      └─────────┘
 │ id_personne   │      │ date_inclusion   │
 │ nom           │      │ bras             │
 │ prenom        │      │ date_sortie      │
 │ date_naissance│      │ motif_sortie     │
 │ sexe          │      ╰──────────────────╯
 └───────────────┘
```

Une personne participe à 0..n études ; une étude a 0..n participants : association plusieurs-à-plusieurs. (Le centre est aussi lié à chaque participation : en toute rigueur, l'association relie PERSONNE, ÉTUDE et CENTRE.)

b) MLD

```
personne      (_id_, nom, prenom, date_naissance, sexe)
participation (_id_, #personne_id, #etude_id, #centre_id, code_patient,
               date_screening, date_inclusion, bras, date_sortie, motif_sortie)
visite        (_id_, #participation_id, type_visite, date_prevue, date_realisee)
evenement_indesirable (_id_, #participation_id, …)
```

On donne à `participation` sa propre clé `id` (plutôt qu'une clé composée `personne_id, etude_id`) car d'autres tables la référencent, et parce qu'une personne pourrait en théorie être screenée deux fois pour la même étude.

Les visites et les EI se rattachent à la **participation** : une visite V3 n'a de sens que dans le calendrier d'une étude précise, et un EI doit être déclaré dans l'étude pendant laquelle il survient (en particulier pour comparer le bras traitement et le bras placebo).

c)

```sql
SELECT pe.id, pe.nom, pe.prenom, COUNT(DISTINCT pa.etude_id) AS nb_etudes
FROM personne pe
JOIN participation pa ON pa.personne_id = pe.id
GROUP BY pe.id, pe.nom, pe.prenom
HAVING COUNT(DISTINCT pa.etude_id) >= 2;
```

(Cette requête porte sur le modèle imaginé dans l'exercice : elle ne s'exécute pas sur `essais_cliniques`.)

