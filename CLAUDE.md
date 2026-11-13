# Conventions du dépôt

- Formation SQL **générique et réutilisable** (certification RS7205 / ENI). Ne jamais citer de stagiaire nommément.
- Contenu rédigé **en français**.
- Pratique sur MySQL 8 + DBeaver ; chaque chapitre signale les écarts avec le SQL standard (encadré « Standard vs MySQL »).
- Une **seule base d'entraînement**, `essais_cliniques` (données fictives), utilisée par tous les exemples. Toute évolution du schéma passe par `db/` et est notée dans `db/CHANGELOG.md`.
- Gabarit de chapitre : Objectif → Concept → Visuel → Exemples → À vous → Pièges → Quiz → Côté métier.
- Visuels : schémas en texte (box-drawing) ou Mermaid.
