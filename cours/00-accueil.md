# Module 0 — Accueil, installation et positionnement

> **Objectif** : disposer d'un poste de travail prêt (MySQL + DBeaver + base d'entraînement) et situer son niveau de départ.
> **Durée indicative** : 1 h

---

## 0.1 Comment utiliser ce support

Chaque chapitre suit le même déroulé :

```
┌──────────┐   ┌─────────┐   ┌─────────┐   ┌──────────┐   ┌─────────┐   ┌────────┐   ┌──────┐   ┌─────────────┐
│ Objectif │ → │ Concept │ → │ Visuel  │ → │ Exemples │ → │ À vous  │ → │ Pièges │ → │ Quiz │ → │ Côté métier │
└──────────┘   └─────────┘   └─────────┘   └──────────┘   └─────────┘   └────────┘   └──────┘   └─────────────┘
```

- **Exemples** : chaque requête est suivie de son **résultat attendu**. Tapez-la vous-même dans DBeaver (ne la copiez pas : c'est en tapant qu'on retient) et comparez.
- **À vous** : les énoncés sont dans `exercices/`, les corrigés dans `exercices/solutions/`. Cherchez d'abord, regardez le corrigé ensuite.
- **Pièges** : les erreurs les plus fréquentes, et l'encadré **« Standard vs MySQL »**. L'examen de certification porte sur le **SQL standard** : on pratique sur MySQL, mais il faut connaître les quelques différences.
- **Quiz** : 5 questions au format de l'examen (QCM/QCU). Les réponses sont repliées sous chaque quiz.

> 💡 **Règle d'or de la formation** : on apprend le SQL en écrivant du SQL. Prévoyez d'écrire au moins autant de requêtes que vous en lisez.

---

## 0.2 Installer l'environnement de travail

On a besoin de deux logiciels :

```
┌──────────────────────┐   requêtes SQL    ┌──────────────────────┐
│       DBeaver        │ ────────────────► │     Serveur MySQL    │
│  (le client : on y   │                   │  (le SGBD : il stocke│
│   écrit les requêtes)│ ◄──────────────── │   et calcule)        │
└──────────────────────┘     résultats     └──────────────────────┘
```

### Étape 1 — Installer MySQL 8 (le serveur)

**Windows**
1. Télécharger **MySQL Installer for Windows** sur le site officiel de MySQL (rubrique *MySQL Community Downloads*).
2. Choisir le type d'installation **Server only**.
3. Garder les options par défaut (port **3306**).
4. Définir un mot de passe pour l'utilisateur **root** — **notez-le**, il sera demandé dans DBeaver.
5. Laisser MySQL démarrer comme service Windows.

**macOS** : télécharger le paquet `.dmg` de *MySQL Community Server* et suivre l'assistant (même logique : noter le mot de passe root).

**Linux (Debian/Ubuntu)** : `sudo apt install mysql-server`, puis `sudo mysql_secure_installation`.

> Alternative possible : **MariaDB** (un « cousin » de MySQL) fonctionne pour la quasi-totalité du cours.

### Étape 2 — Installer DBeaver (le client)

1. Télécharger **DBeaver Community** (gratuit) sur `dbeaver.io`.
2. Installer avec les options par défaut.

### Étape 3 — Se connecter

1. Dans DBeaver : **Base de données → Nouvelle connexion** → choisir **MySQL**.
2. Hôte `localhost`, port `3306`, utilisateur `root`, mot de passe : celui de l'étape 1.
3. Cliquer **Tester la connexion**. La première fois, DBeaver propose de **télécharger le pilote** : accepter.
4. Si l'erreur `Public Key Retrieval is not allowed` apparaît : onglet **Propriétés du pilote** → mettre `allowPublicKeyRetrieval` à `true`.

### Étape 4 — Charger la base d'entraînement

1. **Fichier → Ouvrir un fichier…** → `db/essais_cliniques.sql`.
2. Associer l'éditeur à la connexion MySQL si DBeaver le demande.
3. Exécuter **tout le script** : **Alt + X**.
4. Dans le panneau de gauche, rafraîchir (**F5**) : la base `essais_cliniques` apparaît avec ses 8 tables.

### Étape 5 — Vérifier

Ouvrir un éditeur SQL (**Ctrl + ]**), sélectionner la base `essais_cliniques` en haut de l'éditeur, puis exécuter (**Ctrl + Entrée**) :

```sql
SELECT COUNT(*) AS nb_patients FROM patient;
```
<!-- resultat -->
```text
+-------------+
| nb_patients |
+-------------+
| 262         |
+-------------+
1 ligne
```
<!-- /resultat -->

Si vous obtenez ce nombre, tout est prêt. 🎉

> **Remettre la base à zéro** : réexécutez simplement `essais_cliniques.sql`. Faites-le sans hésiter après les exercices du module 5 (modification des données).

### Raccourcis DBeaver utiles

| Action | Raccourci |
|---|---|
| Exécuter la requête sous le curseur | **Ctrl + Entrée** |
| Exécuter tout le script | **Alt + X** |
| Nouvel éditeur SQL | **Ctrl + ]** |
| Autocomplétion | **Ctrl + Espace** |
| Mettre en forme la requête | **Ctrl + Maj + F** |
| Commenter / décommenter une ligne | **Ctrl + /** |

---

## 0.3 La base d'entraînement en un coup d'œil

Toute la formation utilise la base **`essais_cliniques`** : le suivi (fictif) d'essais cliniques de médicaments. Vous n'avez pas besoin de connaître ce domaine : la page [**Comprendre la base**](../db/comprendre-la-base.md) l'explique simplement (les acteurs, le parcours d'un patient, les indicateurs). Lisez-la maintenant ; la référence technique est dans [`db/README.md`](../db/README.md).

```
ETUDE ──< ETUDE_CENTRE >── CENTRE ──< INVESTIGATEUR
  │                          │
  └──────< PATIENT >─────────┘
              │
              ├──< VISITE ──< MESURE
              └──< EVENEMENT_INDESIRABLE

  A ──< B  se lit : « un A est lié à plusieurs B »
```

Pourquoi ce domaine ? Parce qu'il contient tout ce qu'on rencontre dans de vraies données d'entreprise : des dates, des **valeurs manquantes**, des relations plusieurs-à-plusieurs, des objectifs chiffrés à comparer au réalisé… et donc de vrais **indicateurs** à calculer.

---

## 0.4 Questionnaire de positionnement

Répondez sans chercher, simplement pour situer votre point de départ. Il n'y a pas de piège : « je ne sais pas » est une réponse utile.

| # | Question | Jamais vu | Vu, flou | À l'aise |
|---|---|:-:|:-:|:-:|
| 1 | Je sais ce qu'est une clé primaire et une clé étrangère | ☐ | ☐ | ☐ |
| 2 | J'écris un `SELECT … FROM … WHERE …` sans aide | ☐ | ☐ | ☐ |
| 3 | Je sais trier et limiter un résultat | ☐ | ☐ | ☐ |
| 4 | J'utilise `COUNT`, `SUM`, `AVG` avec `GROUP BY` | ☐ | ☐ | ☐ |
| 5 | Je fais la différence entre `WHERE` et `HAVING` | ☐ | ☐ | ☐ |
| 6 | J'écris une jointure entre 2 tables | ☐ | ☐ | ☐ |
| 7 | Je sais quand utiliser `LEFT JOIN` plutôt que `INNER JOIN` | ☐ | ☐ | ☐ |
| 8 | J'écris une sous-requête | ☐ | ☐ | ☐ |
| 9 | Je sais modifier des données (`INSERT`, `UPDATE`, `DELETE`) sans risque | ☐ | ☐ | ☐ |
| 10 | Je sais créer une vue | ☐ | ☐ | ☐ |
| 11 | Je sais lire un schéma de base (MCD / MLD) | ☐ | ☐ | ☐ |
| 12 | J'ai déjà utilisé Excel / VBA / un autre outil pour produire des indicateurs | ☐ | ☐ | ☐ |

**Mini-test pratique** (après l'installation) — essayez d'écrire ces requêtes, même approximativement :

1. Afficher le code et le titre de toutes les études.
2. Afficher les patients nés avant 1950.
3. Compter le nombre de patients par étude.

Gardez vos réponses : vous les comparerez avec ce que vous saurez écrire à la fin du module 4.

---

## 0.5 Vos besoins

Notez 2 ou 3 extractions ou indicateurs que vous produisez (ou aimeriez produire) dans votre travail. Le formateur s'en servira pour orienter les exemples, et vous pourrez les réécrire en SQL au fil de la formation.

```
1. ................................................................
2. ................................................................
3. ................................................................
```

---

➡️ Suite : [Module 1 — Concepts fondamentaux](01-concepts.md)
