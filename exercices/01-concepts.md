# Exercices — Module 1 : Concepts fondamentaux

> Corrigés : [`solutions/01-concepts.md`](solutions/01-concepts.md)

**Ex 1.1** — Afficher tout le contenu de la table `investigateur`. Combien de lignes contient-elle ?

**Ex 1.2** — Afficher uniquement le nom, le prénom et la spécialité des investigateurs.

**Ex 1.3** — Afficher le contenu de la table `etude_centre`. Quelle est sa clé primaire ? Pourquoi n'a-t-elle pas de colonne `id` ?

**Ex 1.4** — Dans DBeaver, ouvrir la table `patient` (double-clic) puis l'onglet **Colonnes**. Lister les colonnes qui acceptent `NULL` et expliquer, pour chacune, ce que signifie une valeur absente (aidez-vous de `db/README.md`).

**Ex 1.5** — Afficher le code, la date de screening et la date d'inclusion des patients. Repérer quelques patients dont `date_inclusion` est NULL : que s'est-il passé pour eux ?

**Ex 1.6** — Afficher le diagramme ER de la base dans DBeaver. Retrouver sur ce diagramme : (a) la table qui relie `etude` et `centre` ; (b) la colonne qui permet de savoir qui supervise un investigateur.

**Ex 1.7 (réflexion)** — Pour chacun des besoins suivants, dire à quelle famille d'instructions (LDD, LMD, LID) il correspond :
- a) Ajouter une colonne `telephone` à la table `centre`
- b) Lister les patients de l'étude CARDIO-01
- c) Enregistrer un nouveau patient
- d) Supprimer une visite saisie par erreur
- e) Créer une nouvelle table `medicament`
