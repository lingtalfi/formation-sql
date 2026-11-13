# Exercices — Module 6 : Création de vues

> Corrigés : [`solutions/06-vues.md`](solutions/06-vues.md)
> Les exercices s'appuient sur les vues créées dans le cours (`v_patient_detail`, `v_tableau_de_bord_*`). Créez-les d'abord si ce n'est pas fait.

**Ex 6.1** ⭐ — Créer une vue `v_investigateur_detail` : nom complet (`Prénom NOM`), spécialité, centre, ville, pays, nom complet du superviseur (NULL pour les chefs).

**Ex 6.2** ⭐ — À partir de `v_investigateur_detail`, lister les investigateurs exerçant hors de France.

**Ex 6.3** ⭐⭐ — Créer une vue `v_ei_detail` : identifiant de l'EI, code étude, code patient, bras, ville du centre, terme, grade, grave (`'oui'` / `'non'`), date de survenue, durée en jours (NULL si non résolu), statut (`'résolu'` / `'en cours'`).

**Ex 6.4** ⭐⭐ — À partir de `v_ei_detail` : les EI dont le terme contient « douleur » ou commence par « Vert », survenus entre le 1er janvier et le 30 juin 2026.

**Ex 6.5** ⭐⭐ — À partir de `v_ei_detail` : durée moyenne des EI résolus par grade.

**Ex 6.6** ⭐⭐ — Créer une vue `v_inclusions_mensuelles` (étude, mois `AAAA-MM`, nombre d'inclusions). L'utiliser pour trouver, pour chaque étude, le meilleur mois de recrutement.

**Ex 6.7** ⭐⭐⭐ — Créer une vue `v_derniere_visite` donnant pour chaque patient inclus la date de sa dernière visite **réalisée** et le type de cette visite. *(Indice : une sous-requête corrélée avec `MAX`.)* Puis l'utiliser pour lister les patients en cours dont la dernière visite remonte à plus de 120 jours au 30/06/2026.

**Ex 6.8** ⭐⭐⭐ — Créer une vue `v_alerte_centres` qui, à partir de `v_tableau_de_bord_recrutement`, ne garde que les centres ouverts dont l'atteinte est inférieure à 50 % **ou** le taux d'échec de screening supérieur à 25 %, avec une colonne `motif_alerte` lisible.

**Ex 6.9 (réflexion)** — Votre responsable veut chaque 1er du mois une **photo** du tableau de bord de recrutement, pour suivre son évolution dans le temps. Une vue suffit-elle ? Proposer une solution (structure + requête mensuelle).
