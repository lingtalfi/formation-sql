# Exercices — Module 3 : Requêtes simples

> Corrigés : [`solutions/03-requetes-simples.md`](solutions/03-requetes-simples.md)
> Niveaux : ⭐ application directe · ⭐⭐ combinaison · ⭐⭐⭐ réflexion

## SELECT, WHERE, ORDER BY

**Ex 3.1** ⭐ — Afficher le code, la phase et le promoteur des études, triés par phase puis par code.

**Ex 3.2** ⭐ — Lister les investigateurs (nom, prénom) dont la spécialité est la cardiologie.

**Ex 3.3** ⭐ — Lister les patientes (sexe `F`) de l'étude 2, triées par année de naissance décroissante.

**Ex 3.4** ⭐ — Lister les visites de type `V6` réalisées en 2025 (id, patient, date réalisée).

**Ex 3.5** ⭐⭐ — Lister les patients sortis prématurément de l'étude, c'est-à-dire sortis pour un autre motif que la fin d'étude (code, date de sortie, motif).

**Ex 3.6** ⭐⭐ — Lister les visites **manquées** : date prévue antérieure au 30/06/2026 et non réalisées. Afficher les 10 plus anciennes.

**Ex 3.7** ⭐⭐ — Lister les événements indésirables de grade 2 ou plus, **non résolus**, dont le lien avec le traitement est « certain », « probable » ou « possible ».

## Fonctions

**Ex 3.8** ⭐ — Afficher pour chaque investigateur une colonne `nom_complet` au format `Dr Claire MARTIN`.

**Ex 3.9** ⭐⭐ — Pour chaque patient inclus, afficher son code, sa date d'inclusion et la date prévue de sa visite de fin à 336 jours (`date_fin_theorique`).

**Ex 3.10** ⭐⭐ — Afficher, pour chaque événement indésirable résolu, sa durée en jours. Quels sont les 5 plus longs ?

**Ex 3.11** ⭐⭐ — Afficher le code des patients et une colonne `generation` : « avant 1950 », « 1950-1969 », « 1970 et après ».

## Agrégats, GROUP BY, HAVING

**Ex 3.12** ⭐ — Combien d'événements indésirables ont été déclarés au total ? Combien sont graves ? Combien sont non résolus ?

**Ex 3.13** ⭐ — Nombre d'investigateurs par spécialité, du plus grand nombre au plus petit.

**Ex 3.14** ⭐⭐ — Pour chaque étude (`etude_id`), le nombre de patients sortis et le nombre de patients encore en cours (inclus et non sortis).

**Ex 3.15** ⭐⭐ — Délai moyen (en jours, arrondi à 1 décimale) entre screening et inclusion, par étude.

**Ex 3.16** ⭐⭐ — Pour l'étude 1, le nombre d'inclusions par année.

**Ex 3.17** ⭐⭐ — Les patients ayant déclaré au moins 3 événements indésirables (identifiant du patient, nombre).

**Ex 3.18** ⭐⭐⭐ — Taux de visites manquées par type de visite (`V1`…`V6`), parmi les visites dont la date prévue est passée. Arrondir à 1 décimale.

## Sous-requêtes

**Ex 3.19** ⭐⭐ — Lister les études (code, titre) qui n'ont encore aucun patient.

**Ex 3.20** ⭐⭐ — Lister les investigateurs qui ne sont investigateur principal d'aucune étude.

**Ex 3.21** ⭐⭐ — Les patients ayant au moins un relevé de poids supérieur à 100 kg : afficher seulement leur code. *(Indice : `mesure` → `visite` → `patient`, avec deux `IN` imbriqués.)*

**Ex 3.22** ⭐⭐⭐ — Les centres (`etude_id`, `centre_id`) dont le nombre d'inclus est **inférieur à la moitié** de leur objectif.

**Ex 3.23** ⭐⭐⭐ — Pour chaque terme d'EI, le nombre d'occurrences et la part (en %) qu'il représente dans le total des EI.
