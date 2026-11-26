# GTA-1744 - Retour PO : widget « En déplacement aujourd'hui »

Contexte : `cronexia-suivi-2/suivi/GTA-1744-wf-events-hourly/` (plans 01 backend, 02 frontend, note 05 modalité).

Branche des retours : `feat-1744-wf-events-hourly-returns`.

Afficher le déplacement du jour, en journée ou en heures, sur l'accueil manager et l'accueil RH. Réutiliser `DayPeriodRangeDisplay`, déjà utilisé par le calendrier collaborateur. Pas de nouveau composant d'affichage.

## Retour PO

Manager > Accueil > widget « En déplacement aujourd'hui ». Le connecter. L'événement `DEP` peut être en jour et en heures (`events.seed.ts`, `isTravelling: true`, `isManagedByDay`, `isManagedByHalfDay`, `isManagedByDuration`, `isManagedByStartAndEndHours`). Réutiliser le composant d'affichage du calendrier.

## Où c'est aujourd'hui

`+page.svelte` monte déjà `HomeManager.svelte` et `HomeHrManager.svelte`. Les deux rendent `WidgetDeplacementAujourdhui.svelte`. Pas de changement sur la page.

`deplacementData` ne parcourt que `resourcesEventRangeOnResourcesByPeriod` (plages en jour). Il garde `event.isTravelling` et `isEventRangeOnResourceStrictlyValidated`, puis passe `typeDay` à `DayType` (Journée, Matin, Après-midi).

Une plage en jour est un `EventRangeOnResource`, avec sa tranche du jour `EventRangeByDay`. Un déplacement en heures est un `EventByDay` sur le même événement `DEP`. Ces lignes sont déjà chargées pour aujourd'hui via `/api/event-by-day/by-resources-by-period` (`hourAbsencesResp`) : `timeStart`, `timeEnd`, `duration`, `event.isTravelling`, `workflowResource.state`. Elles ne sont fusionnées que dans le widget absences, avec `typeDay: 'Heures'`, que `DayType` peint en Journée.

## Qui est affiché

Même règle pour un `EventRangeOnResource` (et son `EventRangeByDay` du jour) et pour un `EventByDay`. Réutiliser `isEventRangeOnResourceStrictlyValidated` (`event-range-on-resource-workflow.helpers.ts`) :

- Pas de `workflowResource` : affiché. Un admin ou un rôle supérieur peut poser l'événement sans workflow. Cela compte comme validé. Le helper renvoie déjà vrai dans ce cas (`if (!workflowResource) return true`).
- `workflowResource` présent et état `VALIDATED_*` : affiché.
- `workflowResource` présent et état pending, draft, refused, cancelled, ou vide : masqué.

La tranche du jour (`EventRangeByDay`) n'a pas de workflow. Le contrôle est sur `EventRangeOnResource.workflowResource`. La ligne horaire est contrôlée sur `EventByDay.workflowResource`, déjà sélectionné par la requête.

## Affichage

Réutiliser `DayPeriodRangeDisplay.svelte`. Le calendrier collaborateur l'utilise déjà pour les deux formes : `UpcomingEventsList.svelte` et `PendingRequestsList.svelte`, montés depuis `PersonalCalendarPage.svelte` sur `calendar/[[year]]/[[month]]/+page.svelte`.

`DateAndDayType`, à l'intérieur, affiche le badge jour, ou `trailingText` quand il est posé. Le texte horaire vient de `resolveHourlyDisplay`, et seulement pour un `EventByDay` (`idEventByDay` présent, pas de `idEventRangeOnResource`), même garde que `UpcomingEventsList`. Une plage en jour garde son `typeDay`. Plusieurs lignes horaires le même jour passent par `resolveHourlyDisplayFromLines`.

Une ligne par matricule. À droite : `DayPeriodRangeDisplay` pour aujourd'hui, `size="XS"`, `dayTypePosition="right"` :

- Jour seul : date et Journée / Matin / Après-midi.
- Heures seules : date et le créneau (`09:00 - 12:30`) ou la durée. Pas de badge jour.
- Les deux : le créneau gagne, parce que `trailingText` remplace le badge.

La date fait partie du composant. Le widget ne gagne pas une deuxième implémentation de badge.

## Étape 1 — Affichage du widget

Fichier : `cronexia-gta-front-v2/app/src/routes/components/common/widgets/WidgetDeplacementAujourdhui.svelte`.

Remplacer le `DayType` de la ligne par `DayPeriodRangeDisplay` pour aujourd'hui, `size="XS"`, `dayTypePosition="right"`. `periodStart` est `typeDay`. `trailingText` est `resolveHourlyDisplay` seulement quand le voyageur porte un `EventByDay` (`idEventByDay` posé, pas de `idEventRangeOnResource`). Plusieurs lignes : `resolveHourlyDisplayFromLines`.

Étendre `Traveler` avec `timeStart`, `timeEnd`, `duration`, `idEventByDay`, tous optionnels. Les accueils et les démos qui ne passent que `typeDay` gardent le badge jour. La ligne témoin reste une journée entière, pour que la hauteur réservée inclue la date.

Fini quand un déplacement en jour déjà dans la liste montre la date et Journée, Matin ou Après-midi. Les personnes en heures ne sont pas encore dans la liste. Aucun fichier d'accueil ne change.

## Étape 2 — Construction de la liste

Nouveau fichier sous `cronexia-gta-front-v2/app/src/routes/functions/cronexia/home/`, et un spec à côté. Pas encore importé par les accueils.

Entrée : ressources des plages du jour, ressources des `EventByDay` du jour, matricules, aujourd'hui en `YYYY-MM-DD`. Sortie : un voyageur par matricule, avec `typeDay` pour une plage en jour et les champs horaires quand ils existent. Garder une ligne quand `event.isTravelling` et `isEventRangeOnResourceStrictlyValidated(workflowResource)` sont vrais, y compris un `workflowResource` absent sur l'`EventRangeOnResource` ou sur l'`EventByDay`. Les deux sources pour le même matricule se replient en une ligne qui garde les champs horaires.

Cas du spec : jour seul, lignes horaires gardées, pending exclu, pas de `workflowResource` affiché pour les deux formes, les deux sources repliées en une ligne. Lancé par l'équipe, pas par l'agent.

Fini quand le spec existe et que les accueils construisent encore `deplacementData` eux-mêmes.

## Étape 3 — Branchement des deux accueils

`HomeManager.svelte` et `HomeHrManager.svelte`, le même changement dans les deux.

`deplacementData` appelle le builder avec `dayAbsencesResp` et `hourAbsencesResp`. Ne pas sortir tôt quand seule la requête jour a échoué. `hasDeplacementError` est vrai quand la requête jour ou la requête heures a échoué, comme `hasAbsencesError` (aujourd'hui ce n'est que `hasEventsError`).

Fini quand un `DEP` horaire validé, ou sans workflow, montre le créneau, et qu'un `DEP` en jour montre encore le badge. Un workflow pending reste dehors.

## Inchangé

- Widget absences, accueil collaborateur, widget « Validation des demandes ».
- `+page.svelte`.
- Bouton déplacement collaborateur (note 09), repasse des widgets collab (note 08).
