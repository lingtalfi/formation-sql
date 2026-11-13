# Formation « Langage SQL »

Support de cours pour la certification **RS7205 – Langage SQL : Exploiter une base de données relationnelle** (Éditions ENI).

- Pratique sur **MySQL 8** avec le client **DBeaver**, en restant aligné sur le **SQL standard** évalué à l'examen.
- Tous les exemples utilisent une base d'entraînement unique et fictive : [`essais_cliniques`](db/README.md).
- Chaque chapitre : objectif → concept → visuel → exemples (avec résultat attendu) → exercices → pièges → quiz → côté métier.

## Démarrer

1. Installer MySQL 8 et DBeaver, puis charger [`db/essais_cliniques.sql`](db/essais_cliniques.sql) : voir le [module 0](cours/00-accueil.md).
2. Comprendre le domaine de la base (essais cliniques, acteurs, KPI), même sans rien y connaître : [**Comprendre la base**](db/comprendre-la-base.md).
3. Référence technique de la base (tables, colonnes, schéma) : [`db/README.md`](db/README.md).

## Sommaire

| Module | Cours | Exercices | Corrigés |
|---|---|---|---|
| 0 — Accueil, installation, positionnement | [cours](cours/00-accueil.md) | | |
| 1 — Concepts fondamentaux | [cours](cours/01-concepts.md) | [énoncés](exercices/01-concepts.md) | [corrigés](exercices/solutions/01-concepts.md) |
| 2 — Modélisation et intégrité | [cours](cours/02-modelisation.md) | [énoncés](exercices/02-modelisation.md) | [corrigés](exercices/solutions/02-modelisation.md) |
| 3 — Requêtes simples | [cours](cours/03-requetes-simples.md) | [énoncés](exercices/03-requetes-simples.md) | [corrigés](exercices/solutions/03-requetes-simples.md) |
| 4 — Requêtes multi-tables | [cours](cours/04-jointures.md) | [énoncés](exercices/04-jointures.md) | [corrigés](exercices/solutions/04-jointures.md) |
| 5 — Mise à jour des données | [cours](cours/05-mise-a-jour.md) | [énoncés](exercices/05-mise-a-jour.md) | [corrigés](exercices/solutions/05-mise-a-jour.md) |
| 6 — Création de vues | [cours](cours/06-vues.md) | [énoncés](exercices/06-vues.md) | [corrigés](exercices/solutions/06-vues.md) |
| 7 — Certification et bonus | [cours](cours/07-certification.md) | [examen blanc](quiz/examen-blanc.md) | [corrigé](quiz/examen-blanc-corrige.md) |

Plan détaillé et principes pédagogiques : [PLAN.md](PLAN.md).

## Organisation du dépôt

```
formation-sql/
├── README.md, PLAN.md
├── db/            ← la base d'entraînement (script à charger, schéma, générateur, documentation)
├── cours/         ← un fichier par module
├── exercices/     ← énoncés ; corrigés dans exercices/solutions/
├── quiz/          ← examen blanc et corrigé
└── outils/        ← outils du formateur (recalcul automatique des résultats affichés)
```

## Pour le formateur

Les résultats affichés sous les requêtes sont **générés automatiquement** à partir de la base. Après toute modification de la base ou d'une requête :

```bash
python3 db/generate_data.py     # si le générateur a changé
python3 outils/resultats.py     # recalcule tous les résultats
```

Détails : [`outils/README.md`](outils/README.md).
