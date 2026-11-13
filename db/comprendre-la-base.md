# Comprendre la base `essais_cliniques`

> **Pour qui ?** Pour toute personne qui ne connaît pas le monde des essais cliniques. Pas besoin d'être du métier pour suivre la formation : cette page donne tout le contexte nécessaire, en 10 minutes.
> Pour la référence technique (tables, colonnes, schéma), voir [`README.md`](README.md).

---

## 1. L'histoire en une minute

Un laboratoire pharmaceutique a inventé un comprimé, la molécule **KX-12**, dont il pense qu'il fait baisser la tension artérielle. Avant de pouvoir le vendre, il doit prouver aux autorités de santé deux choses :

1. que le médicament **fonctionne** (efficacité) ;
2. qu'il est **sans danger** (tolérance, sécurité).

Pour le prouver, il organise un **essai clinique** : on donne le médicament à de vraies personnes, sous surveillance médicale étroite, et on les compare à des personnes qui ne l'ont pas reçu.

Notre base contient le suivi (fictif) de cinq essais de ce type.

---

## 2. Les acteurs

```
   PROMOTEUR (laboratoire)          « Laboratoires Alvéa »
        │ finance et pilote
        ▼
   ÉTUDE                            « CARDIO-01 : KX-12 fait-elle baisser la tension ? »
        │ se déroule dans plusieurs
        ▼
   CENTRES (hôpitaux)               Tours, Nantes, Genève…
        │ dans chacun, des médecins :
        ▼
   INVESTIGATEURS                   dont un INVESTIGATEUR PRINCIPAL par étude et par centre
        │ recrutent et suivent les
        ▼
   PATIENTS
```

### Le promoteur (`etude.promoteur`)

L'entreprise qui **paie et organise** l'essai, par exemple « Laboratoires Alvéa ». C'est le propriétaire du projet, mais il ne soigne personne lui-même : il délègue aux hôpitaux.

### L'étude (`etude`)

L'essai lui-même, avec un code (`CARDIO-01`) et une question à laquelle il doit répondre. Elle suit un règlement très strict, le **protocole** : qui peut participer, combien de patients, quelles visites, quelles mesures.

Chaque étude a une **phase**, qui indique son degré de maturité :

| Phase | Qui ? | But principal | Dans la base |
|---|---|---|---|
| I | quelques dizaines de volontaires sains | vérifier que le produit est tolérable | NEURO-04 |
| II | une centaine de malades | premiers signes d'efficacité, bonne dose | DIAB-02, ONCO-03 |
| III | des centaines / milliers de malades | **prouver** l'efficacité | CARDIO-01, DERM-05 |
| IV | patients après la mise sur le marché | surveiller sur le long terme | — |

Et un **statut** : en préparation → recrutement → suivi (on ne recrute plus, on suit les patients déjà inclus) → terminée.

### Les centres (`centre`, `etude_centre`)

Le promoteur a besoin de patients, et les patients sont dans les hôpitaux. Il fait donc participer **plusieurs hôpitaux**, dans plusieurs villes, parfois plusieurs pays. Chacun recrute et suit des patients localement.

Un même hôpital peut participer à plusieurs études, et une étude se déroule dans plusieurs hôpitaux : c'est la table **`etude_centre`**, qui dit quel centre participe à quelle étude, depuis quand (`date_ouverture`) et avec quel **objectif** de patients à recruter.

### Les investigateurs (`investigateur`)

Les **médecins** des centres. Pour chaque étude, dans chaque centre, l'un d'eux est l'**investigateur principal** (PI, *Principal Investigator*) : le responsable local de l'étude. Certains médecins sont supervisés par un chef de service (`superviseur_id`).

### Les patients (`patient`)

Les personnes qui participent. Chaque patient est identifié par un **code** (jamais par son nom : les données de santé sont confidentielles), par exemple `CARDIO-01-C03-012` = étude CARDIO-01, centre n° 3, 12ᵉ patient du centre.

---

## 3. Le parcours d'un patient

```
  SCREENING ──► remplit les critères ? ──non──► « échec de screening »
  (pré-sélection)          │ oui                 (fin : n'est jamais entré dans l'étude)
                           ▼
                      INCLUSION  (entrée officielle dans l'étude)
                           │
                      TIRAGE AU SORT du BRAS : traitement  ou  placebo
                           │
                      VISITES  V0 ─ V1 ─ V2 ─ … ─ V6   (calendrier fixé par le protocole)
                           ├─ à chaque visite : des MESURES (poids, tension, glycémie…)
                           └─ entre-temps : d'éventuels ÉVÉNEMENTS INDÉSIRABLES
                           │
                      SORTIE  ── normale : fin d'étude
                              └─ prématurée : retrait du consentement, perdu de vue,
                                               événement indésirable…
```

### Screening et inclusion

Le **screening** est une pré-sélection : on vérifie que la personne remplit les critères du protocole (âge, maladie, traitements en cours…). Beaucoup échouent. C'est pourquoi la base contient des patients avec une **date de screening** mais **sans date d'inclusion** (`date_inclusion` à NULL) : ce sont les **échecs de screening**.

### Le bras : traitement ou placebo

Un **placebo** est un faux comprimé, identique en apparence au vrai. Les patients inclus sont répartis **au hasard** entre deux groupes, appelés **bras** :
- le bras **traitement** reçoit le vrai médicament ;
- le bras **placebo** reçoit le faux.

Ni le patient ni le médecin ne savent qui reçoit quoi. Si le bras traitement s'améliore nettement plus que le bras placebo, c'est que le médicament fonctionne. Vous le vérifierez vous-même au module 4 : dans CARDIO-01, la tension baisse d'environ 13 points dans le bras traitement, contre 4 dans le bras placebo.

### Les visites et les mesures

Le protocole fixe un calendrier de rendez-vous : V0 le jour de l'inclusion, V1 deux semaines plus tard, etc. Chaque visite a une **date prévue** et, si elle a eu lieu, une **date réalisée**. Une visite dont la date prévue est passée mais qui n'a pas été réalisée est une **visite manquée**.

À chaque visite réalisée, on relève des **mesures** : poids, tension (PAS / PAD = pression artérielle systolique / diastolique, en mmHg), glycémie pour l'étude sur le diabète.

### Les événements indésirables (EI)

Tout problème de santé survenu pendant l'étude (maux de tête, nausées, chute…), **que le médicament en soit responsable ou non**. Le médecin le décrit avec :

| Information | Valeurs | Colonne |
|---|---|---|
| **Grade** (intensité) | 1 léger · 2 modéré · 3 sévère · 4 menace vitale · 5 décès | `grade` |
| **Grave** (EIG) | oui si hospitalisation, menace vitale… (déclaration obligatoire aux autorités) | `grave` |
| **Imputabilité** (lien avec le traitement, selon le médecin) | certain · probable · possible · improbable · exclu | `lien_traitement` |
| **Résolution** | date de fin, ou NULL s'il est toujours en cours | `date_resolution` |

### La sortie d'étude

Un patient quitte l'étude soit **normalement** (il a fait toutes ses visites : « fin d'étude »), soit **prématurément** : il retire son consentement, on perd sa trace (« perdu de vue »), ou un effet indésirable oblige à arrêter.

---

## 4. Les KPI : à quoi servent toutes ces données ?

Un **KPI** (*Key Performance Indicator*, « indicateur clé de performance ») est un chiffre que l'on surveille régulièrement pour savoir si un projet est sur la bonne voie. C'est le tableau de bord d'une voiture : vitesse, carburant, température.

Le **chef de projet clinique** coordonne une étude dans tous ses centres. Chaque semaine ou chaque mois, il se pose des questions comme celles-ci :

| Question | KPI | Module où on l'apprend |
|---|---|---|
| Recrute-t-on assez vite ? | nombre d'inclus vs objectif, par centre ; inclusions par mois | 3, 4, 6 |
| Les centres sélectionnent-ils les bons patients ? | taux d'échec de screening | 3 |
| Les patients viennent-ils à leurs rendez-vous ? | taux de visites manquées | 3, 6 |
| Perd-on des patients en route ? | taux de sortie prématurée, et ses motifs | 3, 6 |
| Le médicament est-il bien toléré ? | nombre d'EI, d'EI graves, bras traitement vs placebo | 4, 6 |
| Le médicament fonctionne-t-il ? | évolution moyenne de la tension entre V0 et V6, par bras | 4 |

Chacune de ces questions se traduit par **une requête SQL**. Par exemple : « Lyon a inclus 7 patients pour un objectif de 20 → 35 % → il faut les relancer. » Produire ces chiffres automatiquement, plutôt que de recopier des données à la main dans Excel, c'est exactement ce que cette formation apprend à faire.

> 💡 Ces indicateurs ne sont pas propres à la santé. Remplacez « centre » par « agence », « patient » par « client », « visite » par « rendez-vous » ou « commande », « objectif d'inclusions » par « objectif commercial » : vous obtenez les tableaux de bord de la plupart des entreprises.

---

## 5. Ce qu'il faut garder en tête en écrivant des requêtes

- **Tout est fictif** : hôpitaux, médecins, laboratoires, molécules et patients sont inventés.
- **« Aujourd'hui » = le 30 juin 2026.** Les données sont figées à cette date ; on écrit `'2026-06-30'` plutôt que `CURRENT_DATE` pour que tout le monde obtienne les mêmes résultats.
- **Les NULL ont un sens** :

| Colonne à NULL | Signifie |
|---|---|
| `etude.date_debut` | l'étude n'a pas encore démarré (DERM-05) |
| `etude_centre.date_ouverture` | le centre n'est pas encore ouvert pour cette étude |
| `investigateur.superviseur_id` | c'est un chef de service |
| `patient.date_inclusion` | échec de screening |
| `patient.bras` | pas de bras (non inclus) |
| `patient.date_sortie` | toujours dans l'étude |
| `visite.date_realisee` | visite pas faite : manquée si la date prévue est passée, à venir sinon |
| `evenement_indesirable.date_resolution` | EI toujours en cours |

- **Les données contiennent des « trous » volontaires** (un centre sans patient, une étude sans centre ouvert, des investigateurs sans étude…) : ce sont eux qui rendent les jointures externes et les tests de NULL intéressants.
