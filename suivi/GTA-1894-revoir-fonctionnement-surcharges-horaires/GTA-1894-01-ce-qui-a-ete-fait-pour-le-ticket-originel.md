# GTA-1894 — message quand une surcharge d'horaire existe déjà

Une demande de changement d'horaire sur une date déjà surchargée (admin, gestionnaire RH, ou une autre demande) tombait sur la contrainte unique `resourceId` + `effectDate`. Le front affichait `Conflit, le champ "inconnu" est déjà présent en BDD mais doit être unique.`

Le back lève maintenant `CRO_WR_000000050` avant l'insert. Le toast devient :

`Vous avez déjà une surcharge d'horaire « VAR_7H » à cette date (25/11/2026).`

`VAR_7H` est le `code` de l'horaire **déjà en base**, pas celui que le salarié vient de choisir. Plusieurs jours : `« VAR_7H » le 25/11/2026, « REPOS » le 26/11/2026`. Le front n'a pas été modifié : il affiche déjà `messageHuman` dès que l'erreur GraphQL porte `errorCronexia`.

## Fichiers

- `cronexia-gta-back/app/src/_utility/error/cronexia-error-dictionnary.ts` — entrée `CRO_WR_000000050`, variable `{details}`.
- `cronexia-gta-back/app/src/workflow-resources/functions/guard-existing-schedule-overload-for-resource.ts` — lecture des `ScheduleOverLoadForResource` de la ressource sur les dates demandées, puis `ConflictException`.
- `cronexia-gta-back/app/src/workflow-resources/functions/guard-existing-schedule-overload-for-resource.spec.ts` — 4 tests (aucune ligne, un code `VAR_7H`, deux dates, ligne de la demande en cours ignorée). Lancés à la main : 4 passed.
- `cronexia-gta-back/app/src/workflow-resources/workflow-resources.resolver.ts` — appel à la création (`createWorkflowResource`) et à la mise à jour si `scheduleOverLoads.create` ou `createMany` est envoyé.
- `cronexia-gta-back/app/src/workflow-resources/docs/create.doc.ts` — une phrase sur le paragraphe `scheduleOverLoads`.

Le message générique reste dans `cronexia-gta-front-v2/app/src/routes/api/workflow-resource/create/+server.ts`. Il ne s'applique plus à ce cas, parce que l'erreur Cronexia est prioritaire.

## Surcharge d'horaire et workflow

`ScheduleOverLoadForResource` n'autorise qu'une surcharge par ressource et par date (`@@unique([resourceId, effectDate])`). Une surcharge posée hors demande (planning, admin, RH) a `workflowResourceId` vide. Une demande de type `scheduleOverload` crée ces lignes en même temps que le `WorkflowResource`, une par jour (`effectDate` + `schedule.connect` par `code`).

L'ancien garde `CRO_WR_000000017` ne voit qu'une **autre demande du même workflow** dans un état bloquant. Une surcharge admin, un autre workflow, ou un brouillon lui échappent : Prisma renvoyait P2002, sans nom de champ, d'où « inconnu ».

Le nouveau garde s'exécute avant celui-là et avant l'insert. Il nomme le `Schedule.code` de la ligne déjà présente. À la mise à jour, les lignes déjà rattachées à la demande éditée sont ignorées ; une surcharge admin sur la même date bloque quand même.

La clé unique ne change pas. Une demande annulée ou refusée qui a encore sa ligne de surcharge continue de bloquer la date. Deux fois la même date dans un seul envoi, sans ligne déjà en base, retombe encore sur le message générique.
