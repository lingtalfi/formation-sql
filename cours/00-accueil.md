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

La base est livrée sous forme d'un **script SQL** : un simple fichier texte, `essais_cliniques.sql`, qui contient toutes les instructions pour créer les tables et les remplir. « Charger la base », c'est **faire exécuter ce fichier par MySQL**, via DBeaver.

> Dans DBeaver, les menus sont indiqués en français, suivis de leur nom anglais *en italique* (DBeaver s'affiche dans la langue de votre système).

**4.1 — Récupérer le fichier**

- Si vous avez cloné le dépôt : le fichier est dans `db/essais_cliniques.sql`.
- Sinon, sur GitHub : ouvrir [`db/essais_cliniques.sql`](../db/essais_cliniques.sql), puis cliquer sur l'icône **Télécharger** (*Download raw file*, flèche vers le bas, en haut à droite du fichier). Il arrive dans votre dossier *Téléchargements*.

**4.2 — Ouvrir le fichier dans DBeaver**

Menu **Fichier → Ouvrir un fichier…** (*File → Open File…*) → choisir `essais_cliniques.sql` → **Ouvrir**.

Le script s'affiche dans un **éditeur SQL** (un onglet au centre de l'écran). On voit son contenu : des `CREATE TABLE`, puis des centaines de lignes `INSERT INTO`. Rien n'est encore exécuté.

**4.3 — Dire à DBeaver sur quel serveur l'exécuter**

Un fichier ouvert ainsi n'est rattaché à **aucune connexion**. Dans la barre d'outils, au-dessus de l'éditeur, le sélecteur de connexion active affiche alors `N/A` :

```
 Barre d'outils :   … [ 🔌 N/A        ▾ ]  [ < N/A > ▾ ] …
                         ▲                     ▲
                         connexion active      base (schéma) active
```

1. Cliquer sur le **premier** sélecteur (`N/A`) — raccourci **Ctrl + 9**.
2. Choisir votre connexion MySQL (par ex. `localhost`), puis **Sélectionner** (*Select*).

Le sélecteur affiche maintenant le nom de la connexion, et le titre de l'onglet passe de `<none> essais_cliniques.sql` à `<localhost> essais_cliniques.sql`.

> 🚩 Si vous oubliez cette étape, l'exécution s'arrête aussitôt avec le message **« Cannot obtain session — No active connection »**. Cliquez sur **OK**, faites l'étape 4.3, puis relancez **Alt + X**. Le second sélecteur (la base) peut rester vide : le script crée et sélectionne lui-même la base `essais_cliniques`.

**4.4 — Exécuter tout le script**

Menu **Éditeur SQL → Exécuter le script SQL** (*SQL Editor → Execute SQL Script*), ou **Alt + X**, ou le bouton ▶️📄 « Exécuter le script » dans la barre verticale à gauche de l'éditeur.

> ⚠️ **Pas Ctrl + Entrée** : ce raccourci n'exécute que **l'instruction sous le curseur**, pas tout le fichier.

DBeaver exécute les instructions une par une (quelques secondes). Si une fenêtre de confirmation apparaît (le script commence par supprimer la base si elle existe), validez.

À la fin, l'onglet **Statistiques** (*Statistics*), en bas de l'éditeur, résume l'exécution : nombre de requêtes et **0 erreur**. Si une erreur s'affiche, notez son message : c'est presque toujours la connexion qui n'a pas été choisie (étape 4.3).

**4.5 — Rafraîchir**

Dans le panneau de gauche (*Database Navigator*), clic droit sur votre connexion → **Rafraîchir** (*Refresh*) ou **F5**. Dépliez **Bases de données** (*Databases*) : `essais_cliniques` apparaît, avec ses 8 tables dans **Tables**.

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

### Remettre la base à zéro

Après des exercices qui modifient les données (modules 2 et 5 surtout), ou si vous pensez avoir « cassé » quelque chose, vous pouvez à tout moment revenir à la base d'origine. C'est **exactement l'étape 4**, rejouée :

1. **Fichier → Ouvrir un fichier…** (*File → Open File…*) → `essais_cliniques.sql`
   (ou, s'il est encore ouvert dans un onglet, cliquez simplement sur cet onglet) ;
2. vérifiez que le sélecteur de connexion affiche votre connexion MySQL (sinon **Ctrl + 9**) ;
3. **Alt + X** (*Execute SQL Script*) ;
4. **F5** sur la connexion dans le panneau de gauche.

Le script commence par `DROP DATABASE IF EXISTS essais_cliniques` : il **efface entièrement** la base puis la recrée à l'identique. Tout ce que vous y aviez ajouté (tables, vues, lignes modifiées) disparaît. Si vous voulez garder vos propres requêtes, enregistrez-les dans des fichiers `.sql` à part : elles ne sont pas stockées dans la base.

> 💡 **En ligne de commande** (si vous avez un client `mysql` installé, ou MySQL dans Docker), la même opération tient en une ligne :
> ```bash
> mysql -h 127.0.0.1 -u root -p --default-character-set=utf8mb4 < essais_cliniques.sql
> ```

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
