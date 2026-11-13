# GTA-1915 / Formules des compteurs qui codaient l'état à part

Découpe de [01---GTA-1915-compteurs-gestion-etat-des-events-pour-aggregats-uniquement.md](01---GTA-1915-compteurs-gestion-etat-des-events-pour-aggregats-uniquement.md). Les fichiers [02](02---GTA-1915---implement-events-states-for-counters-event-aggregation.md) et [03](03---GTA-1915---implement-events-states-for-counters-events.md) sont livrés avant : l'état se lit sur le paramètre `Event`.

Ce fichier réécrit les formules qui passaient l'état en second argument, puis retire ce second argument.

Les compteurs concernés sont dans trois seeds, même schéma pour CP, RTT et TT :

- `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-CP.seed.ts`
- `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-RTT.seed.ts`
- `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-TT.seed.ts`

Hors de ce fichier : agrégats, paramètre `Event` nu (fichier 03), somme de quantités, contrôle de droits. Les `TODO: GTA-1915` de `resources.service.ts` et de `isWorkflowStateInEventRightsForecast` restent. A valider reste dans le prévisionnel des compteurs, parce que la formule le demande.

Estimation proposée : ⏱️ ~1 j, une fois les fichiers 02 et 03 livrés.

---

## Règle cible

Même Validé que les fichiers 02 et 03. Validé = demande `validated`, ou saisie directe sans workflow. Une liste écrite remplace le défaut.

| Compteur | Aujourd'hui | Formule cible | Chiffre |
| --- | --- | --- | --- |
| CPPD, RTTPD, TTPD | `VALEUR_EVENT_ETAT(event, null)` + `VALEUR_EVENT_ETAT(event, validated)`, cumulés par `VALEUR_PRECEDENTE_PERIODICITE` | La même lecture : dernière ligne sans workflow, plus dernière ligne `validated`, sur `eventRangeByDay`. Pas la map `EVENT__`. Plus le cumul de la veille | Saisie directe + validés. Pas A valider |
| CPPA, RTTPA, TTPA | Trois `SOMME_ANNEE_ETAT` : `null`, `validated`, `pending` | Un `SOMME_ANNEE` dont l'Event porte `validated` et `pending` | Saisie directe + validés + A valider |

Le `null` d'aujourd'hui est la saisie directe seule. Le `validated` d'aujourd'hui est l'état exact, sans la saisie directe. Les deux filtres ne se recouvrent pas. Pour `*PA`, leur réunion plus `pending` est un seul `OR` : la saisie directe est dans la branche `validated`, une fois. Un troisième terme « saisie directe » la compterait deux fois.

Pour `*PD`, le chiffre du jour est la somme des deux dernières lignes, une par filtre. Une seule dernière ligne sur l'union des deux filtres n'en garde qu'une quand les deux existent le même jour. Ce n'est pas le chiffre actuel, et `*SD` suit `*PD`.

`*PD` ne liste pas d'état. Le défaut, pour cette lecture, est cette paire (`null` plus `validated`), pas le seau fusionné du fichier 03.

CPSD / RTTSD / TTSD restent `droits − pris à date`. CPSP / RTTSP / TTSP restent `droits − pris prévisionnel`. Leurs formules ne citent pas d'état. Leurs chiffres suivent `*PD` et `*PA`.

La page « Mes droits & soldes » (`source="counters"`) lit ces compteurs. Elle continue de compter A valider dans le prévisionnel. La somme de quantités, elle, ne le compte plus. Cet écart reste.

---

## État des lieux

`*PD`, étape par étape, CP (RTT et TT sont identiques, events `RTT` et `TT`) :

1. `qty_direct` = `VALEUR_EVENT_ETAT(CP, valueStr null)`
2. `qty_validated` = `VALEUR_EVENT_ETAT(CP, validated)`
3. `RETURN` de `VALEUR_PRECEDENTE_PERIODICITE` + ces deux variables

`*PA` :

1. `somme_*_direct` = `SOMME_ANNEE_ETAT(event, null)`
2. `somme_*_validated` = `SOMME_ANNEE_ETAT(event, validated)`
3. `somme_*_pending` = `SOMME_ANNEE_ETAT(event, pending)`
4. `RETURN` de la somme des trois

Le second argument est une constante String. `function.ts` la traduit ainsi : argument absent → `__all__` (sans workflow ou Validé), `valueStr: null` → `__null__` (saisie directe seule), une chaîne → cet état exact. Le préchargement de `SOMME_ANNEE_ETAT` ne lit que `eventRangeByDay` (vers 3050). Pas les events en heures.

`SOMME_ANNEE` existe déjà, un seul paramètre Event. Son préchargement (vers 2878) somme l'année, jours et heures. Jours : sans workflow, ou `validated`, écrit en dur. Heures : `buildCountedDeclarationEventByDayWhere()`. La clé est `EVENT__${name}__${returnType}__${year}`, sans état. Aucun seed ne l'appelle. `*PA` appelle encore la variante `_ETAT`.

`VALEUR_EVENT_ETAT` est le seul appelant journalier de ces seeds. Son préchargement (vers 3166) ne lit que `eventRangeByDay`. Pour un jour et un état, la dernière ligne remplace la précédente. `quantity` et `duration` nuls deviennent 0. Il n'additionne pas deux plages du même jour, et il ne lit pas les heures. Le fichier 03, lui, additionne ces plages et charge les heures. `*PD` ne passe pas par cette map : le pris à date changerait, et CPSD avec lui.

`SOMME_ANNEE_ETAT` additionne toutes les lignes de l'année (`+=`), toujours sur `eventRangeByDay` seulement. `SOMME_ANNEE` additionne de la même façon, mais lit aussi les heures. `*PA` reste sur les jours. Aucun seed n'appelle `SOMME_ANNEE`. Sa clé est `EVENT__${name}__${returnType}__${year}`, sans état. Elle reste ainsi tant que l'Event ne liste pas d'états.

Dans le dépôt, ces deux fonctions ne sont référencées que par le catalogue, le service, `function.ts`, le commentaire de `02-get-resources-with-mixed-events.ts` (ligne 361), et les trois seeds. Une base déjà chargée peut en avoir d'autres : les formules enregistrées ne sont pas dans le dépôt. Le front n'a pas leur nom en dur : il lit le catalogue.

Les seeds font un `create`. Une base déjà chargée garde l'ancien graphe tant que ces compteurs ne sont pas rechargés.

---

## Ce qu'il convient de faire

### 1. Réécrire `*PD`

Une variable, `eventReturnType: quantity`, l'event connecté par `code`, aucune ligne d'état. Le paramètre n'est pas un `Event` nu lu par `manageParam`. Cette lecture est la map `EVENT__` du fichier 03 : les plages du même jour s'additionnent, et les heures chargées pour le compteur entrent. `*PD` n'utilise pas cette map.

La valeur du jour reste le préchargement actuel, après le retrait du nom `VALEUR_EVENT_ETAT`. Source : `eventRangeByDay` seulement. Clé de date inchangée (`toISOString().substring(0, 10)`). `quantity` et `duration` nuls deviennent 0 (`?? 0`). Pas d'`eventByDay`.

Le chiffre du jour est `dernière ligne (workflowResourceId: null)` + `dernière ligne (state: validated)`. Deux lignes dans le même filtre : la dernière reste. Une saisie directe et une ligne `validated` le même jour comptent toutes les deux, comme les deux appels d'aujourd'hui. `pending`, brouillon, refusé, annulé et en attente de justificatif restent dehors.

Le `RETURN` reste `VALEUR_PRECEDENTE_PERIODICITE` plus cette variable. Plus de second argument, plus de constante `null`.

`labelLong` qui décrit « saisie directe + validés » reste juste. Il ne cite plus `VALEUR_EVENT_ETAT`.

### 2. Réécrire `*PA`

Un seul appel `SOMME_ANNEE`. Son Event porte deux lignes d'état : `validated` et `pending`. `eventReturnType: quantity`.

Le chiffre annuel reste la somme de chaque `eventRangeByDay` de l'année dans trois filtres disjoints : `workflowResourceId: null`, `state: validated`, `state: pending`. Un `OR` de ces trois égale les trois totaux actuels. Les lignes du même jour s'additionnent. `quantity` nulle compte comme 0, comme le `+=` de `quantity ?? 0` aujourd'hui. Pas d'`eventByDay` sur cet appel. Une ligne horaire de CP, RTT ou TT n'entre ni dans `*PA` ni dans `*SP`.

`validated` plus `pending` produit cet `OR`. La branche sans workflow est incluse une fois, parce que `validated` est dans la liste. Pas de troisième terme « saisie directe ».

Un appel sans lignes d'état garde le `SOMME_ANNEE` d'aujourd'hui : le `OR` jours en dur (vers 2901, sans workflow ou `validated`, sans `pending`), le where heures, et la clé `EVENT__${name}__${returnType}__${year}` sans suffixe. `*PA` n'est pas cet appel. Une liste absente sur `*PA` ne doit pas retomber sur ce where : `pending` en sortirait.

La clé de `*PA` gagne le `stateKey` du fichier 02 (`pending+validated`), une fois à l'écriture du préchargement, une fois dans `function.ts`. Un seul des deux côtés, et le solde vaut 0.

`labelLong` ne dit plus « SOMME_ANNEE_ETAT × 3 ». Il dit saisie directe + validés + A valider.

### 3. Retirer les deux fonctions

Quand plus aucune formule en base n'appelle `SOMME_ANNEE_ETAT` ni `VALEUR_EVENT_ETAT`. `functionsCatalog.get` est lu avant le retour spécial de `function.ts` : un compteur qui nomme encore ces fonctions lève une erreur. Les trois seeds ne suffisent pas. L'ordre est : réécrire les six formules `*PD` et `*PA` en base, vider leur `preprocessedDatas`, recalculer, puis seulement retirer le catalogue, les branches et les préchargements. Un cache écrit avant les lignes d'état n'a pas de liste. La liste se lit sur la formule rechargée.

- `function-definition.ts` : les deux définitions, et l'import de `WORKFLOW_STATE__CONSTANT` s'il ne sert plus.
- `admissible-params.ts` : `WORKFLOW_STATE__CONSTANT`, plus cité.
- `functions-catalog.ts` : les deux entrées (le catalogue les déclare deux fois).
- `function.ts` : les branches qui lisent `paramSecond.constant.valueStr`.
- `ct-counters.service.ts` : préchargements vers 2977 et 3086, inits vers 3341 et 3356, mises à jour vers 3484 et 4155.
- Commentaire de `02-get-resources-with-mixed-events.ts`, ligne 361. L'état explicite est sur le paramètre.

`SOMME_ANNEE` et `VALEUR_PRECEDENTE_PERIODICITE` restent. La somme de quantités et le contrôle de droits restent, avec leurs `TODO: GTA-1915`.

Le diff de seed ne touche que les étapes et le `labelLong` de `CPPD`, `RTTPD`, `TTPD`, `CPPA`, `RTTPA`, `TTPA`. `*DR`, `*SD`, `*SP`, les codes, la périodicité, les dates et le format restent. Tout autre fichier de seed reste, y compris `events.seed.ts` (`name` reste `code`).

### 4. Recharger les compteurs déjà en base

Le `create` des seeds n'écrit pas par-dessus un compteur existant. Une base déjà chargée se recharge en remplaçant les six formules `*PD` et `*PA`, pas en relançant un second `create`. `preprocessedDatas` de ces six compteurs passe à null, pour que l'extraction suivante lise les lignes d'état. Puis on recalcule la famille, afin que `*SD` et `*SP` suivent. Leurs graphes ne changent pas. Leur résultat bouge seulement si `*PD` ou `*PA` a bougé. Ici le chiffre cible est le même. Une base vide reçoit les nouvelles étapes par le `create`.

---

## Inventaire des impacts

### Fichiers dont le résultat change

- Les trois seeds de congés, étapes et `labelLong` de `*PD` et `*PA` seulement
- `cronexia-gta-back\app\src\ct-counters\ct-counters.service.ts` (préchargement de `SOMME_ANNEE` quand l'Event a des états : jours seulement, `OR` des trois filtres. Le where sans état reste celui d'aujourd'hui, heures comprises. La lecture journalière de `*PD` garde dernière ligne par filtre)
- `cronexia-gta-back\app\src\ct-counters\functions\manage\function.ts` (clé de `SOMME_ANNEE` : suffixe seulement si l'Event a des états)
- Catalogue et définitions, au retrait, après rechargement des six formules et vidage de leur `preprocessedDatas`

Chaîne inchangée en aval : CPSD lit CPPD, CPSP lit CPPA, mêmes codes RTT et TT. La page « Mes droits & soldes » lit ces codes.

### Déjà conforme, à ne pas retoucher

- `*DR`, `*SD`, `*SP` : graphe, codes, périodicité, dates, format.
- `PVA`, `PVAJ`, CPT13, CPT14, CPT15, CPT16, CPT17, CPT23, `events.seed.ts`.
- Somme de quantités, garde de droits, et leurs `TODO: GTA-1915`.
- Table des états et clés `EVENT__` / `EVENT_AGGREG__` des fichiers 02 et 03. `*PD` ne lit pas `EVENT__`.
- `SOMME_ANNEE` sans états : clé, `OR` jours (vers 2901), where heures.

### Hors impact

- Un `SOMME_ANNEE` sans état, posé dans l'admin ou déjà en base, garde la clé `EVENT__${name}__${returnType}__${year}` et son where actuel.
- Events en heures de CP / RTT / TT : ils restent hors de `*PD` et de `*PA`, comme les préchargements `_ETAT`. Le where des heures de `SOMME_ANNEE` sans état ne change pas.

---

## Non-régression

### Specs

À lancer à la main.

Aucune spec de formule ne cite ces codes aujourd'hui. Après coup :

- `*PA` égale l'ancienne somme des trois `SOMME_ANNEE_ETAT` (`null` + `validated` + `pending`) sur une année de `eventRangeByDay` seulement. Les lignes du même jour s'additionnent. Les heures n'entrent pas. Pas de troisième terme saisie directe. La clé porte `pending+validated` des deux côtés.
- `*PD` égale l'ancienne somme des deux lectures au jour le jour : dernière ligne sans workflow, plus dernière ligne `validated`, `?? 0`, pas d'heures, pas la map `EVENT__`. Deux lignes dans le même filtre : la dernière reste. Une saisie directe et une ligne `validated` le même jour comptent toutes les deux. `pending` n'entre pas. Le cumul reste `VALEUR_PRECEDENTE_PERIODICITE` plus cette valeur.
- Un `SOMME_ANNEE` sans état garde sa clé actuelle, son `OR` jours et son where heures.
- Une liste absente sur `*PA` ne retombe pas sur ce where sans état.

### Recette

Même ressource, même période 2026, avant et après rechargement. Events `CP`, `RTT`, `TT`.

| Situation | `*PD` | `*PA` | Solde à date | Solde prévisionnel |
| --- | --- | --- | --- | --- |
| Saisie directe | Compte | Compte | Baisse | Baisse |
| Validé | Compte | Compte | Baisse | Baisse |
| A valider | Ignoré | Compte | Inchangé | Baisse |
| Brouillon, refusé, annulé, en attente de justificatif | Ignoré | Ignoré | Inchangé | Inchangé |

Le prévisionnel annuel est le même chaque jour de l'année. Le pris à date grandit au fil des jours, et reprend la veille via `VALEUR_PRECEDENTE_PERIODICITE`. Deux plages du même filtre le même jour : le pris à date garde la dernière, le prévisionnel les additionne sur l'année. Une saisie directe et une ligne validée le même jour : le pris à date les additionne, comme les deux appels actuels. Une ligne horaire ne bouge ni l'un ni l'autre.

Page « Mes droits & soldes » : le prévisionnel compte encore A valider. L'accueil, qui lit la somme de quantités, ne le compte pas. Écart inchangé, voulu.

### Jeux de données

Les trois seeds ci-dessus. Demandes à faire vivre, comme les fichiers 02 et 03. Matricule d'exemple déjà dans l'en-tête du seed CP : `123456A`.

---

## Questions PO

Pas de question nouvelle. A valider reste dans `*PA`. Le sortir alignerait « Mes droits & soldes » sur la somme de quantités, et changerait le prévisionnel. Ce n'est pas la formule actuelle.

---

## Dev

### Emplacements des fichiers

- Formules
  - `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-CP.seed.ts`
  - `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-RTT.seed.ts`
  - `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-TT.seed.ts`
- Lecture annuelle, à faire lire le jeu d'états
  - `cronexia-gta-back\app\src\ct-counters\ct-counters.service.ts` (préchargement `SOMME_ANNEE`, vers 2878)
  - `cronexia-gta-back\app\src\ct-counters\functions\manage\function.ts` (`SOMME_ANNEE`, vers 61)
- À retirer après le rechargement des six formules et le vidage de leur `preprocessedDatas`
  - `cronexia-gta-back\app\src\_utility\functions\function-definition.ts`
  - `cronexia-gta-back\app\src\_utility\functions\functions-catalog.ts`
  - `cronexia-gta-back\app\src\_utility\functions\admissible-params.ts` (`WORKFLOW_STATE__CONSTANT`)
  - branches `VALEUR_EVENT_ETAT` et `SOMME_ANNEE_ETAT` de `function.ts`
  - préchargements `_ETAT` de `ct-counters.service.ts` (vers 2977, 3086, 3341, 4155)
  - commentaire ligne 361 de `cronexia-gta-back\app\src\ct-counters\functions\histo\04-events\02-get-resources-with-mixed-events.ts`
- Déjà livrés, relus ici
  - where : `cronexia-gta-back\app\src\resources\functions\events\times\build-counted-workflow-state-where.ts`
  - lecture journalière de `*PD` : dernière ligne par filtre, comme le préchargement vers 3129 (`eventRangeByDay`, `?? 0`, clé de date inchangée). Sans état = `null` plus `validated`, pas une seule dernière ligne sur l'union
  - la map `EVENT__` du fichier 03 n'alimente pas `*PD`
