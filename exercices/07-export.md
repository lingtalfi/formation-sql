# Exercices — Module 7 : Préparer ses données pour Excel et Power BI

> Corrigés : [`solutions/07-export.md`](solutions/07-export.md)
> Les exercices 7.2 à 7.4 se font dans Excel (ou Power BI Desktop).

**Ex 7.1** ⭐⭐ — Créer une vue `v_export_ei` au **format long**, prête pour Power BI : une ligne par événement indésirable, avec son identifiant, le code de l'étude, le centre, le pays, le code patient, le bras, le terme, le grade, un indicateur `grave` valant 1 ou 0, la date de survenue, la date de résolution et la durée en jours (NULL si non résolu).

**Ex 7.2** ⭐ — **Constater le problème.** Exécuter `SELECT * FROM v_export_ei;` dans DBeaver, puis exporter le résultat en **CSV avec les réglages par défaut** (clic droit sur la grille → *Exporter les données* → CSV). Ouvrir le fichier en **double-cliquant** dessus. Dans une cellule libre, essayer `=ANNEE(J2)` (ou la colonne qui contient la date de survenue) et `=SOMME(I:I)` (la colonne `grave`). Noter tout ce qui ne va pas : colonnes, accents, dates, nombres.

**Ex 7.3** ⭐⭐ — **Corriger avec Power Query.** Dans un nouveau classeur, importer le même CSV via **Données → À partir d'un fichier texte/CSV**. Régler l'origine du fichier et le délimiteur, puis dans **Transformer les données**, typer les colonnes de date en *Date* (avec les paramètres régionaux adaptés) et `grade`, `grave`, `duree_jours` en *Nombre entier*. Charger, puis vérifier que `=ANNEE(…)` et `=SOMME(…)` fonctionnent.

**Ex 7.4** ⭐ — Refaire l'export, cette fois en **XLSX**. Comparer avec l'exercice 7.2.

**Ex 7.5** ⭐⭐⭐ — Créer une vue `v_kpi_inclusions_mensuelles` au format long : étude, mois (une **vraie date** : le 1er jour du mois, pour qu'Excel et Power BI la reconnaissent et puissent faire des axes chronologiques), bras, nombre d'inclusions. *(Indice : `STR_TO_DATE(DATE_FORMAT(d, '%Y-%m-01'), '%Y-%m-%d')`.)*

**Ex 7.6** ⭐⭐ — **Connexion directe** (si vous avez Excel ou Power BI et le pilote MySQL) : se connecter à la base et charger `v_kpi_inclusions_mensuelles` sans passer par un fichier. Construire un graphique en courbes des inclusions par mois. Modifier ensuite une date d'inclusion dans la base (module 5), cliquer sur **Actualiser** : le graphique suit.

**Ex 7.7 (réflexion)** — Pour chacun de ces besoins, dire s'il vaut mieux le calculer dans une vue SQL ou dans l'outil (Excel / Power BI), et pourquoi :
- a) « un patient est en échec de screening si sa date d'inclusion est vide » ;
- b) le pourcentage d'EI graves, selon les filtres que l'utilisateur choisit (étude, pays, période) ;
- c) la durée d'un EI en jours ;
- d) la couleur rouge des centres sous 50 % de leur objectif.
