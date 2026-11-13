# Exercices — Module 4 : Requêtes multi-tables

> Corrigés : [`solutions/04-jointures.md`](solutions/04-jointures.md)
> Niveaux : ⭐ application directe · ⭐⭐ combinaison · ⭐⭐⭐ réflexion

## INNER JOIN

**Ex 4.1** ⭐ — Afficher chaque investigateur (nom, prénom) avec le nom et la ville de son centre.

**Ex 4.2** ⭐ — Afficher les patients inclus de l'étude `ONCO-03` (code patient, bras, date d'inclusion) **en filtrant sur le code de l'étude**, pas sur son identifiant.

**Ex 4.3** ⭐⭐ — Nombre de patients inclus par **pays**.

**Ex 4.4** ⭐⭐ — Pour chaque **promoteur**, le nombre d'événements indésirables graves déclarés dans ses études.

**Ex 4.5** ⭐⭐ — Glycémie moyenne (arrondie à 2 décimales) par bras et par type de visite, pour l'étude `DIAB-02`.

**Ex 4.6** ⭐⭐ — Lister les visites manquées (date prévue passée, non réalisée) avec le code patient, le nom du centre et le code de l'étude, triées par centre.

## LEFT JOIN

**Ex 4.7** ⭐ — Tous les centres avec le nombre d'études auxquelles ils participent (0 compris).

**Ex 4.8** ⭐⭐ — Les patients inclus qui n'ont **aucune mesure** enregistrée.

**Ex 4.9** ⭐⭐ — Pour chaque étude (toutes), le nombre de patients **encore en cours** (inclus, non sortis).

**Ex 4.10** ⭐⭐⭐ — Pour chaque centre (tous), le nombre de visites réalisées **en 2026**. Attention à l'endroit où vous placez le filtre sur l'année.

## Auto-jointure, CROSS JOIN

**Ex 4.11** ⭐⭐ — Lister les investigateurs qui n'ont pas la même spécialité que leur superviseur (nom de l'investigateur, sa spécialité, nom du superviseur, spécialité du superviseur).

**Ex 4.12** ⭐⭐⭐ — Construire la grille de **tous** les types de visite (V0 à V6) × bras (traitement, placebo) pour l'étude `CARDIO-01`, avec le nombre de visites réalisées dans chaque case. *(Indice : les types de visite et les bras s'obtiennent avec `SELECT DISTINCT`.)*

## UNION

**Ex 4.13** ⭐⭐ — Produire une liste unique de « personnes » avec une colonne `role` : les investigateurs (`'investigateur'`, nom et prénom) et les patients inclus du centre 7 (`'patient'`, code patient à la place du nom, prénom vide).

**Ex 4.14** ⭐⭐ — Chronologie complète du patient `ONCO-03-C04-008` : visites (prévues et réalisées), EI, et sortie d'étude, triée par date.

## Tables temporaires, CTE

**Ex 4.15** ⭐⭐ — Créer une table temporaire `tmp_eig` contenant les EI graves avec le code patient, le code étude et la ville du centre. L'interroger pour obtenir le nombre d'EI graves par ville.

**Ex 4.16** ⭐⭐⭐ — Avec une CTE, calculer pour chaque patient de `CARDIO-01` ayant fait V0 **et** V6 la variation de PAS (valeur à V6 − valeur à V0), puis la variation moyenne par bras.

**Ex 4.17** ⭐⭐⭐ — Tableau de bord des centres pour `DIAB-02` : nom du centre, investigateur principal, objectif, inclus, % d'atteinte, nombre d'EI, nombre de visites manquées. Tous les centres de l'étude doivent apparaître.
