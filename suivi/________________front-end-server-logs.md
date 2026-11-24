$ vitest run

 RUN  v4.1.12 /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app

 ↓ src/routes/api/chatbot/_functions/interpret-message.live.spec.ts (81 tests | 81 skipped)
stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > les gardes lisent toute la conversation tapée > garde le type cité au tour précédent quand la réponse ne le répète pas
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > les gardes lisent toute la conversation tapée > écarte toujours un type que personne n’a cité
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > quand le modèle écrit « J’ouvre… » sans appeler l’outil > retente quand le modèle recopie la question des homonymes (GTA-1879)
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > quand le modèle écrit « J’ouvre… » sans appeler l’outil > retente une fois et prend la réponse qui appelle l’outil
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > quand le modèle écrit « J’ouvre… » sans appeler l’outil > ouvre l’écran nommé quand le modèle échoue deux fois sur un ordre net
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > quand le modèle écrit « J’ouvre… » sans appeler l’outil > dit que rien n’a été fait quand la seconde tentative échoue aussi
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > quand le modèle écrit « J’ouvre… » sans appeler l’outil > ne retente pas quand la première réponse est déjà bonne
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > place la consigne AVANT la question
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > 🔒 rien de personnel ne part > masque le nom AVANT l’envoi, même sans référentiel
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > 🔒 rien de personnel ne part > masque aussi l’HISTORIQUE — sinon le masquage ne dure qu’un tour
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > 🔒 rien de personnel ne part > rétablit le nom au RETOUR, alors qu’il n’est jamais parti
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > 🔒 rien de personnel ne part > rétablit le nom au retour de lister_absences
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > 🔒 rien de personnel ne part > rétablit le nom au retour de modifier_absence
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > 🔒 rien de personnel ne part > rétablit le nom au retour de supprimer_absence
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > 🔒 rien de personnel ne part > rétablit le nom dans une réponse en toutes lettres
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > 🔒 rien de personnel ne part > lit le vrai nom, jamais le pseudonyme
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > donne la date du jour au modèle, sans quoi « demain » n’a aucun sens
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > n’expose QUE les codes d’absence du client
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > transmet l’historique entre la consigne et la question
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > borne l’attente — une requête qui ne revient jamais est le pire cas
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > reprend l’appel quand le fournisseur échoue, et répond normalement
chatbot > interprétation : 1602 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > rend une intention structurée quand le modèle appelle l’outil
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > rend une réponse en texte pour une salutation
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > historique : les questions que le serveur a posées > garde lisible une question de désambiguïsation, sans laisser sortir un nom
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > historique : les questions que le serveur a posées > applique le filet complet à une réponse que le serveur n’a pas qualifiée de question
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « l’équipe » rendue comme une personne > reclasse les soldes de « l’équipe » en consultation de groupe
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « l’équipe » rendue comme une personne > reclasse aussi « tout le monde » pour les absences
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « l’équipe » rendue comme une personne > laisse une vraie personne là où elle est
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « l’équipe » rendue comme une personne > rétablit le nom quand le modèle recopie un pseudonyme dans le groupe
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > des heures dans une pose > marque une pose où des heures sont citées
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > des heures dans une pose > ne marque pas une pose à la journée
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « qui est présent ? » > marque la liste d’absents demandée comme une liste de présents
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « qui est présent ? » > ne marque pas une question sur les absents
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « les deux » en réponse à « Laquelle ? » > rejoue la demande pour toutes les personnes proposées (« les 2 »)
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « les deux » en réponse à « Laquelle ? » > rejoue la demande pour toutes les personnes proposées (« les deux »)
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « les deux » en réponse à « Laquelle ? » > rejoue la demande pour toutes les personnes proposées (« toutes »)
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « les deux » en réponse à « Laquelle ? » > rejoue la demande pour toutes les personnes proposées (« Tous »)
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « les deux » en réponse à « Laquelle ? » > rejoue la demande pour toutes les personnes proposées (« tout le monde »)
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « les deux » en réponse à « Laquelle ? » > rejoue la demande sans les échanges précédents, qu’il recopiait (GTA-1879)
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « les deux » en réponse à « Laquelle ? » > garde la question qui précède la demande rejouée
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « les deux » en réponse à « Laquelle ? » > garde une écriture personne par personne
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > « les deux » en réponse à « Laquelle ? » > laisse au modèle un vrai nom donné en réponse
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > un nom que rien dans le message ne permet de nommer > ne cherche personne et demande de qui il s’agit, au lieu de « je ne trouve personne »
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

stdout | src/routes/api/chatbot/_functions/interpret-message.spec.ts > interpretMessage > un nom que rien dans le message ne permet de nommer > laisse passer un nom écrit dans le message courant, même inconnu
chatbot > interprétation : 0 ms · 0.000 m$ · 0 entrée (dont 0 % en cache) + 0 sortie

 ✓ src/routes/api/chatbot/_functions/interpret-message.spec.ts (46 tests) 3291ms
     ✓ ne laisse JAMAIS remonter le message du fournisseur  1606ms
     ✓ reprend l’appel quand le fournisseur échoue, et répond normalement  1603ms
 ✓ src/routes/api/chatbot/_functions/anonymize-message.spec.ts (105 tests) 71ms
 ✓ src/routes/functions/common/home/home-widget-user-layout.spec.ts (35 tests) 19ms
stderr | src/routes/api/chatbot/_functions/demands-gateway.spec.ts > submitDemand > lit un refus du back comme un échec, jamais comme un succès
chatbot > écriture de demande refusée par le back : [ { message: 'délai dépassé' } ]

stderr | src/routes/api/chatbot/_functions/demands-gateway.spec.ts > submitDemand > rend la RAISON du back : c’est elle que le chat dit à l’utilisateur
chatbot > écriture de demande refusée par le back : [ { message: 'Bad Request', extensions: { errorCronexia: [Object] } } ]

stderr | src/routes/api/chatbot/_functions/demands-gateway.spec.ts > decideDemand > lit un refus du back comme un échec
chatbot > écriture de demande refusée par le back : [ { message: 'pas valideur' } ]

 ✓ src/routes/api/chatbot/_functions/demands-gateway.spec.ts (20 tests) 22ms
 ✓ src/routes/api/chatbot/_functions/parse-model-intent.spec.ts (32 tests) 17ms
 ✓ src/routes/api/chatbot/_functions/identify-person.spec.ts (28 tests) 23ms
 ✓ src/routes/api/chatbot/_functions/open-page.spec.ts (25 tests) 25ms
 ❯ src/routes/components/cronexia/rights-employee/employee-rights-takes.spec.ts (0 test)
 ✓ src/routes/components/common/voice/extract-speech-text.spec.ts (25 tests) 62ms
 ✓ src/routes/functions/cronexia/workflow-tab/employee-tab-create-action.spec.ts (10 tests) 9ms
 ✓ src/routes/api/chatbot/_functions/parse-chatbot-request.spec.ts (20 tests) 11ms
 ✓ src/routes/components/cronexia/rights-hr-collective/hr-collective-rights-fixture.spec.ts (4 tests) 28ms
 ✓ src/routes/functions/cronexia/event-range-on-resource/check-event-conflicts.spec.ts (22 tests) 14ms
 ✓ src/routes/functions/cronexia/declaration-follow-up/declaration-follow-up-periods.spec.ts (30 tests) 21ms
 ✓ src/routes/functions/cronexia/workflow-tab/filter-employee-catalog-tabs-for-modality.spec.ts (10 tests) 9ms
 ✓ src/routes/functions/cronexia/workflow-tab/parse-workflow-tabs-for-navigation.spec.ts (13 tests) 12ms
 ✓ src/routes/components/cronexia/rights-hr-individual/hr-individual-rights-kpis.spec.ts (12 tests) 10ms
 ❯ src/routes/functions/cronexia/calendrier-annuel/planning-data-to-events.hour-absences.spec.ts (0 test)
 ❯ src/routes/functions/cronexia/workflow/hourly-event-workflow-create.helpers.spec.ts (0 test)
 ✓ src/routes/components/cronexia/rights-employee/employee-rights-balances.spec.ts (12 tests) 10ms

🎯 Extraction des personnes : 37/37 (100 %)
 ✓ src/routes/api/chatbot/_functions/person-extraction.corpus.spec.ts (37 tests) 35ms
 ✓ src/routes/api/chatbot/_functions/demand-workflows.spec.ts (23 tests) 12ms
 ✓ src/routes/components/cronexia/cycle-catalog/cycle-catalog-view.spec.ts (24 tests) 21ms
 ✓ src/routes/components/common/chatbot/chatbot-conversation.spec.ts (12 tests) 13ms
 ✓ src/routes/functions/cronexia/event-range-on-resource/resolve-conflict-reaction.spec.ts (14 tests) 8ms
 ✓ src/routes/api/chatbot/_functions/existing-absences.spec.ts (18 tests) 9ms
 ✓ src/routes/functions/cronexia/declaration-presence/declaration-resubmission.test.ts (13 tests) 8ms
 ✓ src/routes/functions/cronexia/workflow/workflow-clocking-overload-create.helpers.spec.ts (10 tests) 16ms
 ✓ src/routes/api/chatbot/_functions/text-assist.spec.ts (18 tests) 20ms
 ✓ src/routes/functions/common/menu/secondary/expand-menu-sections.spec.ts (16 tests) 11ms
 ✓ src/routes/functions/cronexia/declaration-follow-up/map-declaration-follow-up-rows.spec.ts (14 tests) 10ms
 ✓ src/routes/components/cronexia/rights-hr-collective/hr-collective-rights-period.spec.ts (8 tests) 8ms
 ✓ src/routes/functions/cronexia/workflow-tab/families-for-employee-tab.spec.ts (6 tests) 7ms
 ✓ src/routes/components/cronexia/rights-employee/employee-rights-share.spec.ts (18 tests) 9ms
 ✓ src/routes/api/chatbot/_functions/parse-demands.spec.ts (10 tests) 9ms
 ✓ src/routes/components/cronexia/schedule-catalog/schedule-catalog-view.spec.ts (19 tests) 20ms
 ✓ src/routes/functions/cronexia/calendar/calendar-days-draft.spec.ts (11 tests) 8ms
 ✓ src/routes/functions/cronexia/declaration-follow-up/follow-up-history.spec.ts (9 tests) 47ms
 ✓ src/routes/functions/cronexia/planning/collective/planning-display-options.spec.ts (12 tests) 8ms
 ✓ src/routes/functions/cronexia/planning/home-planning-widget.helpers.spec.ts (18 tests) 25ms
 ✓ src/routes/functions/cronexia/home-widget/home-widget-visibility-draft.spec.ts (17 tests) 17ms
 ✓ src/routes/components/cronexia/rights-employee/employee-rights-kpi.spec.ts (6 tests) 7ms
 ✓ src/_utility/auth/complete-login-session.spec.ts (9 tests) 9ms
 ✓ src/routes/functions/cronexia/planning/collective/summary-rows-presence.test.ts (7 tests) 7ms
 ✓ src/routes/functions/cronexia/notification/parse-workflow-notification-message.test.ts (13 tests) 9ms
 ✓ src/routes/functions/cronexia/workflow-tab/absence-event-codes-for-employee-tab.spec.ts (6 tests) 6ms
 ✓ src/routes/functions/cronexia/workflow/hide-resubmitted-refused-declarations.test.ts (11 tests) 8ms
 ✓ src/routes/functions/cronexia/workflow/map-validator-for-workflow-level-state.spec.ts (9 tests) 8ms
 ✓ src/routes/functions/cronexia/anomaly/aggregate-anomalies.spec.ts (5 tests) 15ms
 ✓ src/routes/functions/cronexia/schedule/allowed-for-resource.spec.ts (12 tests) 9ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/convert-organize-dnd-to-replace.spec.ts (3 tests) 5ms
 ✓ src/_utility/workflow/function/build-workflow-to-validate-summary.spec.ts (4 tests) 5ms
 ❯ src/routes/functions/cronexia/planning/planning-workflow-resolve.helpers.spec.ts (0 test)
 ✓ src/routes/functions/cronexia/workflow-tab/workflows-for-display-family.spec.ts (6 tests) 6ms
 ✓ src/routes/functions/cronexia/declaration-hours/map-resources-declaration-hourly.spec.ts (6 tests) 8ms
 ✓ src/routes/functions/common/table/build-grouped-table-items.spec.ts (11 tests) 10ms
 ✓ src/routes/api/chatbot/_functions/resolve-day-types.spec.ts (10 tests) 8ms
 ✓ src/routes/functions/cronexia/workflow-tab/validator-workflow-names-for-tab.spec.ts (7 tests) 5ms
 ❯ src/routes/functions/cronexia/workflow/build-workflow-demand-details.hourly.spec.ts (0 test)
 ✓ src/routes/components/cronexia/rights-hr-individual/hr-individual-rights-exercises.spec.ts (3 tests) 14ms
 ✓ src/routes/components/cronexia/rights-hr-individual/hr-individual-rights-warning.spec.ts (5 tests) 15ms
 ✓ src/routes/api/auth/login-profile-choice/login-profile-choice.spec.ts (4 tests) 40ms
 ↓ src/routes/api/chatbot/_functions/interpret-message.bench.spec.ts (1 test | 1 skipped)
 ✓ src/routes/components/cronexia/rights-hr-individual/hr-individual-rights-calc.spec.ts (5 tests) 6ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/organize-catalog-workflow-groups.spec.ts (6 tests) 7ms
 ✓ src/routes/api/auth/login/login.spec.ts (4 tests) 38ms
 ✓ src/routes/api/chatbot/_functions/turn-cost.spec.ts (10 tests) 7ms
 ✓ src/routes/api/chatbot/_functions/carried-person.spec.ts (12 tests) 11ms
 ❯ src/routes/functions/cronexia/calendrier-annuel/calendar-pending-requests.helpers.spec.ts (0 test)
 ✓ src/routes/functions/cronexia/planning/favorites/planning-catalogue-cache.server.spec.ts (3 tests) 9ms
 ✓ src/routes/functions/cronexia/declaration-hours/segments/presence-slot-validation.spec.ts (10 tests) 8ms
 ✓ src/routes/components/cronexia/rights-employee/employee-rights-fixture.spec.ts (5 tests) 8ms
 ✓ src/routes/functions/cronexia/counters/widget-counters.test.ts (13 tests) 8ms
 ✓ src/routes/functions/cronexia/event-range-on-resource/build-event-range-create-input.spec.ts (7 tests) 6ms
 ✓ src/routes/api/ai/_functions/ai-routes-guard.spec.ts (12 tests) 39ms
 ✓ src/routes/functions/cronexia/declaration-follow-up/follow-up-ui.helpers.spec.ts (12 tests) 24ms
 ✓ src/routes/functions/cronexia/event/resolve-hourly-display.spec.ts (12 tests) 8ms
 ✓ src/routes/functions/cronexia/workflow/clocking-demand-day.helpers.spec.ts (8 tests) 16ms
 ✓ src/routes/api/auth/sso/[provider]/callback/sso-callback.spec.ts (2 tests) 33ms
 ✓ src/routes/functions/cronexia/delegation/delegation-mode-history.spec.ts (10 tests) 14ms
 ✓ src/_utility/auth/profile-choice-cookie.spec.ts (6 tests) 9ms
 ✓ src/_utility/time/day-end-time.spec.ts (9 tests) 8ms
 ✓ src/routes/functions/cronexia/clocking/clocking-workflow-display.spec.ts (7 tests) 15ms
 ✓ src/routes/api/ai/_const/transcription-vocabulary.spec.ts (11 tests) 8ms
 ✓ src/routes/functions/cronexia/workflow-tab/canonical-employee-tab-segment.spec.ts (6 tests) 5ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/insert-organize-catalog-workflow.spec.ts (6 tests) 10ms
 ✓ src/routes/api/chatbot/_functions/resolve-population.spec.ts (18 tests) 10ms
 ✓ src/_utility/navigation/400-params/410-420-resolve-dates-page-default.spec.ts (5 tests) 8ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/find-duplicate-organize-tab-workflow.spec.ts (3 tests) 5ms
 ✓ src/_utility/auth/sso-attempt-cookie.spec.ts (7 tests) 8ms
 ✓ src/routes/api/chatbot/_const/chatbot-pages.spec.ts (8 tests) 9ms
 ✓ src/routes/functions/cronexia/workflow-tab/canonical-validator-tab-segment.spec.ts (6 tests) 5ms
 ✓ src/routes/functions/cronexia/vacation-rights/resolve-workflow-right-key.spec.ts (6 tests) 5ms
 ✓ src/routes/functions/cronexia/workflow-tab/is-catalog-tab-active.spec.ts (4 tests) 5ms
 ✓ src/routes/functions/cronexia/workflow-tab/families-on-tab.spec.ts (4 tests) 5ms
 ✓ src/routes/components/common/chatbot/absences-target.spec.ts (9 tests) 7ms
 ❯ src/routes/functions/cronexia/calendrier-annuel/index-calendar-events-by-date.hourly.spec.ts (0 test)
 ✓ src/routes/functions/cronexia/workflow-tab/organize/count-organize-workflow-tab-usages.spec.ts (4 tests) 5ms
 ✓ src/routes/api/ai/_functions/assert-ai-available.spec.ts (7 tests) 36ms
 ✓ src/routes/functions/cronexia/workflow-tab/catalog-tab-membership.spec.ts (3 tests) 5ms
 ❯ src/routes/functions/cronexia/workflow/map-validator-hourly-event-from-api.spec.ts (0 test)
 ✓ src/routes/functions/cronexia/workflow/hourly-event-workflow-display.helpers.spec.ts (5 tests) 20ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/selected-organize-catalog-workflows.spec.ts (5 tests) 5ms
 ✓ src/routes/functions/cronexia/anomaly/timeline-overlap-segments.spec.ts (5 tests) 7ms
 ✓ src/routes/functions/cronexia/declaration-follow-up/follow-up-group-levels.spec.ts (6 tests) 13ms
 ✓ src/routes/functions/cronexia/workflow-tab/creatable-hourly-event-workflows.spec.ts (3 tests) 5ms
 ✓ src/routes/components/common/chatbot/chatbot-client.spec.ts (8 tests) 7ms
 ✓ src/routes/functions/cronexia/planning/collective/planning-event-state-filter.spec.ts (8 tests) 6ms
 ✓ src/routes/functions/common/pagination/paginate-items.spec.ts (10 tests) 7ms
 ✓ src/routes/functions/cronexia/declaration-follow-up/follow-up-saved-view.spec.ts (10 tests) 7ms
 ❯ src/routes/functions/cronexia/planning/is-cancelled-or-refused-event.spec.ts (0 test)
 ✓ src/routes/functions/common/menu/secondary/build-menu-tree.spec.ts (6 tests) 6ms
 ✓ src/routes/api/chatbot/_const/chatbot-engine.spec.ts (7 tests) 7ms
 ✓ src/routes/functions/cronexia/event-range-on-resource/submit-conflict-replacement.spec.ts (3 tests) 7ms
 ✓ src/routes/functions/cronexia/anomaly/rows-for-anomalies-without-row.spec.ts (6 tests) 7ms
 ✓ src/routes/functions/cronexia/clocking/clocking-table-view-cookie.spec.ts (6 tests) 6ms
 ✓ src/routes/components/cronexia/rights-hr-individual/hr-individual-rights-rules.spec.ts (3 tests) 5ms
 ✓ src/routes/functions/cronexia/workflow-tab/workflow-demand-title-suffix-from-catalog.spec.ts (3 tests) 4ms
 ✓ src/routes/functions/cronexia/resource/file/format-constraint-errors.spec.ts (5 tests) 5ms
 ✓ src/routes/functions/cronexia/anomaly/updated-anomalies-override.test.ts (8 tests) 6ms
 ✓ src/routes/functions/cronexia/planning/clocking-workflow-requests.spec.ts (4 tests) 6ms
 ✓ src/routes/components/common/chatbot/chatbot-proposal-labels.spec.ts (9 tests) 6ms
 ✓ src/routes/api/chatbot/_functions/normalize-iso-date.spec.ts (8 tests) 6ms
 ✓ src/routes/api/chatbot/_functions/unmentioned-event.spec.ts (14 tests) 9ms
 ✓ src/routes/functions/cronexia/planning/collective/planning-resource-batch.spec.ts (6 tests) 6ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/parse-organize-workflows.spec.ts (3 tests) 12ms
 ✓ src/routes/components/common/chatbot/chatbot-dock-resize.spec.ts (10 tests) 7ms
 ✓ src/routes/api/auth/sso/[provider]/start/sso-start.spec.ts (2 tests) 32ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/workflow-tab-icon-svelecte-options.spec.ts (4 tests) 14ms
 ✓ src/routes/functions/cronexia/declaration/declaration-alert-messages.spec.ts (7 tests) 20ms
 ✓ src/routes/functions/cronexia/workflow-tab/employee-create-tab-cards.spec.ts (1 test) 4ms
 ✓ src/routes/api/chatbot/_functions/invented-period.spec.ts (11 tests) 10ms
 ✓ src/routes/functions/cronexia/workflow/declaration-alert-reasons.test.ts (5 tests) 20ms
 ✓ src/routes/functions/cronexia/declaration-hours/declaration-hours-workflow-create.helpers.spec.ts (3 tests) 5ms
 ✓ src/routes/functions/cronexia/workflow-tab/load-workflow-tab-catalog.server.spec.ts (3 tests) 7ms
 ❯ src/routes/functions/cronexia/event/event-by-day-direct-mutation.spec.ts (0 test)
 ✓ src/routes/api/chatbot/_functions/server-texts-masking.spec.ts (46 tests) 27ms
 ✓ src/routes/functions/common/chip-group/apply-visible-chip-selection.test.ts (9 tests) 6ms
 ✓ src/routes/functions/cronexia/resource/workflow-validator-field-warning.spec.ts (6 tests) 5ms
 ✓ src/routes/functions/cronexia/workflow/workflow-table-sort.helpers.test.ts (8 tests) 14ms
 ✓ src/routes/functions/cronexia/reports/report-group-by.test.ts (3 tests) 6ms
 ✓ src/routes/components/common/chatbot/chatbot-greeting.spec.ts (7 tests) 6ms
 ❯ src/routes/functions/cronexia/planning/filter-planning-datas-draft-for-viewer.spec.ts (0 test)
 ✓ src/routes/functions/common/codes-selection/codes-selection.test.ts (6 tests) 6ms
 ✓ src/routes/api/chatbot/_functions/anonymize-vocabulary.spec.ts (4 tests) 6ms
 ✓ src/routes/functions/cronexia/counters/resolve-searched-counter-codes.test.ts (7 tests) 6ms
 ✓ src/routes/functions/cronexia/rights-initialization/build-initialization-preview.spec.ts (4 tests) 20ms
 ✓ src/_utility/navigation/200-auth-profile/245-to-safe-redirect-path.spec.ts (20 tests) 8ms
 ✓ src/routes/components/cronexia/schedule-catalog/schedule-ranges-view.spec.ts (6 tests) 6ms
 ✓ src/routes/functions/common/dom/anchored-placement.spec.ts (7 tests) 6ms
 ✓ src/routes/functions/cronexia/event/is-day-absence-direct-input.spec.ts (7 tests) 5ms
 ❯ src/routes/functions/cronexia/workflow/describe-workflow-validation-candidate.spec.ts (0 test)
 ✓ src/routes/functions/cronexia/workflow-tab/catalog-workflow-create-item-id.spec.ts (3 tests) 4ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/filter-organize-catalog-workflows.spec.ts (3 tests) 7ms
 ✓ src/routes/functions/cronexia/workflow/declaration-days-rest-alert.test.ts (4 tests) 12ms
 ✓ src/routes/functions/cronexia/reports/report-favorites.test.ts (5 tests) 5ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/organize-catalog-group-key.spec.ts (5 tests) 5ms
 ✓ src/_utility/auth/sso-provider-logo.spec.ts (13 tests) 6ms
 ✓ src/routes/functions/common/auth/page-rights-config.spec.ts (35 tests) 9ms
 ✓ src/routes/functions/cronexia/declaration/declaration-period-status.spec.ts (4 tests) 5ms
 ✓ src/routes/functions/cronexia/planning/collective-planning-search-params.spec.ts (3 tests) 4ms
 ✓ src/routes/functions/cronexia/workflow/employee-demands-tabs.spec.ts (7 tests) 5ms
 ✓ src/routes/api/chatbot/_functions/back-error-message.spec.ts (4 tests) 4ms
 ❯ src/routes/functions/cronexia/anomaly/transform-events.spec.ts (0 test)
 ✓ src/routes/functions/cronexia/legislation/legislation-lines.spec.ts (6 tests) 20ms
 ✓ src/config/themes/function/resolve-login-panel-logo.test.ts (8 tests) 5ms
 ✓ src/routes/functions/cronexia/declaration/calendar-utils.spec.ts (5 tests) 6ms
 ✓ src/routes/functions/cronexia/planning/favorites/apply-planning-favorite.spec.ts (3 tests) 7ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/workflow-tab-icon-material-ligature.spec.ts (3 tests) 6ms
 ✓ src/routes/components/cronexia/rights-hr-individual/hr-individual-rights-page.spec.ts (3 tests) 5ms
 ✓ src/routes/functions/cronexia/workflow/workflow-resource-row-display.helpers.spec.ts (5 tests) 5ms
 ✓ src/routes/functions/cronexia/counters/counter-periodicity.test.ts (6 tests) 5ms
 ✓ src/routes/functions/cronexia/workflow/declaration-view-href.spec.ts (3 tests) 4ms
 ✓ src/routes/functions/cronexia/calendrier-annuel/calendar-day-schedule.test.ts (5 tests) 7ms
 ✓ src/routes/components/cronexia/schedule-catalog/schedule-parameters-view.spec.ts (4 tests) 6ms
 ✓ src/routes/functions/cronexia/planning/collective/month-header-segments.test.ts (4 tests) 5ms
 ✓ src/routes/components/cronexia/event/create/event-create.spec.ts (5 tests) 5ms
 ✓ src/routes/functions/common/chip-group/toggle-chip-code.test.ts (6 tests) 5ms
 ✓ src/_utility/cookie/function/server/session-seal.spec.ts (9 tests) 8ms
 ❯ src/routes/functions/cronexia/workflow/map-employee-hourly-event-from-api.spec.ts (0 test)
 ✓ src/routes/functions/cronexia/workflow-tab/catalog-tab-href-segment.spec.ts (3 tests) 4ms
 ✓ src/routes/api/chatbot/_functions/describe-relative-period.spec.ts (5 tests) 5ms
 ✓ src/routes/components/cronexia/cycle-catalog/cycle-parameters-fixture.spec.ts (4 tests) 6ms
 ✓ src/routes/functions/cronexia/workflow-tab/icon-from-workflow-tab-key.spec.ts (5 tests) 8ms
 ❯ src/routes/functions/cronexia/event/timeline-event-open-target.spec.ts (0 test)
 ✓ src/routes/functions/cronexia/event-range-on-resource/build-conflict-resource-labels.spec.ts (6 tests) 5ms
 ✓ src/routes/functions/cronexia/calendrier-annuel/calendar-rest-days.test.ts (5 tests) 5ms
 ✓ src/routes/functions/cronexia/delegation/delegation-mode.spec.ts (8 tests) 6ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/organize-workflow-is-missing-target-event.spec.ts (3 tests) 4ms
 ✓ src/routes/functions/cronexia/workflow/employee-demands-synthesis.spec.ts (6 tests) 23ms
 ✓ src/routes/components/common/chatbot/chatbot-dock-fit.spec.ts (5 tests) 18ms
 ✓ src/_utility/api/forward-client-headers.spec.ts (3 tests) 5ms
 ✓ src/routes/functions/common/home/collaborator-home-widget-visibility.spec.ts (2 tests) 5ms
 ✓ src/routes/components/cronexia/rights-employee/employee-rights-page.spec.ts (2 tests) 7ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/split-organize-tabs-by-affected.spec.ts (1 test) 5ms
 ✓ src/routes/components/common/chatbot/chatbot-navigation.spec.ts (2 tests) 9ms
 ✓ src/routes/api/chatbot/_functions/describe-absence-period.spec.ts (4 tests) 6ms
 ✓ src/routes/functions/cronexia/declaration-hours/segments/display-segments.spec.ts (2 tests) 6ms
 ✓ src/routes/functions/cronexia/workflow/get-workflow-resource-attachments-max.spec.ts (4 tests) 6ms
 ✓ src/routes/components/common/chatbot/chatbot-follow-up.spec.ts (5 tests) 5ms
 ✓ src/_utility/export/export-formats-allowed.test.ts (5 tests) 5ms
 ✓ src/routes/functions/cronexia/delegation/pick-delegation-owner.spec.ts (4 tests) 4ms
 ✓ src/routes/components/common/form/select/render-workflow-tab-icon-option.spec.ts (3 tests) 4ms
 ✓ src/routes/api/chatbot/_functions/guess-page.spec.ts (13 tests) 7ms
 ✓ src/routes/api/chatbot/_functions/verbatim-comment.spec.ts (5 tests) 7ms
 ✓ src/routes/components/cronexia/rights-hr-individual/hr-individual-rights-period.spec.ts (2 tests) 4ms
 ✓ src/config/events/resources-events-quantity-sum-config.spec.ts (4 tests) 6ms
 ✓ src/routes/functions/cronexia/resource/file/form/histo-cycle-companion.spec.ts (3 tests) 4ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/initial-organize-catalog-selection.spec.ts (3 tests) 4ms
 ✓ src/_utility/navigation/400-params/472-build-filter-navigation-href.spec.ts (2 tests) 4ms
 ❯ src/routes/functions/cronexia/workflow/skips-day-conflict-check-on-submit.spec.ts (0 test)
 ✓ src/routes/functions/common/table/view-all-max-rows.test.ts (4 tests) 4ms
 ✓ src/routes/functions/cronexia/workflow/demand-type-visual.spec.ts (2 tests) 4ms
 ✓ src/config/ai-chat-version-config.spec.ts (5 tests) 5ms
 ✓ src/routes/functions/cronexia/planning/favorites/favorite-form-counters-panel.spec.ts (3 tests) 4ms
 ✓ src/routes/functions/cronexia/event-range-on-resource/workflow-state-key.spec.ts (4 tests) 4ms
 ✓ src/routes/functions/common/dom/edge-auto-scroll.spec.ts (4 tests) 4ms
 ✓ src/routes/components/common/chatbot/chatbot-balance-soldes.spec.ts (3 tests) 4ms
 ✓ src/routes/functions/cronexia/delegation/resolve-delegations-period.spec.ts (2 tests) 4ms
 ✓ src/_utility/api/post-back-graphql.spec.ts (4 tests) 4ms
 ✓ src/routes/functions/common/date/seniority-label.spec.ts (3 tests) 4ms
 ✓ src/routes/functions/cronexia/calendar/calendar-easter.spec.ts (3 tests) 12ms
 ✓ src/routes/components/cronexia/rights-employee/employee-rights-history.spec.ts (3 tests) 5ms
 ✓ src/config/themes/function/resolve-brand-theme.test.ts (3 tests) 4ms
 ✓ src/config/login-profile-choice-config.spec.ts (6 tests) 4ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/is-reserved-workflow-tab-name.spec.ts (2 tests) 4ms
 ✓ src/_utility/navigation/400-params/405-page-default-date-range.spec.ts (2 tests) 4ms
 ✓ src/routes/functions/common/auth/is-static-asset-path.spec.ts (9 tests) 5ms
 ✓ src/routes/functions/cronexia/event-range-on-resource/parse-created-by-names.spec.ts (3 tests) 4ms
 ✓ src/routes/functions/common/tooltip/swipe-to-close.spec.ts (4 tests) 4ms
 ✓ src/routes/functions/cronexia/counters/counter-chip-options.test.ts (2 tests) 11ms
 ✓ src/routes/functions/common/table/next-sort-state.spec.ts (3 tests) 6ms
 ✓ src/routes/functions/common/ai/get-is-ai-available.spec.ts (4 tests) 4ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/workflow-tab-custom-icon-keys.spec.ts (1 test) 4ms
 ✓ src/routes/functions/cronexia/workflow/workflow-schedule-overload-create.helpers.spec.ts (3 tests) 4ms
 ✓ src/routes/api/chatbot/_functions/hour-request.spec.ts (11 tests) 8ms
 ✓ src/routes/functions/cronexia/declaration-presence/declaration-planned-days.spec.ts (1 test) 3ms
 ✓ src/routes/functions/common/dom/horizontal-swipe.spec.ts (4 tests) 4ms
 ✓ src/routes/functions/cronexia/workflow-tab/choice-tab-cards-to-demand-items.spec.ts (1 test) 4ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/is-organize-catalog-drag.spec.ts (1 test) 3ms
 ✓ src/_utility/date/iso-week.spec.ts (3 tests) 4ms
 ✓ src/routes/api/chatbot/_functions/presence-question.spec.ts (10 tests) 7ms
 ✓ src/routes/functions/cronexia/planning/collective/collective-schedule.data.spec.ts (3 tests) 4ms
 ✓ src/routes/functions/common/menu/secondary/icon-from-menu-key.spec.ts (4 tests) 6ms
 ✓ src/lib/graphql/events/fragments/event-by-day-workflow-resource-selection.spec.ts (2 tests) 4ms
 ✓ src/routes/functions/cronexia/delegation/delegations-menu-link.spec.ts (2 tests) 6ms
 ✓ src/routes/functions/common/dom/keep-in-viewport.spec.ts (4 tests) 4ms
 ✓ src/routes/functions/cronexia/declaration/declaration-return-label.spec.ts (2 tests) 4ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/organize-workflow-tab-usage-label.spec.ts (1 test) 3ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/workflow-tab-icon-custom-svg.spec.ts (1 test) 3ms
 ✓ src/_utility/date/to-paris-calendar-date.spec.ts (2 tests) 18ms
 ✓ src/routes/functions/cronexia/planning/collective/planning-hour-picker.helpers.spec.ts (2 tests) 4ms
 ✓ src/routes/functions/cronexia/workflow-tab/demand-type-cards-from-hidden-ids.spec.ts (1 test) 4ms
 ✓ src/routes/functions/cronexia/workflow-tab/organize/workflow-tab-code-from-label.spec.ts (1 test) 4ms
stdout | src/_utility/time/format-time-for-api.spec.ts > formatTimeForAPI > garde les autres heures
formatTimeForAPI h format result: 10:15:00Z

 ✓ src/_utility/time/format-time-for-api.spec.ts (2 tests) 5ms
 ✓ src/routes/functions/cronexia/vacation-rights/filter-vacation-rights.spec.ts (1 test) 3ms

⎯⎯⎯⎯⎯⎯ Failed Suites 16 ⎯⎯⎯⎯⎯⎯

 FAIL  src/routes/components/cronexia/rights-employee/employee-rights-takes.spec.ts [ src/routes/components/cronexia/rights-employee/employee-rights-takes.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/config/color/function/event/resolve-event-color-category.ts
 ❯ src/config/color/function/event/resolve-event-color-category.ts:5:1
      3| // 👌 Types & props
      4| import type { EventModel } from '$typesGraphql';
      5| import { EventTypeEnum } from '$typesGraphql';
       | ^
      6| import type { EventColorCategory } from '../../type/event-color-catego…
      7|
 ❯ src/config/color-config.ts:12:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/16]⎯

 FAIL  src/routes/functions/cronexia/anomaly/transform-events.spec.ts [ src/routes/functions/cronexia/anomaly/transform-events.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/anomaly/transform-events.spec.ts
 ❯ src/routes/functions/cronexia/anomaly/transform-events.spec.ts:5:1
      3| import { describe, expect, it } from 'vitest';
      4|
      5| import { WorkflowStateEnum, WorkflowTypeEnum } from '$typesGraphql';
       | ^
      6|
      7| import { transformEvents } from './transform-events';

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/16]⎯

 FAIL  src/routes/functions/cronexia/calendrier-annuel/calendar-pending-requests.helpers.spec.ts [ src/routes/functions/cronexia/calendrier-annuel/calendar-pending-requests.helpers.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/calendrier-annuel/calendar-pending-requests.helpers.spec.ts
 ❯ src/routes/functions/cronexia/calendrier-annuel/calendar-pending-requests.helpers.spec.ts:5:1
      3| import { describe, expect, it } from 'vitest';
      4|
      5| import { EventTypeEnum, WorkflowStateEnum, WorkflowTypeEnum } from '$t…
       | ^
      6|
      7| import { buildCalendarPendingRequests } from './calendar-pending-reque…

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/16]⎯

 FAIL  src/routes/functions/cronexia/calendrier-annuel/index-calendar-events-by-date.hourly.spec.ts [ src/routes/functions/cronexia/calendrier-annuel/index-calendar-events-by-date.hourly.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/calendrier-annuel/index-calendar-events-by-date.hourly.spec.ts
 ❯ src/routes/functions/cronexia/calendrier-annuel/index-calendar-events-by-date.hourly.spec.ts:6:1
      4| import { describe, expect, it } from 'vitest';
      5|
      6| import { WorkflowTypeEnum } from '$typesGraphql';
       | ^
      7|
      8| import { indexCalendarEventsByDate } from './index-calendar-events-by-…


⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[4/16]⎯

 FAIL  src/routes/functions/cronexia/calendrier-annuel/planning-data-to-events.hour-absences.spec.ts [ src/routes/functions/cronexia/calendrier-annuel/planning-data-to-events.hour-absences.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/calendrier-annuel/planning-data-to-events.hour-absences.spec.ts
 ❯ src/routes/functions/cronexia/calendrier-annuel/planning-data-to-events.hour-absences.spec.ts:5:1
      3| import { describe, expect, it } from 'vitest';
      4|
      5| import { WorkflowStateEnum, WorkflowTypeEnum } from '$typesGraphql';
       | ^
      6|
 Test Files  16 failed | 239 passed | 2 skipped (257)
      7| import {

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[5/16]⎯

 FAIL  src/routes/functions/cronexia/event/event-by-day-direct-mutation.spec.ts [ src/routes/functions/cronexia/event/event-by-day-direct-mutation.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/event/event-by-day-direct-mutation.spec.ts
      Tests  1931 passed | 82 skipped (2013)
 ❯ src/routes/functions/cronexia/event/event-by-day-direct-mutation.spec.ts:5:1
   Start at  10:29:12
      3|
   Duration  59.13s (transform 4.76s, setup 0ms, import 15.62s, tests 5.57s, environment 519ms)
      4| // 🧰 Utility

      5| import { WorkflowTypeEnum } from '$typesGraphql';
       | ^
      6|
      7| // 🦾 Functions

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[6/16]⎯

 FAIL  src/routes/functions/cronexia/event/timeline-event-open-target.spec.ts [ src/routes/functions/cronexia/event/timeline-event-open-target.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/event/timeline-event-open-target.spec.ts
 ❯ src/routes/functions/cronexia/event/timeline-event-open-target.spec.ts:5:1
      3| import { describe, expect, it } from 'vitest';
      4|
      5| import { WorkflowTypeEnum } from '$typesGraphql';
       | ^
      6|
      7| import { resolveTimelineEventOpenTarget } from './timeline-event-open-…

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[7/16]⎯

 FAIL  src/routes/functions/cronexia/planning/filter-planning-datas-draft-for-viewer.spec.ts [ src/routes/functions/cronexia/planning/filter-planning-datas-draft-for-viewer.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/planning/filter-planning-datas-draft-for-viewer.spec.ts

 ❯ src/routes/functions/cronexia/planning/filter-planning-datas-draft-for-viewer.spec.ts:5:1
Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/config/color/function/event/resolve-event-color-category.ts
 ❯ src/config/color/function/event/resolve-event-color-category.ts:5:1
 ❯ src/config/color-config.ts:12:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }

      3| import { describe, expect, it } from 'vitest';
      4|
      5| import { WorkflowTypeEnum } from '$typesGraphql';
       | ^
      6|
      7| import { filterPlanningDatasDraftForViewer } from './filter-planning-d…

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[8/16]⎯

 FAIL  src/routes/functions/cronexia/planning/is-cancelled-or-refused-event.spec.ts [ src/routes/functions/cronexia/planning/is-cancelled-or-refused-event.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/planning/is-cancelled-or-refused-event.spec.ts
 ❯ src/routes/functions/cronexia/planning/is-cancelled-or-refused-event.spec.ts:3:1
      1| import { describe, expect, it } from 'vitest';
      2|
      3| import { WorkflowTypeEnum } from '$typesGraphql';
       | ^
      4|
      5| import { isCancelledOrRefusedEvent } from './is-cancelled-or-refused-e…

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[9/16]⎯

 FAIL  src/routes/functions/cronexia/planning/planning-workflow-resolve.helpers.spec.ts [ src/routes/functions/cronexia/planning/planning-workflow-resolve.helpers.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/planning/planning-workflow-resolve.helpers.spec.ts
 ❯ src/routes/functions/cronexia/planning/planning-workflow-resolve.helpers.spec.ts:5:1
      3| import { describe, expect, it } from 'vitest';
      4|
      5| import { WorkflowStateEnum, WorkflowTypeEnum } from '$typesGraphql';
       | ^
      6| import type { WorkflowAccordionModel } from '$functions/cronexia/workf…
      7|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[10/16]⎯

 FAIL  src/routes/functions/cronexia/workflow/build-workflow-demand-details.hourly.spec.ts [ src/routes/functions/cronexia/workflow/build-workflow-demand-details.hourly.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/build-workflow-demand-details.hourly.spec.ts
 ❯ src/routes/functions/cronexia/workflow/build-workflow-demand-details.hourly.spec.ts:5:1
      3|
      4| // 👌 Types & props
      5| import { WorkflowStateEnum, WorkflowTypeEnum } from '$typesGraphql';
       | ^
      6|
      7| // 🦾 Functions

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[11/16]⎯

 FAIL  src/routes/functions/cronexia/workflow/describe-workflow-validation-candidate.spec.ts [ src/routes/functions/cronexia/workflow/describe-workflow-validation-candidate.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/describe-workflow-validation-candidate.spec.ts
 ❯ src/routes/functions/cronexia/workflow/describe-workflow-validation-candidate.spec.ts:5:1
      3|
      4| // 👌 Types & props
      5| import { WorkflowStateEnum, WorkflowTypeEnum } from '$typesGraphql';
       | ^
      6|
      7| // 🦾 Functions

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[12/16]⎯

 FAIL  src/routes/functions/cronexia/workflow/hourly-event-workflow-create.helpers.spec.ts [ src/routes/functions/cronexia/workflow/hourly-event-workflow-create.helpers.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/hourly-event-workflow-create.helpers.spec.ts
 ❯ src/routes/functions/cronexia/workflow/hourly-event-workflow-create.helpers.spec.ts:5:1
      3|
      4| // 👌 Types & props
      5| import { WorkflowStateEnum } from '$typesGraphql';
       | ^
      6|
      7| // 🦾 Functions

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[13/16]⎯

 FAIL  src/routes/functions/cronexia/workflow/map-employee-hourly-event-from-api.spec.ts [ src/routes/functions/cronexia/workflow/map-employee-hourly-event-from-api.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/_utility/workflow/function/map-workflow-resource-state-from-api.ts
 ❯ src/_utility/workflow/function/map-workflow-resource-state-from-api.ts:1:1
      1| import { WorkflowDebugStateEnum, WorkflowStateEnum } from '$typesGraph…
       | ^
      2|
      3| import { asWorkflowDebugStateEnum } from './as-workflow-debug-state-en…
 ❯ src/routes/functions/cronexia/workflow/map-employee-hourly-event-from-api.ts:1:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[14/16]⎯

 FAIL  src/routes/functions/cronexia/workflow/map-validator-hourly-event-from-api.spec.ts [ src/routes/functions/cronexia/workflow/map-validator-hourly-event-from-api.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/_utility/workflow/function/map-workflow-resource-state-from-api.ts
 ❯ src/_utility/workflow/function/map-workflow-resource-state-from-api.ts:1:1
      1| import { WorkflowDebugStateEnum, WorkflowStateEnum } from '$typesGraph…
       | ^
      2|
      3| import { asWorkflowDebugStateEnum } from './as-workflow-debug-state-en…
 ❯ src/routes/functions/cronexia/workflow/map-validator-hourly-event-from-api.ts:9:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[15/16]⎯

 FAIL  src/routes/functions/cronexia/workflow/skips-day-conflict-check-on-submit.spec.ts [ src/routes/functions/cronexia/workflow/skips-day-conflict-check-on-submit.spec.ts ]
Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/skips-day-conflict-check-on-submit.spec.ts
 ❯ src/routes/functions/cronexia/workflow/skips-day-conflict-check-on-submit.spec.ts:5:1
      3|
      4| // 👌 Types & props
      5| import { WorkflowStateEnum, WorkflowTypeEnum } from '$typesGraphql';
       | ^
      6|
      7| // 🦾 Functions

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[16/16]⎯


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/anomaly/transform-events.spec.ts
 ❯ src/routes/functions/cronexia/anomaly/transform-events.spec.ts:5:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/calendrier-annuel/calendar-pending-requests.helpers.spec.ts
 ❯ src/routes/functions/cronexia/calendrier-annuel/calendar-pending-requests.helpers.spec.ts:5:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/calendrier-annuel/index-calendar-events-by-date.hourly.spec.ts
 ❯ src/routes/functions/cronexia/calendrier-annuel/index-calendar-events-by-date.hourly.spec.ts:6:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/calendrier-annuel/planning-data-to-events.hour-absences.spec.ts
 ❯ src/routes/functions/cronexia/calendrier-annuel/planning-data-to-events.hour-absences.spec.ts:5:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/event/event-by-day-direct-mutation.spec.ts
 ❯ src/routes/functions/cronexia/event/event-by-day-direct-mutation.spec.ts:5:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/event/timeline-event-open-target.spec.ts
 ❯ src/routes/functions/cronexia/event/timeline-event-open-target.spec.ts:5:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/planning/filter-planning-datas-draft-for-viewer.spec.ts
 ❯ src/routes/functions/cronexia/planning/filter-planning-datas-draft-for-viewer.spec.ts:5:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/planning/is-cancelled-or-refused-event.spec.ts
 ❯ src/routes/functions/cronexia/planning/is-cancelled-or-refused-event.spec.ts:3:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/planning/planning-workflow-resolve.helpers.spec.ts
 ❯ src/routes/functions/cronexia/planning/planning-workflow-resolve.helpers.spec.ts:5:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/build-workflow-demand-details.hourly.spec.ts
 ❯ src/routes/functions/cronexia/workflow/build-workflow-demand-details.hourly.spec.ts:5:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/describe-workflow-validation-candidate.spec.ts
 ❯ src/routes/functions/cronexia/workflow/describe-workflow-validation-candidate.spec.ts:5:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/hourly-event-workflow-create.helpers.spec.ts
 ❯ src/routes/functions/cronexia/workflow/hourly-event-workflow-create.helpers.spec.ts:5:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/_utility/workflow/function/map-workflow-resource-state-from-api.ts
 ❯ src/_utility/workflow/function/map-workflow-resource-state-from-api.ts:1:1
 ❯ src/routes/functions/cronexia/workflow/map-employee-hourly-event-from-api.ts:1:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/_utility/workflow/function/map-workflow-resource-state-from-api.ts
 ❯ src/_utility/workflow/function/map-workflow-resource-state-from-api.ts:1:1
 ❯ src/routes/functions/cronexia/workflow/map-validator-hourly-event-from-api.ts:9:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }


Error: Error: Cannot find module '$typesGraphql' imported from /home/runner/work/cronexia-gta-front-v2/cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/skips-day-conflict-check-on-submit.spec.ts
 ❯ src/routes/functions/cronexia/workflow/skips-day-conflict-check-on-submit.spec.ts:5:1

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }

error: script "test" exited with code 1
Error: Process completed with exit code 1.
