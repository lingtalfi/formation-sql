# Exercices — Module 2 : Modélisation et intégrité

> Corrigés : [`solutions/02-modelisation.md`](solutions/02-modelisation.md)
> 🔄 Ces exercices modifient la structure : [remettez la base à zéro](../cours/00-accueil.md#remettre-la-base-à-zéro) à la fin.

**Ex 2.1 — Choisir les types.** Proposer un type SQL pour chacune de ces données : a) le numéro de lot d'un médicament (`LOT-2025-00412`) ; b) la température corporelle (`37,8`) ; c) la date et l'heure exacte d'une prise de sang ; d) le fait qu'un patient soit fumeur ; e) le nombre de comprimés délivrés ; f) un commentaire libre de l'investigateur.

**Ex 2.2 — Prédire les erreurs.** Pour chaque instruction, dire si elle réussit ou échoue, et pourquoi (sans l'exécuter, puis vérifier) :

```sql
-- a)
INSERT INTO evenement_indesirable (patient_id, date_survenue, terme, grade, lien_traitement)
VALUES (1, '2026-06-01', 'Céphalées', 6, 'possible');
-- b)
INSERT INTO evenement_indesirable (patient_id, date_survenue, terme, grade, lien_traitement)
VALUES (1, '2026-06-01', 'Céphalées', 2, 'possible');
-- c)
INSERT INTO visite (patient_id, type_visite, date_prevue) VALUES (1, 'V0', '2026-07-01');
-- d)
DELETE FROM etude WHERE code = 'DERM-05';
-- e)
INSERT INTO investigateur (nom, prenom, specialite, email, centre_id)
VALUES ('Test', 'Jean', 'Cardiologie', 'claire.martin@loire-centre1.example', 1);
```

**Ex 2.3 — MCD.** Le promoteur veut suivre les **moniteurs** (ou ARC : attachés de recherche clinique), qui vont contrôler les données dans les centres. Règles :
- un moniteur a un nom, un prénom, un email (unique) ;
- un moniteur surveille un ou plusieurs couples (étude, centre) ; un couple (étude, centre) est surveillé par un seul moniteur à un instant donné ;
- chaque visite de monitoring a une date et un nombre d'anomalies relevées.

Dessiner le MCD (entités, associations, cardinalités) puis en déduire le MLD.

**Ex 2.4 — CREATE TABLE.** Écrire les instructions `CREATE TABLE` correspondant à votre MLD de l'exercice 2.3 (tables `moniteur` et `visite_monitoring`), avec : clés primaires, clés étrangères, email unique, nombre d'anomalies ≥ 0 et valant 0 par défaut. Ajouter dans `etude_centre` une colonne `moniteur_id` (facultative) avec sa clé étrangère.

**Ex 2.5 — Normalisation.** Une collègue vous transmet ce tableau Excel et veut le « mettre en base ». Repérer les problèmes et proposer une structure en plusieurs tables.

| code_patient | etude | promoteur | centre | ville_centre | visites_faites | ei |
|---|---|---|---|---|---|---|
| CARDIO-01-C01-001 | CARDIO-01 | Laboratoires Alvéa | Clinique du Val de Loire | Tours | V0, V1, V2 | Céphalées (grade 1); Toux (grade 2) |
| CARDIO-01-C01-002 | CARDIO-01 | Labo Alvéa | Clinique Val de Loire | Tours | V0 | |

**Ex 2.6 — Sauvegarde.** a) Faire un dump complet de `essais_cliniques` avec DBeaver. b) Écrire la commande `mysqldump` qui sauvegarde uniquement la table `evenement_indesirable`. c) Créer par SQL une copie de la table `visite` nommée `visite_copie`, vérifier qu'elle contient autant de lignes que l'originale, puis la supprimer.
