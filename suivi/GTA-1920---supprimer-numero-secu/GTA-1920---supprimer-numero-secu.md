# Suppression du champ "numéro de sécu" ou neutralisation

Le champ numéro de sécu n’apparait nulle part dans le front: il n’est même pas visible dans la liste des champs pouvant être ajoutés à un onglet du dossier.

Il faut donc le supprimer ou le neutraliser totalement car c’est un champ actuellement obligatoire lors de l’import via CSV ou API ce qui est un non sens (champ obligatoire jamais visible) et même problématique d’un point de vue RGPD.

Si un client décide de gérer les numéros de sécu, ce sera un champ custom.

## Dev

File locations:

- cronexia-gta-back\app\prisma\schema\resource.prisma
- cronexia-gta-back\app\src\resources

Might have some artifacts in frontend too

- Input components : cronexia-gta-front-v2\app\src\routes\components\common\form
- employee file page, used to have a read only input displayed : cronexia-gta-front-v2\app\src\routes\(app)\(with-filters)\employee-file\population\[[population]]\resource\[[resource]]\dateStart\[[dateStart]]\dateEnd\[[dateEnd]]\+page.svelte
- admin > fields > manage : cronexia-gta-front-v2\app\src\routes\(app)\(without-filters)\admin\fields\manage

## Inventaire et conséquences

Décision : commenter `socialSecurityNumber`, ne pas l'effacer, pour pouvoir revenir en arrière. La colonne SQL et son index unique restent. Pas de migration, pas de `DROP COLUMN`. Les fichiers générés (`schema.gql`, client Prisma, `graphql.ts`, `schema.graphql`) ne sont pas édités à la main.

Le champ est déjà facultatif en Prisma (`BigInt? @unique`) et dans `CreateResourceInput` (`nullable: true`). Il reste obligatoire sur l'API client JSON, et c'est une colonne directe de l'import CSV. C'est le non-sens du ticket : un NIR exigé à l'import, jamais proposé dans le dossier.

Le `ResourceField` « Numéro de sécurité sociale » n'existe que dans le seed dev (`isCustom: false`, `isReadOnly: true`). Il n'est posé sur aucun onglet. Les seeds demo et arte ne le déclarent pas. D'où l'absence dans l'admin (liste des champs ajoutables à un onglet) et dans le dossier. Il n'y a pas d'input dédié dans `components/common/form` : le dossier injecte seulement une valeur lecture seule quand l'API renvoie le champ.

### Déjà neutralisé (ne pas réouvrir)

- Argument GraphQL `ResourceInput` : `cronexia-gta-back/app/src/_utility/graphql/inputs/resource.input.ts`
- Lookup dans `craft-resource-where-input.ts`
- Lookup workflow dans `find-resource-id-for-resources-workflow-resource.ts`
- Anciennes lignes de `prisma/seed-po.ts`

### Back — comportement réel (à commenter)

Obligation d'import, le bug du ticket :

- `app/src/resources/client-api/resources-client.service.ts` — validation « champ obligatoire », conversion BigInt, contrôle d'unicité, écriture Prisma
- `app/src/resources/client-api/swagger-dynamic.setup.ts` — swagger : matricule et NIR toujours obligatoires
- `app/src/resources/client-api/resources-client.controller.ts`, `upsert-resource.controller.ts`, `upsert-resource.service.ts` — mêmes textes
- `app/src/resources/client-api/csv-import/resource-csv-import.constant.ts` — `socialSecurityNumber` dans `CSV_IMPORT_DIRECT_COLUMNS`
- `app/src/resources/client-api/csv-import/functions/validate-resource-csv-headers.ts` — commentaire associé
- Specs : `resource-csv-import.spec.ts`, `resources-client-referentiel.spec.ts`
- Exemples : `_docs/imports-csv-exemples/import_resources_create-many.csv`, `import_resources_upsert-many.csv`

Conséquence : create, update, upsert et CSV n'exigent plus le NIR et ne l'écrivent plus. Le matricule suffit.

Contrat GraphQL encore exposé :

- Modèles : `resource.model.ts`, `resource-no-deps.model.ts`, `find-at-date-return.model.ts`, `resource.entity.ts`
- DTO : `create-resource.input.ts`, `create-many-resources.input.ts`, `find-unique-resource.ts`, `where-resource.input.ts`, `order-by-resource.input.ts`, `enums/resource-distinct.enum.ts`
- `resources.resolver.ts` — `findUnique` par NIR et `distinct` sur cette colonne (vers 921, 1113-1123, 1271-1281, 3388, 3716). Vers 3389 la valeur copiée est `findUniqueResource.matricule`, pas le NIR : à commenter avec le bloc, sans correctif à part.

Conséquence : plus de recherche unique par NIR. Restent le matricule, `id` et `idResource`. Les requêtes qui sélectionnent encore le champ cassent tant que le front n'est pas commenté en même temps.

Lectures et écritures résiduelles :

- `resources.service.ts` vers 2626 — import CSV legacy qui écrit la colonne quand le nom de champ est `socialSecurityNumber`
- `functions/service/generate-csv-example-data.ts` — l'exemple CSV émet toujours cette colonne
- `functions/find-values-at-date.ts` — le NIR est renvoyé avec les valeurs à date
- `functions/aggreg/aggregate-en-dur.ts`, `group-by-en-dur.ts`
- `functions/service/validate-and-parse-record.ts` — `Joi.number().required()`, aucun appelant

Nom réservé (empêche un champ custom du même nom) :

- `app/src/resource-fields/constants/reserved-resource-field-names.ts`
- `app/src/resources/client-api/reserved-resource-fields.constant.ts`
- `resource-fields.service.ts` suit ces constantes (création refusée, name/type figés). Seul le commentaire « matricule, NIR » est à ajuster.

Seed du ResourceField système :

- `prisma/seeds-new/50-dev/resource-fields/resource-fields.dev.seed.ts` — bloc `name: 'socialSecurityNumber'`

Seeds qui passent la valeur à `resource.create` (environ 90 fichiers `seeds-new` dev, demo, demo-arte), en général via `createFakeSocialSecurityNumber` :

- À commenter avant le champ Prisma, sinon `resource.create` refuse la propriété
- Laisser le helper `src/_utility/strings/create-fake-social-security-number`
- Générateur : `src/_generators/seed/resources/functions/write-inputs/resource.ts`
- Aussi : `prisma/_bp_add_one_resource.ts` et les deux `_bp_add_one_resource-to-demo-w-refacto.ts` (demo et demo-arte)

Colonne, en dernier :

- `prisma/schema/resource.prisma` lignes 17-19 — commenter le champ actif
- Ne pas modifier `prisma/schema/migrations/20261126154735_init/migration.sql`
- Ne pas lancer `prisma migrate` : il proposerait un `DROP COLUMN`

### Back — ne pas commenter

Chaînes de documentation GraphQL, pas des requêtes exécutées. Les laisser évite un diff énorme ; les exemples deviennent obsolètes.

- Resolvers dont les descriptions d'exemple sélectionnent `socialSecurityNumber` : clockings, events (by day, range, group), cycles, schedules, ct-results, resource-*-vals, badge-on-resources, anomaly-instances, populations, pop-criterias, schedule-type-over-load, tests-and-examples
- `docs/*.doc.ts` : resources, users, user-profile-instances, ar-movement-instances, ar-resource-balances, theoretical-clocking-overloads
- JSON historiques `prisma/seeds/resource/*.json` (jeux 1k) et `seed-po.ts` (déjà commenté)
- Client Prisma généré

### Front — à commenter

Hors `lib/generated` et `app/generated`.

Création et affichage dossier :

- `routes/api/resource/create/+server.ts` — rejette la création si le NIR est absent, et l'envoie dans le payload
- `routes/functions/cronexia/resource/file/form/action/build-resource-create-input.ts` + spec
- `routes/functions/cronexia/resource/file/form/action/resource-create.ts`
- `routes/functions/cronexia/resource/file/build-random-resource-values.ts` + spec
- Page dossier `employee-file/.../+page.svelte` vers 218 — injection lecture seule si l'API renvoie une valeur
- `routes/functions/cronexia/resource-fields/has-any-resource-values.ts` — le NIR y est traité comme une colonne physique

Sélections GraphQL exécutées (une ligne `socialSecurityNumber` dans le retour `resource`). Sans les commenter en même temps que le schéma, ces opérations cassent :

- `lib/graphql/auth/me/queries/me.ts`
- `lib/graphql/resources/queries/getResourceByMatricule.ts`
- `lib/graphql/resources/queries/getResourceWithMovementInstances.ts`
- Events : `createEventByDay.ts`, `updateEventByDay.ts`, `deleteEvent.ts`, `createEventRangeOnResource.ts`, `updateEventRangeOnResource.ts`, `deleteEventRangeOnResource.ts`
- `routes/components/common/ai/discussion/paths/event/AiPathEventCreate.svelte`
- Schedules : `createScheduleOverLoadForResource.ts`, `deleteScheduleOverLoadForResource.ts`
- Clockings : `createClocking.ts`, `updateClocking.ts`, `deleteClockings.ts`
- Droits : `createArMovementInstances.ts`, `updateArMovementInstances.ts`, `deleteArMovementInstances.ts`, `absenceRightGenerate.ts`
- `lib/graphql/anomalies/queries/getAnomalyInstances.ts`
- Profils : `userProfileInstances.ts`, `deleteUserProfileInstances.ts`
- Types locaux : `resourceSubmitWorkflowResource.ts`, `addWorkflowResourceAttachments.ts`
- `lib/graphql/resources/queries/functions/resourcesValuesAtEffectDate.ts` — liste `doNotProcess`
- `routes/api/resource/_validate-workflow-resource-mutation-body.ts` — le NIR est un identifiant accepté parmi d'autres ; matricule, `id` et `idResource` restent

### Conséquences assumées

- Import CSV et API : le matricule seul suffit. Un client qui veut gérer les numéros de sécu crée un ResourceField custom. Retirer le nom des listes réservées autorise ce nom sur une base fraîche.
- Les bases déjà seedées gardent la colonne, les valeurs, et la ligne `ResourceField` dev déjà insérée. Commenter le seed ne supprime pas cette ligne : le nom reste pris sur ces bases tant qu'il n'y a pas de nettoyage de données. Ce nettoyage serait une suppression, hors scope.
- RGPD : les NIR déjà en base restent lisibles en SQL. Le commentaire coupe l'exposition applicative, pas le stockage. Effacer la colonne serait un ticket à part, irréversible.
- Revenir en arrière = décommenter. Pas de migration à inverser.

### Ordre prévu

1. Cet inventaire (fait ici, aucun fichier de la stack).
2. Import back : plus obligatoire, plus écrit. La colonne Prisma reste.
3. Front création et dossier.
4. Nom réservé et seed du ResourceField dev.
5. Contrat GraphQL et sélections front, dans la même passe.
6. Lectures et écritures résiduelles.
7. Seeds resources et générateur.
8. Champ dans `resource.prisma`, sans migration.
