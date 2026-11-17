# Implémentation d'une checkbox de filtre pour les events Annulé / Refusé

Guide générique. Il sert de base à un plan par page, à compléter au moment de traiter chaque écran. Pas de câblage détaillé ici.

Source : [01-GTA-1911---ticket-de-base.md](01-GTA-1911---ticket-de-base.md) (option d'affichage) et le suivi du 17/11 (une option, partout, cookie commun par user/rôle). Branche : `feat-1915-events-states-visu-option`.

## Décisions

- Une seule checkbox, les deux états ensemble (`cancelled` et `refused` de `WorkflowStateEnum` dans [workflow.prisma](../../../cronexia-gta-back/app/prisma/schema/workflow.prisma)).
- Libellé : « Afficher les événements annulés et refusés ». Cookie absent = affiché (comportement actuel). Décocher masque.
- Un seul cookie pour les 6 écrans, suffixe `_{sub}_{role}`. Pas de variante par page (contrairement à `CALENDAR__LEGEND_FILTERS`).
- Filtre d'affichage uniquement, sur les listes déjà chargées. Aucune requête, aucun paramètre GraphQL, aucun `?states=` ne change. Basculer la checkbox ne refetch pas.
- Hors scope métier : génération d'anomalies, compteurs, conflits (d'autres points du ticket).
- Event sans workflow : considéré validé, donc jamais masqué par cette checkbox.
- Pas d'exception « mes propres events restent visibles ». Cette exception existe pour les brouillons (`isOwnPlanningResource`) et ne s'applique pas ici.
- `draft`, `pending`, `validated`, `awaitingAttachements` ne sont pas touchés.
- Ne pas réutiliser le masquage en dur de [remote-work-days.ts](../../../cronexia-gta-front-v2/app/src/routes/functions/cronexia/declaration-presence/remote-work-days.ts) (`HIDDEN_STATES`) : autre écran, sans préférence utilisateur.

## Modèle brouillon (déjà en place, à ne pas modifier)

Ce n'est pas une checkbox utilisateur. C'est la config site `IS_DISPLAY_DRAFT_REQUESTS` ([get-is-display-draft-requests.ts](../../../cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/get-is-display-draft-requests.ts)), défaut false. Le payload arrive entier ; le masquage est ensuite en mémoire :

- Planning : `mapPlanningData` dans [planning-data.mapper.ts](../../../cronexia-gta-front-v2/app/src/routes/functions/cronexia/planning/collective/planning-data.mapper.ts) appelle `filterPlanningDatasDraftForViewer` sur `rawResources` déjà reçus.
- Anomalies : [DayTimelineAccordion.svelte](../../../cronexia-gta-front-v2/app/src/routes/components/common/accordion/DayTimelineAccordion.svelte) filtre le tableau `events`.
- Synthèse : le `+page.svelte` summary retire les brouillons via `getEventByDayWorkflowFields({ hideDrafts })`.
- Tables valideur : `visibleRows` passe par `passesValidatorDraftVisibility`. Les helpers `buildValidatorStatesParamFromStatusFilters` / `sanitizeValidatorStatesQueryParam` pourraient retirer `draft` d'un `?states=`, mais rien ne les appelle.

Le nouveau filtre se pose à côté de celui-ci, jamais dedans, pour ne pas mélanger config site (brouillon) et préférence user (annulé / refusé).

## Hors scope : tables de demandes

Demandes collaborateur et gestion des demandes valideur ont déjà [WorkflowDemandsStatusFiltersBar.svelte](../../../cronexia-gta-front-v2/app/src/routes/components/cronexia/workflow/WorkflowDemandsStatusFiltersBar.svelte) : pills `draft`, `pending`, `validated`, `refused` ([workflow-demands-status-filters.ts](../../../cronexia-gta-front-v2/app/src/_utility/workflow/constant/workflow-demands-status-filters.ts)), cookie `WORKFLOW__TABLE_FILTERS`. Ne pas y ajouter cette checkbox.

Note, sans la traiter ici : `cancelled` n'a pas de pill. `getWorkflowDemandStatusFilterKey` renvoie `null`, donc une demande annulée n'apparaît que lorsque aucun statut n'est sélectionné (« Toutes »). Refusé est déjà une pill.

---

## Cookies / ✅ Terminé

Calquer [persist-scoped-boolean.svelte.ts](../../../cronexia-gta-front-v2/app/src/_utility/cookie/function/persist-scoped-boolean.svelte.ts). Ne pas hydrater dans `onMount` ni via `navigationCronexia.cookiesSuffixUserAndRole` : le suffixe n'est pas prêt et la préférence ne serait jamais relue (voir [README-cookies.md](../../../cronexia-gta-front-v2/app/src/_utility/cookie/README-cookies.md), règle « display booleans », et [275 sync or destroy](../../../cronexia-gta-front-v2/app/src/_utility/navigation/275-cookies-sync-or-destroy/_cookies-sync-or-destroy.md)).

- Ajouter une clé dans `COOKIE_KEYS_PREFIXS` de [cookies-config.ts](../../../cronexia-gta-front-v2/app/src/config/cookies-config.ts), préfixe `cx_`, valeur `'true' | 'false'`. Nom : `EVENTS__SHOW_CANCELLED_OR_REFUSED` / `cx_events_show_cancelled_or_refused`.
- Une ligne dans le tableau user-scoped du README cookies.
- Le wipe de version supprime déjà tout `cx_*`. Rien à brancher de plus, et ne pas l'ajouter à `CRONEXIA_COOKIES_WIPE_EXCEPT`.
- Pas de lecture SSR pour ce guide : le filtre est client. Flash possible au premier paint (events visibles puis masqués). À trancher page par page seulement si une page charge déjà ses events côté serveur et que le flash gêne.

## Prédicat partagé / ✅ Terminé

Helper pur, à côté du filtre brouillon planning : [is-cancelled-or-refused-event.ts](../../../cronexia-gta-front-v2/app/src/routes/functions/cronexia/planning/is-cancelled-or-refused-event.ts) (`isCancelledOrRefusedEvent`). Il reconnaît annulé / refusé sur les mêmes champs déjà normalisés pour le brouillon : `workflowResource.state`, `workflowState`, `workflowStatus`, `status`.

Chaque page applique ce prédicat sur sa propre liste au moment du rendu, après le chargement. Ne pas généraliser tout de suite le parcours `resources → dates → events` de `filterPlanningDatasDraftForViewer` : cette forme est propre au planning. Le planning pourra s'en inspirer dans son plan de page, dans une fonction séparée.

Checkbox : un seul composant, [ShowCancelledOrRefusedEventsCheckbox.svelte](../../../cronexia-gta-front-v2/app/src/routes/components/cronexia/event/ShowCancelledOrRefusedEventsCheckbox.svelte). Il possède le libellé et appelle `persistScopedBoolean` sur `EVENTS__SHOW_CANCELLED_OR_REFUSED`. Chaque page le monte une fois et lit `checked`. Ne pas créer une autre checkbox, ne pas recopier le libellé, ne pas appeler `persistScopedBoolean` sur cette clé ailleurs. Pas d'état global tant qu'une seule page est affichée.

---

## Pages / filters

Quatre surfaces réelles pour six libellés. Anomalies, la synthèse, les trois plannings, le calendrier d'absences et l'emploi du temps sont câblés. Toutes montent [ShowCancelledOrRefusedEventsCheckbox.svelte](../../../cronexia-gta-front-v2/app/src/routes/components/cronexia/event/ShowCancelledOrRefusedEventsCheckbox.svelte) : ne pas en créer une autre.

### Anomalies / ✅ Terminé

Entrée : [anomalies](<../../../cronexia-gta-front-v2/app/src/routes/(app)/(with-filters)/anomalies>). Rendu events : [AnomalyDayTimeline.svelte](../../../cronexia-gta-front-v2/app/src/routes/components/cronexia/anomaly/AnomalyDayTimeline.svelte). Le brouillon est déjà filtré en amont dans [DayTimelineAccordion.svelte](../../../cronexia-gta-front-v2/app/src/routes/components/common/accordion/DayTimelineAccordion.svelte).

`ShowCancelledOrRefusedEventsCheckbox` est montée une fois dans les actions du `FilterToolbar` de [AnomaliesArray.svelte](../../../cronexia-gta-front-v2/app/src/routes/components/cronexia/anomaly/AnomaliesArray.svelte), page seulement (`hideFilters` faux : la modale planning ne la monte pas et ne filtre pas). Liste filtrée : `events` passé à `AnomaliesArrayTr`, avant `DayTimelineAccordion`. Le filtre brouillon de l'accordéon n'est pas modifié.

### Synthèse / ✅ Terminé

Entrée : [summary](<../../../cronexia-gta-front-v2/app/src/routes/(app)/(with-filters)/summary>). Grille : [SummaryArray.svelte](../../../cronexia-gta-front-v2/app/src/routes/components/cronexia/summary/SummaryArray.svelte). Le brouillon est déjà retiré dans le `+page.svelte` via `hideDrafts`.

`ShowCancelledOrRefusedEventsCheckbox` est montée une fois dans les actions du `FilterToolbar` de `SummaryArray`. Listes filtrées au rendu, à côté du brouillon : `absences` et `presences` de chaque ligne (pastilles, filtre de contenu, quantité en jours), et `events` de la timeline passé à `SummaryArrayTr` avant `DayTimelineAccordion`. `withEventWorkflowFields` n'est pas modifié.

### Planning collectif / ✅ Terminé

Entrée : [collective-schedule](<../../../cronexia-gta-front-v2/app/src/routes/(app)/(with-filters)/collective-schedule>). Écran : [CollectiveSchedulePage.svelte](../../../cronexia-gta-front-v2/app/src/routes/components/cronexia/collective-schedule/CollectiveSchedulePage.svelte), partagé avec le planning individuel.

Le filtre annulé / refusé s'applique sur les events déjà mappés, à côté du passage brouillon de `mapPlanningData` ([planning-data.mapper.ts](../../../cronexia-gta-front-v2/app/src/routes/functions/cronexia/planning/collective/planning-data.mapper.ts)), sans le modifier.

`ShowCancelledOrRefusedEventsCheckbox` est montée une fois dans `rightTools` de l'en-tête, en mode collectif (pas d'aperçu lecture seule). Liste filtrée : events non `schedule` de `resourcesForDisplay`, via [filter-mapped-planning-cancelled-or-refused.ts](../../../cronexia-gta-front-v2/app/src/routes/functions/cronexia/planning/collective/filter-mapped-planning-cancelled-or-refused.ts), avant `resourcesWithWorkflow`. L'aperçu lecture seule ne filtre pas.

### Planning individuel / ✅ Terminé

Même écran que le collectif, monté en mode individuel : [individual-schedule](<../../../cronexia-gta-front-v2/app/src/routes/(app)/(with-filters)/individual-schedule>) importe `CollectiveSchedulePage`.

Même montage et même liste que le collectif : `ShowCancelledOrRefusedEventsCheckbox` dans `rightTools`, filtre `filterMappedPlanningCancelledOrRefused` sur les events non `schedule` avant `resourcesWithWorkflow`. Le cookie est le même. L'aperçu lecture seule (`IndividualPlanningPreview`, `readOnlyPreview`) ne monte pas la checkbox et ne filtre pas.

### Calendrier d'absences / ✅ Terminé

Entrée : [calendar](<../../../cronexia-gta-front-v2/app/src/routes/(app)/(without-filters)/calendar>). Écran : [PersonalCalendarPage.svelte](../../../cronexia-gta-front-v2/app/src/routes/components/cronexia/calendrier-annuel/PersonalCalendarPage.svelte), partagé avec l'emploi du temps.

La légende est déjà persistée (`statusFilters`, cookie `CALENDAR__LEGEND_FILTERS` scopé page). Ne pas y ranger cette option.

`ShowCancelledOrRefusedEventsCheckbox` est montée une fois dans la barre du calendrier, à côté de `CalendarToolbarFilters`. Liste filtrée : `filteredEvents` (segments `absences` / `hourAbsences`, puis l'event s'il n'en reste plus), avant `eventsByDate`. Le cookie de légende n'est pas modifié.

### Emploi du temps / ✅ Terminé

Entrée : [timetable](<../../../cronexia-gta-front-v2/app/src/routes/(app)/(without-filters)/timetable>). Même `PersonalCalendarPage` que le calendrier d'absences.

Même montage et même liste que le calendrier : `ShowCancelledOrRefusedEventsCheckbox` dans la barre, filtre `withoutCancelledOrRefusedCalendarEvents` sur `filteredEvents` avant `eventsByDate`. Le cookie est le même, pas scopé `absences` / `timetable`. Le cookie de légende n'est pas modifié.

### Planning d'équipe / ✅ Terminé

Même écran que les plannings collectif et individuel : [team-schedule](<../../../cronexia-gta-front-v2/app/src/routes/(app)/(without-filters)/team-schedule>) importe `CollectiveSchedulePage` en mode équipe.

`ShowCancelledOrRefusedEventsCheckbox` est montée une fois dans `teamRequestTools`, à côté de `WorkflowNewDemandButton`. Même liste que le collectif : events non `schedule` de `resourcesForDisplay`, via `filterMappedPlanningCancelledOrRefused`, avant `resourcesWithWorkflow`. Le cookie est le même. `isTeamPlanningEventVisibleForViewer` n'est pas modifié : les events refusés d'autrui restent masqués quand la case est cochée.
