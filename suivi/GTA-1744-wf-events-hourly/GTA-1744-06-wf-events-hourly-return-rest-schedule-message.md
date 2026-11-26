# GTA-1744 - Retour PO : message horaire de repos / ✅ Terminé

Contexte : `cronexia-suivi-2/suivi/GTA-1744-wf-events-hourly/` (plans 01 backend, 02 frontend).

Branche des retours : `feat-1744-wf-events-hourly-returns`.

Phrase courte pour toute demande de type `eventByDay`. Les déclarations d'heures gardent la phrase longue. Le contrôle du garde ne change pas.

## Retour PO

Remplacer, pour une demande d'événement horaire :

> La saisie n'est pas autorisée sur un horaire de repos. Ce jour peut être déclaré sans modifications

par :

> La demande n'est pas autorisée sur un horaire de repos

Apostrophe droite, pas de point final. DEP et RC ne sont que des exemples : la phrase vaut pour tout workflow `eventByDay`, quel que soit l'événement cible.

Le libellé en base de code est au singulier (« sans modification »). Le PO le cite au pluriel. Les déclarations d'heures gardent ce libellé :

> La saisie n'est pas autorisée sur un horaire de repos. Ce jour peut être déclaré sans modification.

## Où c'est aujourd'hui

- Un seul libellé : `CRO_DECLA_HOURS_000000001` dans `cronexia-gta-back/app/src/_utility/error/cronexia-error-dictionnary.ts`.
- Levé par `assertHourliesNotOnRestSchedule` (`src/declaration-hourlies/functions/assert-hourlies-not-on-rest-schedule.ts`). `CRO_DECLA_HOURS_000000002` (resourceId absent) est un autre cas.
- Déclarations d'heures : `declaration.service.ts`, `declaration-hourlies.service.ts`, et `assert-hourlies-not-on-rest-schedule-by-declaration.ts`. La phrase « saisie / déclaré » leur correspond.
- Demandes : le même garde est appelé depuis `src/workflow-resources/workflow-resources.resolver.ts`.
  - Création, vers la ligne 906 : un seul appel mélange `declarationHourlyCreates` et `eventByDayRestRows`.
  - Mise à jour `eventByDays.create`, vers la ligne 1538.
  - Mise à jour déclaration différée, vers la ligne 1415.
- `declaration.service.create` est rappelé après le garde du resolver (création et mise à jour différées) et relance la phrase longue.
- Front : la phrase n'est pas en dur. `HourlyEventWorkflowModal.svelte` pose `generalError = hourlyEventCreateUserMessage(result)`. Cette fonction (`routes/functions/cronexia/workflow/hourly-event-workflow-create.helpers.ts`) renvoie `result.message` dès qu'il est non vide et différent du code. Ce `message` est le `messageHuman` posé par `_utility/api/handle-graphql-response.ts`.
- `CRO_DECLA_HOURS_000000001` n'est pas dans le repli `HOURLY_EVENT_CREATE_ERROR_BY_CODE` (codes 043 à 049). Le spec le prouve : un message API avec ce code est affiché tel quel. Message vide et code inconnu : « La demande n'a pas pu être enregistrée. »
- L'écran déclarations d'heures affiche aussi `result.message` (`declaration-hours-page.state.svelte.ts`, `notifyError`). Il suit le dictionnaire, sans table de codes.
- `CRO_WR_000000050` est réservé : commenté dans le dictionnaire, cité dans `workflow-resources/docs/create.doc.ts` pour la surcharge d'horaire.

## Étape 1 — Dictionnaire

Fichier : `cronexia-gta-back/app/src/_utility/error/cronexia-error-dictionnary.ts`.

Ajouter `CRO_WR_000000051` à côté des codes GTA-1744 (043–049).

- `fr-FR` : `La demande n'est pas autorisée sur un horaire de repos`
- `en-US` : `The request is not allowed on a rest schedule.`
- `messageTech` : garde repos, demande `eventByDay`, variables `{date}` et `{resourceId}` déjà utilisées par `CRO_DECLA_HOURS_000000001`.

Le texte de `CRO_DECLA_HOURS_000000001` reste tel quel.

## Étape 2 — Garde, phrase selon l'appelant

Fichier : `cronexia-gta-back/app/src/declaration-hourlies/functions/assert-hourlies-not-on-rest-schedule.ts`.

Le contrôle ne change pas (dates, config, type `rest`). Argument optionnel en fin de signature, défaut `CRO_DECLA_HOURS_000000001`, utilisé uniquement au `throw` de la ligne repos. `CRO_DECLA_HOURS_000000002` reste commun.

Appelants inchangés, donc phrase longue : `declaration.service.ts`, `declaration-hourlies.service.ts`, `assert-hourlies-not-on-rest-schedule-by-declaration.ts`.

Dans `workflow-resources.resolver.ts` :

- Création, vers la ligne 906 : scinder l'appel. `eventByDayRestRows` reçoit `CRO_WR_000000051`. `declarationHourlyCreates` garde le défaut. Appeler d'abord les lignes `eventByDay`.
- Mise à jour `eventByDays.create`, vers la ligne 1538 : passer `CRO_WR_000000051`.
- Mise à jour déclaration différée, vers la ligne 1415 : laisser le défaut.

`declaration.service.create` continue de lever la phrase longue. Une demande `declarationHours` n'a pas de lignes `eventByDay` dans ce garde, donc elle ne prend pas `051`.

## Étape 3 — Repli front et spec

Fichier : `cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/hourly-event-workflow-create.helpers.ts`.

Ajouter `CRO_WR_000000051` dans `HOURLY_EVENT_CREATE_ERROR_BY_CODE`, même phrase que le dictionnaire. Le message API substitué continue de passer avant le repli. La modale ne change pas.

Spec : `hourly-event-workflow-create.helpers.spec.ts`. Garder le cas « message API + `CRO_DECLA_HOURS_000000001` affiché tel quel ». Ajouter : message vide ou égal au code `051` → phrase courte ; message API non vide avec `051` → message API. Lancé par l'équipe, pas par l'agent.

## Inchangé

- Texte et code `CRO_DECLA_HOURS_000000001`.
- Écran déclarations d'heures (`notifyError(result.message)`).
- Modale, widgets, modalité, créneau, bouton déplacement (notes 04, 05, 07, 08, 09).
