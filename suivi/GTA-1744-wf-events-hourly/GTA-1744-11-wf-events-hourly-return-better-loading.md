# GTA-1744 - Retour : affichage des droits horaires sans latence

Contexte : `cronexia-suivi-2/suivi/GTA-1744-wf-events-hourly/` (plans 01 backend, 02 frontend).

Branche des retours : `feat-1744-wf-events-hourly-returns`.

Le détail d'une demande DEP ou RC affiche la situation des droits (pris à date, pris annuel, droits, solde). Ce bloc est déjà juste, mais l'ouverture lance un calcul de compteurs. Le même ajustement que pour les demandes en jours : lancer le calcul à l'écriture, et à l'affichage lire les résultats déjà stockés.

Une étape = un lot. Ordre à respecter. Les tests (Jest, Vitest) sont lancés par l'équipe, pas par l'agent.

## Où c'est lent

`EbdWorkflowSoldePanel.svelte` est rendu par `WorkflowDemandDetailsCard.svelte`. À chaque ouverture il appelle `/api/counters/soldes-conges?full=true&ebd=true`. La route exécute `CounterExecution` pour tout le jeu CP / RTT / TT, plus RC et DEP, du 1er janvier jusqu'à la date demandée.

Cette carte est ouverte depuis :

- les demandes collaborateur (`/demands`)
- la page valideur (`/request-management`)
- les widgets d'accueil (`HomeEmployee`, `HomeManager`, `HomeHrManager`)
- la modale des demandes du planning
- les anomalies et la synthèse, via `DayTimelineAccordion.svelte` (même `WorkflowDemandConsultModal`). `AnomaliesArrayTr.svelte` et `SummaryArrayTr.svelte` hébergent cet accordéon.

Un seul appelant de `ebd=true` : le panneau. Changer cette lecture couvre les six écrans. Aucune page n'est à brancher à part.

Les demandes en jours ne passent plus par `CounterExecution` pour ce bloc. Les heures ont encore besoin des formules (`RCDR` et `RCSD` ne sont pas une somme brute d'événements). L'ajustement : calculer à l'écriture, lire `counterResults` à l'affichage.

## Déjà en place

`enqueueCounterRecalcForWrEventRange` accepte déjà `eventByDay` et les bons codes : `DEPA` / `DEPPD`, `RCPD` / `RCPA` / `RCSD` / `RCSP`. Le recalcul part déjà quand :

- la création ou la soumission devient validée sans valideur
- la demande est validée ou refusée (`recalculate-counters-after-wr-state-change.ts`)
- la demande est annulée ou supprimée (brouillon, en attente, ou validée sans valideur) (`recalculate-counters-after-wr-cancel.ts`)

Les formules DEP et RC comptent aussi l'état `pending`. Une soumission normale reste `pending` et n'empile pas le calcul : le pris stocké ignore la nouvelle demande jusqu'à la validation. Les étapes 1 et 2 ferment ce trou pour `eventByDay` seulement.

Les workflows en jours (`eventRangeOnResource`) restent comme ils sont. Brouillon et `awaitingAttachements` restent dehors : ces états sont exclus des formules horaires. `RCDR` reste hors de la liste d'empilement (constante) ; l'exécution de `RCSD` le résout encore.

## Étape 1 — Empiler à la création en attente

Fichier : `cronexia-gta-back/app/src/workflow-resources/workflow-resources.resolver.ts`, mutation `createWorkflowResource`, après l'insertion des lignes horaires.

Appeler `enqueueCounterRecalcForWrEventRange` quand le workflow est `eventByDay` et que l'état créé est `pending`. Le bloc existant empile déjà une demande validée sans valideur : ne pas empiler une deuxième fois dans ce cas. Un brouillon n'empile pas.

Pas de spec dans cette étape : l'appel est dans le résolveur. L'étape 2 couvre le même helper depuis la soumission, qui a déjà un spec.

Fini quand une création DEP ou RC directement en `pending` empile le flow des compteurs de l'événement, et qu'une création en brouillon ne l'empile pas.

## Étape 2 — Empiler à la soumission en attente

Fichier : `cronexia-gta-back/app/src/resources/functions/workflow-resource/resources-submit-workflow-resource.ts`, à côté de la branche déjà validée.

Empiler quand l'état résultant est `pending` et que le workflow est `eventByDay`. Une demande en jours qui reste `pending` n'empile toujours pas. `awaitingAttachements` n'empile toujours pas.

Spec : `resources-submit-workflow-resource.spec.ts`.

- un `eventByDay` qui reste `pending` appelle `createFlow`
- une demande en jours qui reste `pending` n'appelle pas `createFlow`
- le test « n'empile pas » existant porte sur la génération d'événements, pas sur les compteurs : garder cette assertion

Lancé par l'équipe, pas par l'agent.

Fini quand la soumission d'un brouillon DEP ou RC vers `pending` empile les compteurs, et que la soumission d'une absence en jours vers `pending` ne les empile pas.

## Étape 3 — Requête des résultats déjà calculés

Nouveau document GraphQL à côté de `cronexia-gta-front-v2/app/src/lib/graphql/counter/queries/q_counterExecution_soldesConges.ts`. Une requête, alias de `counterResults` (pas `CounterExecution`) pour `RCDR`, `RCPD`, `RCSD`, `DEPPD`, `DEPA` seulement. Période : 1er janvier de l'année demandée jusqu'à la date.

Petit helper, dans le dossier de `build-soldes-conges-from-counter-execution.ts`, ou à côté de la requête s'il reste une fonction de chaînes et de nombres : dernière `valueFinal`, repli sur `value`, vide ou nul devient `0`. Passer ces nombres à `buildSoldesCongesFromCounterExecution` avec `hourly: true` et `full: true`, pour que DEP garde le pris annuel. Ne pas demander les compteurs jours.

Spec Vitest de la chaîne de requête et du helper de dernière valeur. Suivre `cronexia-gta-front-v2/instructions-tests-unitaires.md` :

- le spec des soldes existant n'importe pas `$typesGraphql` et n'est pas dans `test.exclude`. Garder le nouveau spec sur des chaînes et des nombres.
- si un spec, ou un fichier source qu'il charge, importe une valeur d'exécution depuis `$typesGraphql`, ajouter son chemin à la fin de `test.exclude` dans `cronexia-gta-front-v2/app/vite.config.ts`. Pas de `vi.mock('$typesGraphql')`, pas de copie des enums, pas de remplacement des enums par des chaînes en dur pour contourner la CI.

Lancé par l'équipe, pas par l'agent.

Fini quand la requête ne contient que les cinq codes horaires et `counterResults`, et que le helper lit la dernière `valueFinal`.

## Étape 4 — Branchement de la route

Fichier : `cronexia-gta-front-v2/app/src/routes/api/counters/soldes-conges/+server.ts`.

Quand `ebd=true`, exécuter la requête de l'étape 3, mapper avec le helper de dernière valeur, puis `buildSoldesCongesFromCounterExecution`. Les appels jours (`full=true` sans `ebd`) restent sur `CounterExecution`.

`EbdWorkflowSoldePanel.svelte` appelle déjà `ebd=true`. Garder l'URL, sauf si la forme de la réponse force un changement. Une ligne absente reste `0`. Après une écriture, le job Bull remplit les lignes ; le panneau relit déjà sur `dataRefresh.tick`. L'ouverture du détail n'attend plus le moteur.

Fini quand un appel `ebd=true` ne contient plus `CounterExecution`, et qu'un appel jours sans `ebd` le contient encore.

## Étape 5 — Écrans, sans code en plus

Vérifier qu'il n'y a toujours qu'un appelant de `ebd=true` (le panneau). Ces écrans lisent alors les résultats stockés, sans changement de page :

- `/demands`
- `/request-management`
- widgets d'accueil (`HomeEmployee`, `HomeManager`, `HomeHrManager`)
- modale des demandes du planning
- `/anomalies` (accordéon de la journée)
- `/summary` (accordéon de la journée)

Vérification manuelle, par l'équipe : ouvrir un détail DEP et un détail RC sur les demandes, puis sur les anomalies ou la synthèse. Le bloc situation s'affiche sans l'attente actuelle. Créer ou soumettre une demande horaire en attente, puis rouvrir une fois le job compteurs terminé : le pris à date et le pris annuel bougent. Valider, refuser et supprimer empilent encore via les hooks déjà en place.

Fini quand les six écrans ouvrent le même panneau, et que l'ouverture ne lance plus de calcul.

## Inchangé

- Situation des demandes en jours (`EmployeeRightsBalanceSource`, sommes de quantités).
- Suppression admin `WorkflowResourcesService.remove` : elle n'empile pas. La suppression collaborateur et valideur passe par l'annulation, qui empile déjà.
