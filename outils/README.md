# Outils de maintenance (formateur)

## `resultats.py` — résultats attendus automatiques

Les résultats affichés sous les requêtes du cours sont **calculés automatiquement** à partir de la base, pour qu'ils restent justes quand la base évolue.

```bash
python3 db/generate_data.py   # si la base a changé
python3 outils/resultats.py   # recalcule tous les résultats de cours/ et exercices/
```

Dans un fichier Markdown :

````markdown
```sql
SELECT COUNT(*) FROM patient;
```
<!-- resultat -->
````

Au lancement, l'outil exécute la requête et insère le résultat sous le marqueur (et le remplace aux lancements suivants).

- `<!-- resultat:30 -->` : affiche jusqu'à 30 lignes (12 par défaut).
- `<!-- exec -->` placé **avant** un bloc ```sql : exécute le bloc sans afficher de résultat (CREATE VIEW, INSERT… nécessaires à la suite du fichier).
- Chaque fichier repart d'une base neuve ; les blocs d'un même fichier s'enchaînent dans l'ordre.

L'outil s'appuie sur SQLite (inclus dans Python) en émulant les fonctions MySQL utilisées dans le cours (`YEAR`, `DATEDIFF`, `CONCAT`, `DATE_ADD`, `TIMESTAMPDIFF`…). L'affichage des décimales peut légèrement différer de celui de DBeaver.
