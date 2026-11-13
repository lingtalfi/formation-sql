# Évolutions de la base `essais_cliniques`

## v1.0.1 — 2026-11-13
- Ajout de `SET NAMES utf8mb4;` en tête des scripts : corrige les accents mal enregistrés (« Ã© » au lieu de « é ») quand le script est chargé par un client MySQL réglé en latin1 (ex. : conteneur Docker). Données inchangées.

## v1.0 — 2026-11-13
- Création : tables `etude`, `centre`, `investigateur`, `etude_centre`, `patient`, `visite`, `evenement_indesirable`, `mesure`.
- Données générées par `generate_data.py` (graine 2026, date de référence 2026-06-30).
