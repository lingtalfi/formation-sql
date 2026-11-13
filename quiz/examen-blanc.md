# Examen blanc — Langage SQL

> **Durée conseillée** : 1 h 30 · sans le cours · corrigé : [`examen-blanc-corrige.md`](examen-blanc-corrige.md)
> Partie A : cas pratique sur la base `essais_cliniques` (requêtes à écrire et exécuter).
> Partie B : 30 questions. **QCU** = une seule bonne réponse ; **QCM** = une ou plusieurs bonnes réponses.
> Sauf mention contraire, les questions de la partie B portent sur le **SQL standard**.

---

## Partie A — Cas pratique (40 min)

Le promoteur **Laboratoires Alvéa** prépare son comité de pilotage. Écrivez les requêtes qui répondent à ses questions.

**A1.** Lister les études du promoteur (code, titre, phase, statut), triées par date de début.

**A2.** Pour chacune de ces études, le nombre de centres participants et le nombre total de patients inclus.

**A3.** Les patients de ces études sortis prématurément (motif autre que la fin d'étude) : code patient, étude, ville du centre, date et motif de sortie.

**A4.** Le nombre d'événements indésirables graves par étude **et** par bras, en incluant les combinaisons à 0.

**A5.** Le centre (toutes études Alvéa confondues) qui a le **meilleur** taux d'atteinte de son objectif d'inclusion.

**A6.** Créer une vue `v_alvea_visites_manquees` listant les visites manquées (date prévue passée au 30/06/2026, non réalisées) des études Alvéa, avec étude, centre, code patient, type de visite et nombre de jours de retard au 30/06/2026.

**A7.** À partir de la vue A6, le nombre de visites manquées par centre, uniquement pour les centres qui en ont au moins 5.

**A8.** Le comité décide de porter l'objectif d'inclusions d'`ONCO-03` à 75. Écrire l'instruction, dans une transaction, puis la vérification.

---

## Partie B — Questions (50 min)

**B1. (QCU)** Quelle instruction appartient au langage de définition des données (LDD) ?
- a) `SELECT`  - b) `UPDATE`  - c) `ALTER TABLE`  - d) `COMMIT`

**B2. (QCM)** Quelles affirmations sur une clé primaire sont vraies ?
- a) Elle peut contenir NULL
- b) Elle identifie chaque ligne de façon unique
- c) Elle peut être composée de plusieurs colonnes
- d) Une table peut avoir plusieurs clés primaires

**B3. (QCU)** Une association de cardinalités (0,n) — (0,n) entre ÉTUDE et CENTRE devient dans le modèle logique :
- a) une clé étrangère `centre_id` dans `etude`
- b) une clé étrangère `etude_id` dans `centre`
- c) une table `etude_centre (etude_id, centre_id)`
- d) une fusion des deux tables

**B4. (QCU)** Quel type convient le mieux à un montant de 1 234,56 € ?
- a) `FLOAT`  - b) `DECIMAL(8,2)`  - c) `VARCHAR(10)`  - d) `INT`

**B5. (QCM)** Quelles contraintes empêchent une valeur NULL ?
- a) `PRIMARY KEY`  - b) `UNIQUE`  - c) `NOT NULL`  - d) `FOREIGN KEY`

**B6. (QCU)** La table `ventes` contient 10 lignes, dont 3 avec `montant` NULL. Que renvoie `SELECT COUNT(montant) FROM ventes` ?
- a) 10  - b) 7  - c) 3  - d) NULL

**B7. (QCU)** Avec les mêmes données, les 7 montants valent tous 10. Que renvoie `SELECT AVG(montant) FROM ventes` ?
- a) 7  - b) 10  - c) 70  - d) NULL

**B8. (QCU)** Que renvoie `SELECT * FROM patient WHERE date_inclusion = NULL` ?
- a) Les patients non inclus
- b) Les patients inclus
- c) Aucune ligne
- d) Une erreur de syntaxe

**B9. (QCM)** Quelles conditions sont équivalentes à `grade BETWEEN 2 AND 4` ?
- a) `grade >= 2 AND grade <= 4`
- b) `grade IN (2, 3, 4)` (si `grade` est entier)
- c) `grade > 2 AND grade < 4`
- d) `NOT (grade < 2 OR grade > 4)`

**B10. (QCU)** `WHERE nom LIKE '_a%'` sélectionne les noms :
- a) qui commencent par « a »
- b) dont la deuxième lettre est « a »
- c) qui contiennent « _a »
- d) qui se terminent par « a »

**B11. (QCU)** Quelle clause filtre des groupes après agrégation ?
- a) `WHERE`  - b) `HAVING`  - c) `GROUP BY`  - d) `ORDER BY`

**B12. (QCU)** Cette requête est-elle correcte ?
```sql
SELECT etude_id, sexe, COUNT(*) FROM patient GROUP BY etude_id;
```
- a) Oui
- b) Non : `sexe` n'est ni dans le `GROUP BY`, ni agrégé
- c) Non : `COUNT(*)` est interdit avec `GROUP BY`
- d) Non : il manque `HAVING`

**B13. (QCU)** Dans quel ordre logique ces clauses sont-elles évaluées ?
- a) SELECT → FROM → WHERE → GROUP BY
- b) FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
- c) FROM → GROUP BY → WHERE → SELECT → HAVING
- d) WHERE → FROM → SELECT → ORDER BY

**B14. (QCU)** Comment écrire, en SQL standard, « les 5 premières lignes » ?
- a) `LIMIT 5`  - b) `TOP 5`  - c) `FETCH FIRST 5 ROWS ONLY`  - d) `ROWNUM = 5`

**B15. (QCU)** La table A a 4 lignes, la table B en a 6. Combien de lignes renvoie `SELECT * FROM A CROSS JOIN B` ?
- a) 4  - b) 6  - c) 10  - d) 24

**B16. (QCU)** Pour lister **toutes** les études avec leurs éventuels patients, on écrit :
- a) `FROM etude e INNER JOIN patient p ON p.etude_id = e.id`
- b) `FROM etude e LEFT JOIN patient p ON p.etude_id = e.id`
- c) `FROM patient p LEFT JOIN etude e ON p.etude_id = e.id`
- d) `FROM etude e, patient p`

**B17. (QCM)** Comment obtenir les centres qui n'ont **aucun** patient ?
- a) `SELECT c.* FROM centre c LEFT JOIN patient p ON p.centre_id = c.id WHERE p.id IS NULL`
- b) `SELECT * FROM centre WHERE id NOT IN (SELECT centre_id FROM patient)`
- c) `SELECT * FROM centre c WHERE NOT EXISTS (SELECT 1 FROM patient p WHERE p.centre_id = c.id)`
- d) `SELECT c.* FROM centre c INNER JOIN patient p ON p.centre_id = c.id WHERE p.id IS NULL`

**B18. (QCU)** Que garde un `FULL OUTER JOIN` ?
- a) Seulement les lignes qui se correspondent
- b) Toutes les lignes de la table de gauche
- c) Toutes les lignes des deux tables
- d) Le produit cartésien

**B19. (QCU)** Une auto-jointure, c'est :
- a) une jointure générée automatiquement par le SGBD
- b) la jointure d'une table avec elle-même, grâce à deux alias
- c) une jointure sans condition
- d) une jointure sur la clé primaire

**B20. (QCU)** `SELECT ville FROM centre UNION SELECT ville FROM centre` renvoie :
- a) chaque ville deux fois
- b) chaque ville une seule fois
- c) une erreur
- d) aucune ligne

**B21. (QCU)** Quelle syntaxe crée une nouvelle table `archive` à partir d'une requête en SQL Server, mais n'est **pas** acceptée par MySQL ?
- a) `CREATE TABLE archive AS SELECT …`
- b) `SELECT … INTO archive FROM …`
- c) `INSERT INTO archive SELECT …`
- d) `CREATE VIEW archive AS SELECT …`

**B22. (QCU)** Une table temporaire :
- a) est visible par tous les utilisateurs jusqu'au redémarrage du serveur
- b) disparaît à la fin de la session qui l'a créée
- c) ne peut pas être interrogée avec `SELECT`
- d) est automatiquement mise à jour quand les tables sources changent

**B23. (QCU)** Que fait `UPDATE patient SET bras = 'placebo';` ?
- a) Erreur : `WHERE` obligatoire
- b) Modifie tous les patients
- c) Ne modifie que les patients sans bras
- d) Ne fait rien

**B24. (QCM)** Quelles instructions insèrent correctement une ligne dans `centre (id AUTO, nom, ville, pays DEFAULT 'France')` ?
- a) `INSERT INTO centre (nom, ville) VALUES ('X', 'Brest');`
- b) `INSERT INTO centre VALUES ('X', 'Brest');`
- c) `INSERT INTO centre (nom, ville, pays) VALUES ('X', 'Brest', 'France');`
- d) `INSERT centre SET nom = 'X', ville = 'Brest';` *(en SQL standard)*

**B25. (QCU)** Pourquoi `DELETE FROM etude WHERE id = 1` peut-il échouer ?
- a) `DELETE` exige `TABLE`
- b) Des lignes d'autres tables référencent cette étude par une clé étrangère
- c) On ne peut supprimer qu'avec `TRUNCATE`
- d) La clé primaire ne peut pas être utilisée dans un `WHERE`

**B26. (QCU)** Après `START TRANSACTION; DELETE FROM mesure; ROLLBACK;` :
- a) la table `mesure` est vide
- b) la table `mesure` est inchangée
- c) la table `mesure` est supprimée
- d) seule la première ligne est supprimée

**B27. (QCM)** Quelles affirmations sur les vues sont vraies ?
- a) Une vue stocke une copie des données
- b) Une vue s'interroge comme une table
- c) Une vue reflète toujours les données actuelles des tables
- d) Une vue peut contenir des jointures et des agrégats

**B28. (QCU)** Quelle option empêche d'insérer, via une vue, une ligne qui ne vérifierait pas le `WHERE` de la vue ?
- a) `WITH READ ONLY`  - b) `WITH CHECK OPTION`  - c) `WITH GRANT OPTION`  - d) `RESTRICT`

**B29. (QCU)** `COALESCE(NULL, NULL, 'a', 'b')` renvoie :
- a) NULL  - b) `'a'`  - c) `'b'`  - d) `'ab'`

**B30. (QCU)** Une sous-requête utilisée après `IN` doit renvoyer :
- a) une seule valeur
- b) une seule colonne
- c) plusieurs colonnes
- d) exactement une ligne
