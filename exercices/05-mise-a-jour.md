# Exercices — Module 5 : Mise à jour des données

> Corrigés : [`solutions/05-mise-a-jour.md`](solutions/05-mise-a-jour.md)
> 🔄 [Remettez la base à zéro](../cours/00-accueil.md#remettre-la-base-à-zéro) avant de commencer, et à la fin.
> Pour chaque `UPDATE` / `DELETE` : écrivez d'abord le `SELECT` qui montre les lignes visées.

**Ex 5.1** ⭐ — Un nouveau centre rejoint le réseau : « Clinique Océane » à Biarritz (France). L'ajouter sans préciser le pays, puis vérifier que le pays a bien été renseigné.

**Ex 5.2** ⭐ — Ajouter un investigateur pour ce nouveau centre : Dr Nadia Kaci, oncologue, `nadia.kaci@oceane-centre9.example`, sans superviseur. *(Retrouvez l'identifiant du centre avec une requête plutôt que de le deviner.)*

**Ex 5.3** ⭐⭐ — Faire participer ce centre à l'étude `ONCO-03`, ouverture le 1er juillet 2026, objectif 10 inclusions, avec Dr Kaci comme investigatrice principale. Utiliser un `INSERT … SELECT` pour ne pas écrire les identifiants en dur.

**Ex 5.4** ⭐ — L'étude `DERM-05` démarre : mettre sa date de début au 1er septembre 2026 et son statut à `recrutement`.

**Ex 5.5** ⭐⭐ — Ouvrir les deux centres de `DERM-05` au 15 septembre 2026, en une seule instruction.

**Ex 5.6** ⭐⭐ — Les EI non résolus de grade 1 sont considérés comme résolus 30 jours après leur survenue. Mettre à jour leur date de résolution en conséquence. Combien de lignes sont concernées ?

**Ex 5.7** ⭐⭐ — Le patient `DIAB-02-C07-008` est perdu de vue depuis le 15 juin 2026. Enregistrer sa sortie.

**Ex 5.8** ⭐⭐ — Supprimer les visites **futures** (date prévue après le 30/06/2026) du patient `DIAB-02-C07-008`, puisqu'il est sorti.

**Ex 5.9** ⭐⭐⭐ — Supprimer complètement le patient `NEURO-04-C02-016` (et tout ce qui dépend de lui), **dans une transaction**. Vérifier avant le `COMMIT` que le patient et ses données ont bien disparu.

**Ex 5.10** ⭐⭐⭐ — Créer une table `objectif_mensuel (etude_id, mois, objectif)` (clé primaire composée `etude_id, mois` ; `mois` au format texte `AAAA-MM`). Y insérer pour `DIAB-02` un objectif de 5 inclusions pour chaque mois de 2026 où il y a eu au moins une inclusion (`INSERT … SELECT`). Puis écrire la requête qui compare objectif et réalisé.

**Ex 5.11 (réflexion)** — Un collègue exécute `DELETE FROM visite WHERE date_realisee = NULL;` pour supprimer les visites non réalisées. Que se passe-t-il ? Corrigez l'instruction… et dites pourquoi il vaut peut-être mieux ne pas l'exécuter.
