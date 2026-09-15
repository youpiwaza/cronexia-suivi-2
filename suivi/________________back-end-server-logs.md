[1]  + 52501 done       clear
$ bun run reset-bdd-seed-dev
$ bun i && rm -Rf prisma/schema/migrations && docker compose -f docker-compose-database-postgresql.yml -p 'cronexia-gta-app' down && docker compose -f docker-compose-database-postgresql.yml rm -fsv && docker volume prune -af && docker compose -f docker-compose-database-postgresql.yml -p 'cronexia-gta-app' up -d && sleep 1 && bun run prisma generate && bun prisma migrate dev --name "init" && ts-node prisma/seed-dev.ts && ts-node prisma/seeds/counter/run-gen-cpts.ts
[1.04ms] ".env"
bun install v1.2.21 (7c45ed97)

Checked 1810 installs across 1604 packages (no changes) [404.00ms]
[+] down 7/7
 ✔ Container cronexia_db_admin      Removed                                                                                      0.1s
 ✔ Container cronexia_cache_admin   Removed                                                                                      0.1s
 ✔ Container cronexia_db_admin_pg   Removed                                                                                      0.1s
 ✔ Container cronexia_cache_queues  Removed                                                                                      0.1s
 ✔ Container cronexia_db_postgres   Removed                                                                                      0.1s
 ✔ Container cronexia_cache         Removed                                                                                      0.1s
 ✔ Network cronexia-gta-app_default Removed                                                                                      0.4s
No stopped containers
Deleted Volumes:
cronexia-gta-app_db_postgres__data
515edcc1d2dabb295f5c1986c87a6bb35b483a3f8c2074cb20e99fe5fa4b1c02
cronexia-gta-app_db_admin_pg__pref
cronexia-gta-app_cache_redis__data
cronexia-gta-app_cache_redis_queues__data
cronexia-gta-app_cache_redis_admin__data

Total reclaimed space: 84.23MB
[+] up 12/12
 ✔ Network cronexia-gta-app_default                 Created                                                                      0.1s
 ✔ Volume cronexia-gta-app_db_postgres__data        Created                                                                      0.0s
 ✔ Volume cronexia-gta-app_cache_redis_admin__data  Created                                                                      0.0s
 ✔ Volume cronexia-gta-app_cache_redis__data        Created                                                                      0.0s
 ✔ Volume cronexia-gta-app_cache_redis_queues__data Created                                                                      0.0s
 ✔ Volume cronexia-gta-app_db_admin_pg__pref        Created                                                                      0.0s
 ✔ Container cronexia_db_admin                      Started                                                                      2.3s
 ✔ Container cronexia_db_postgres                   Started                                                                      1.9s
 ✔ Container cronexia_cache                         Started                                                                      0.9s
 ✔ Container cronexia_cache_queues                  Started                                                                      1.6s
 ✔ Container cronexia_cache_admin                   Started                                                                      1.1s
 ✔ Container cronexia_db_admin_pg                   Started                                                                      2.4s
Loaded Prisma config from prisma.config.ts.

Prisma config detected, skipping environment variable loading.
Prisma schema loaded from prisma/schema

✔ Generated Prisma Client (v6.19.0) to ./prisma/generated/client in 1.39s

✔ Generated Prisma Docs Generator to ./prisma/schema/docs in 1.86s

Start by importing your Prisma Client (See: https://pris.ly/d/importing-client)

Tip: Want to turn off tips and other hints? https://pris.ly/tip-4-nohints

Loaded Prisma config from prisma.config.ts.

Prisma config detected, skipping environment variable loading.
Prisma schema loaded from prisma/schema
Datasource "db": PostgreSQL database "cronexia_gta", schema "public" at "localhost:5433"

Applying migration `20260915111606_init`

The following migration(s) have been created and applied from new schema changes:

prisma/schema/migrations/
  └─ 20260915111606_init/
    └─ migration.sql

Your database is now in sync with your schema.

✔ Generated Prisma Client (v6.19.0) to ./prisma/generated/client in 1.24s
✔ Generated Prisma Docs Generator to ./prisma/schema/docs in 2.29s


🧮 valueFinal generated columns installed on CtResultFlt{Daily,Weekly,Monthly,Yearly}
🌊✔️ WorkflowOnWorkflowTab unassigned-pool unique index installed
🌱🔧 Seeding Config...
✅🔧 Config seeded successfully
🌱🔧🔐 Seeding Config > Password Policy...
✅🔧🔐 Config > Password Policy seeded successfully
🌱🔧📋📅 Seeding Config > PAGE_DECLA_DAYS...
✅🔧📋📅 Config > PAGE_DECLA_DAYS seeded successfully
🌱🔧📋⏱️ Seeding Config > PAGE_DECLA_HOURS...
✅🔧📋⏱️ Config > PAGE_DECLA_HOURS seeded successfully
🌱🔧🗓️ Seeding Config > IS_PLANNING_FILTERS_DISPLAYED...
✅🔧🗓️ Config > IS_PLANNING_FILTERS_DISPLAYED seeded successfully (14)
🌱🔐 Seeding User Rights...
✅🔐 User Rights seeded successfully
🌱👤🎭 Seeding User Profiles...
✅👤🎭 User Profiles seeded successfully
🌱🧭 Seeding MenuLink catalog...

❌ 👨‍💻🌱 Dev Seed process failed: PrismaClientValidationError:
Invalid `prisma.menuLink.createMany()` invocation in
/home/youpiwaza/code/cronexia-gta-back/app/prisma/seeds-new/01-required/menu-link/function/seed-menu-links.ts:17:25

  14   return new Map();
  15 }
  16
→ 17 await prisma.menuLink.createMany({
       data: [
         {
           name: "demandes_employee",
           label: "Demandes",
           href: "/demands/summary",
           iconKey: "clipboard",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000006"
         },
         {
           name: "badger",
           label: "Badger",
           href: null,
           iconKey: "clock",
           isButton: true,
           timeManagementModes: "En heures avec pointages réels",
           userRightId: "00000000-7400-0000-0000-000000000003"
         },
         {
           name: "declaratif",
           label: "Déclaratif",
           href: "/declaration-hours",
           iconKey: "clock",
           isButton: false,
           timeManagementModes: "En heures avec pointages théoriques",
           userRightId: "00000000-7400-0000-0000-000000000020"
         },
         {
           name: "planning_equipe",
           label: "Planning d'équipe",
           href: "/team-schedule",
           iconKey: "calendar",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000018"
         },
         {
           name: "declarer_mes_jours",
           label: "Déclarer mes jours",
           href: "/declaration-days",
           iconKey: "calendarWeek",
           isButton: false,
           timeManagementModes: "En jours",
           userRightId: "00000000-7400-0000-0000-000000000021"
         },
         {
           name: "droits",
           label: "Droits",
           href: "/vacation-rights",
           iconKey: "calendar2Heart",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000004"
         },
         {
           name: "calendrier",
           label: "Calendrier d'absences",
           href: "/calendar",
           iconKey: "calendar",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000017"
         },
         {
           name: "emploi_du_temps",
           label: "Emploi du temps",
           href: "/timetable",
           iconKey: "calendarWeek",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000017"
         },
         {
           name: "dossier",
           label: "Dossier",
           href: "/employee-file",
           iconKey: "folder",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000005"
         },
         {
           name: "demandes_manager",
           label: "Demandes",
           href: "/request-management",
           iconKey: "clipboard",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000006"
         },
         {
           name: "anomalies",
           label: "Anomalies",
           href: "/anomalies",
           iconKey: "exclamationCircle",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000007"
         },
         {
           name: "collectif",
           label: "Collectif",
           href: "/collective-schedule",
           iconKey: "calendar",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000008"
         },
         {
           name: "individuel",
           label: "Individuel",
           href: "/individual-schedule",
           iconKey: "calendar",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000009"
         },
         {
           name: "pointages",
           label: "Pointages",
           href: "/clockings",
           iconKey: "clock",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000010"
         },
         {
           name: "populations",
           label: "Populations",
           href: "/populations",
           iconKey: "people",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000016"
         },
         {
           name: "absences",
           label: "Absences",
           href: "/absences",
           iconKey: "calendar",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000013"
         },
         {
           name: "dossiers",
           label: "Dossiers",
           href: "/employee-file",
           iconKey: "folder",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000005"
         },
         {
           name: "compteurs",
           label: "Compteurs",
           href: "/counters",
           iconKey: "calculator",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000015"
         },
         {
           name: "indicateurs",
           label: "Indicateurs",
           href: "/indicators",
           iconKey: "graphUp",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000011"
         },
         {
           name: "rapports",
           label: "Rapports",
           href: "/reports",
           iconKey: "file",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000012"
         },
         {
           name: "synthese",
           label: "Synthèse",
           href: "/summary",
           iconKey: "checkCircle",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000014"
         },
         {
           name: "dossiers_admin",
           label: "Dossiers",
           href: "/admin/fields/manage",
           iconKey: "folder",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000019"
         },
         {
           name: "dossiers_des_ressources",
           label: "Dossiers des ressources",
           href: "/admin/fields/manage",
           iconKey: "folder",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000019"
         },
         {
           name: "populations_admin",
           label: "Populations",
           href: "/admin/population",
           iconKey: "people",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000019"
         },
         {
           name: "referentiels",
           label: "Référentiels",
           href: "/admin/enums",
           iconKey: "book",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000019"
         },
         {
           name: "organisations",
           label: "Organisations",
           href: "/admin/organizations",
           iconKey: "people",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000019"
         },
         {
           name: "compteurs_admin",
           label: "Compteurs",
           href: "/admin/counter",
           iconKey: "calculator",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000023"
         },
         {
           name: "rapports_admin",
           label: "Rapports",
           href: "http://localhost:5180",
           iconKey: "file",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000024"
         },
         {
           name: "appareils_connectes",
           label: "Appareils connectés",
           href: "/admin/sessions",
           iconKey: "clock",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000002"
         },
         {
           name: "reaction_au_conflit_devenements",
           label: "Réaction au conflit d'événements",
           href: "/admin/conflict-modes",
           iconKey: "shield",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000025"
         },
         {
           name: "liens_rapides_defauts_par_role",
           label: "Liens rapides: Défauts par rôle",
           href: "/admin/menus/quick-links-defaults",
           iconKey: "menuUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000019"
         },
         {
           name: "liens_rapide",
           label: "Liens rapide",
           href: "/customize/menus/quick-links",
           iconKey: "gear",
           isButton: false,
           timeManagementModes: null,
           userRightId: null
         },
         {
           name: "accueil",
           label: "Accueil",
           href: "/",
           iconKey: "user",
           isButton: false,
           timeManagementModes: null,
           userRightId: null
         },
         {
           name: "compteurs_periode",
           label: "Compteurs par période",
           href: "/counters/period",
           iconKey: "calculator",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000015"
         },
         {
           name: "compteurs_date",
           label: "Compteurs par date",
           href: "/counters/date",
           iconKey: "calculator",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000015"
         },
         {
           name: "declaration_view",
           label: "Vue déclaration",
           href: "/request-management/declaration-view",
           iconKey: "clipboard",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000006"
         },
         {
           name: "demo_couleurs",
           label: "Démo couleurs & composants",
           href: "/demo",
           iconKey: "code",
           isButton: false,
           timeManagementModes: null,
           userRightId: null
         },
         {
           name: "notifications_dev",
           label: "Notifications",
           href: "/_dev/notification",
           iconKey: "code",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "integration_heures_presence",
           label: "Intégration mes heures de présence",
           href: "/declaration-hours",
           iconKey: "clock",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000020"
         },
         {
           name: "absences_en_droit",
           label: "Absences en droit",
           href: "/_dev/test/absence-rights",
           iconKey: "bookOpen",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "generation_des_droits",
           label: "Génération des droits",
           href: "/_dev/test/generate-absence-rights",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "prise_de_droits",
           label: "Prise de droits",
           href: "/_dev/test/resource-add-movement-instance/00000000-0000-0000-0000-000000000059",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "ressources_mouvements",
           label: "Ressources - Mouvements",
           href: "/_dev/test/resource-movement-instances/00000000-0000-0000-0000-000000000059",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "exercices",
           label: "Exercices",
           href: "/_dev/test/exercise",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "mouvements",
           label: "Mouvements",
           href: "/_dev/test/movement",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "instances_de_mouvements",
           label: "Instances de mouvements",
           href: "/_dev/test/movement-instance",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "soldes",
           label: "Soldes",
           href: "/_dev/test/ar-resource-balance",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "crud_absenceright",
           label: "CRUD AbsenceRight",
           href: "/_dev/test/absence-right-crud",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "crud_relativedate",
           label: "CRUD RelativeDate",
           href: "/_dev/test/relative-date",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "crud_period",
           label: "CRUD Period",
           href: "/_dev/test/relative-period",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "crud_arpriority",
           label: "CRUD ArPriority",
           href: "/_dev/test/ar-priority",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "pieces_jointes_workflow",
           label: "Pièces jointes workflow",
           href: "/_dev/test/workflow-attachments",
           iconKey: "paperclip",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "erreurs",
           label: "Erreurs",
           href: "/_dev/test/errors",
           iconKey: "shield",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "routes",
           label: "Routes",
           href: "/_dev/routes",
           iconKey: "cornerDownRight",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         }
       ]
     })

Unknown argument `timeManagementModes`. Available options are marked with ?.
    at Nn (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:33:1363)
    at ei.handleRequestError (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:125:6911)
    at ei.handleAndLogRequestError (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:125:6593)
    at ei.request (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:125:6300)
    at async a (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:134:9551)
    at async seedMenuLinks (/home/youpiwaza/code/cronexia-gta-back/app/prisma/seeds-new/01-required/menu-link/function/seed-menu-links.ts:17:3)
    at async seedMenuLinkCatalog (/home/youpiwaza/code/cronexia-gta-back/app/prisma/seeds-new/01-required/menu-link/menu-link.seed.ts:12:18)
    at async runRequiredSeeds (/home/youpiwaza/code/cronexia-gta-back/app/prisma/seeds-new/01-required/_required.orchestrator.ts:38:28)
    at async main (/home/youpiwaza/code/cronexia-gta-back/app/prisma/seed-dev.ts:29:30) {
  clientVersion: '6.19.0'
}
❌ Fatal error during dev seeding: PrismaClientValidationError:
Invalid `prisma.menuLink.createMany()` invocation in
/home/youpiwaza/code/cronexia-gta-back/app/prisma/seeds-new/01-required/menu-link/function/seed-menu-links.ts:17:25

  14   return new Map();
  15 }
  16
→ 17 await prisma.menuLink.createMany({
       data: [
         {
           name: "demandes_employee",
           label: "Demandes",
           href: "/demands/summary",
           iconKey: "clipboard",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000006"
         },
         {
           name: "badger",
           label: "Badger",
           href: null,
           iconKey: "clock",
           isButton: true,
           timeManagementModes: "En heures avec pointages réels",
           userRightId: "00000000-7400-0000-0000-000000000003"
         },
         {
           name: "declaratif",
           label: "Déclaratif",
           href: "/declaration-hours",
           iconKey: "clock",
           isButton: false,
           timeManagementModes: "En heures avec pointages théoriques",
           userRightId: "00000000-7400-0000-0000-000000000020"
         },
         {
           name: "planning_equipe",
           label: "Planning d'équipe",
           href: "/team-schedule",
           iconKey: "calendar",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000018"
         },
         {
           name: "declarer_mes_jours",
           label: "Déclarer mes jours",
           href: "/declaration-days",
           iconKey: "calendarWeek",
           isButton: false,
           timeManagementModes: "En jours",
           userRightId: "00000000-7400-0000-0000-000000000021"
         },
         {
           name: "droits",
           label: "Droits",
           href: "/vacation-rights",
           iconKey: "calendar2Heart",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000004"
         },
         {
           name: "calendrier",
           label: "Calendrier d'absences",
           href: "/calendar",
           iconKey: "calendar",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000017"
         },
         {
           name: "emploi_du_temps",
           label: "Emploi du temps",
           href: "/timetable",
           iconKey: "calendarWeek",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000017"
         },
         {
           name: "dossier",
           label: "Dossier",
           href: "/employee-file",
           iconKey: "folder",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000005"
         },
         {
           name: "demandes_manager",
           label: "Demandes",
           href: "/request-management",
           iconKey: "clipboard",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000006"
         },
         {
           name: "anomalies",
           label: "Anomalies",
           href: "/anomalies",
           iconKey: "exclamationCircle",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000007"
         },
         {
           name: "collectif",
           label: "Collectif",
           href: "/collective-schedule",
           iconKey: "calendar",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000008"
         },
         {
           name: "individuel",
           label: "Individuel",
           href: "/individual-schedule",
           iconKey: "calendar",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000009"
         },
         {
           name: "pointages",
           label: "Pointages",
           href: "/clockings",
           iconKey: "clock",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000010"
         },
         {
           name: "populations",
           label: "Populations",
           href: "/populations",
           iconKey: "people",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000016"
         },
         {
           name: "absences",
           label: "Absences",
           href: "/absences",
           iconKey: "calendar",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000013"
         },
         {
           name: "dossiers",
           label: "Dossiers",
           href: "/employee-file",
           iconKey: "folder",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000005"
         },
         {
           name: "compteurs",
           label: "Compteurs",
           href: "/counters",
           iconKey: "calculator",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000015"
         },
         {
           name: "indicateurs",
           label: "Indicateurs",
           href: "/indicators",
           iconKey: "graphUp",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000011"
         },
         {
           name: "rapports",
           label: "Rapports",
           href: "/reports",
           iconKey: "file",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000012"
         },
         {
           name: "synthese",
           label: "Synthèse",
           href: "/summary",
           iconKey: "checkCircle",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000014"
         },
         {
           name: "dossiers_admin",
           label: "Dossiers",
           href: "/admin/fields/manage",
           iconKey: "folder",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000019"
         },
         {
           name: "dossiers_des_ressources",
           label: "Dossiers des ressources",
           href: "/admin/fields/manage",
           iconKey: "folder",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000019"
         },
         {
           name: "populations_admin",
           label: "Populations",
           href: "/admin/population",
           iconKey: "people",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000019"
         },
         {
           name: "referentiels",
           label: "Référentiels",
           href: "/admin/enums",
           iconKey: "book",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000019"
         },
         {
           name: "organisations",
           label: "Organisations",
           href: "/admin/organizations",
           iconKey: "people",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000019"
         },
         {
           name: "compteurs_admin",
           label: "Compteurs",
           href: "/admin/counter",
           iconKey: "calculator",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000023"
         },
         {
           name: "rapports_admin",
           label: "Rapports",
           href: "http://localhost:5180",
           iconKey: "file",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000024"
         },
         {
           name: "appareils_connectes",
           label: "Appareils connectés",
           href: "/admin/sessions",
           iconKey: "clock",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000002"
         },
         {
           name: "reaction_au_conflit_devenements",
           label: "Réaction au conflit d'événements",
           href: "/admin/conflict-modes",
           iconKey: "shield",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000025"
         },
         {
           name: "liens_rapides_defauts_par_role",
           label: "Liens rapides: Défauts par rôle",
           href: "/admin/menus/quick-links-defaults",
           iconKey: "menuUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000019"
         },
         {
           name: "liens_rapide",
           label: "Liens rapide",
           href: "/customize/menus/quick-links",
           iconKey: "gear",
           isButton: false,
           timeManagementModes: null,
           userRightId: null
         },
         {
           name: "accueil",
           label: "Accueil",
           href: "/",
           iconKey: "user",
           isButton: false,
           timeManagementModes: null,
           userRightId: null
         },
         {
           name: "compteurs_periode",
           label: "Compteurs par période",
           href: "/counters/period",
           iconKey: "calculator",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000015"
         },
         {
           name: "compteurs_date",
           label: "Compteurs par date",
           href: "/counters/date",
           iconKey: "calculator",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000015"
         },
         {
           name: "declaration_view",
           label: "Vue déclaration",
           href: "/request-management/declaration-view",
           iconKey: "clipboard",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000006"
         },
         {
           name: "demo_couleurs",
           label: "Démo couleurs & composants",
           href: "/demo",
           iconKey: "code",
           isButton: false,
           timeManagementModes: null,
           userRightId: null
         },
         {
           name: "notifications_dev",
           label: "Notifications",
           href: "/_dev/notification",
           iconKey: "code",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "integration_heures_presence",
           label: "Intégration mes heures de présence",
           href: "/declaration-hours",
           iconKey: "clock",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000020"
         },
         {
           name: "absences_en_droit",
           label: "Absences en droit",
           href: "/_dev/test/absence-rights",
           iconKey: "bookOpen",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "generation_des_droits",
           label: "Génération des droits",
           href: "/_dev/test/generate-absence-rights",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "prise_de_droits",
           label: "Prise de droits",
           href: "/_dev/test/resource-add-movement-instance/00000000-0000-0000-0000-000000000059",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "ressources_mouvements",
           label: "Ressources - Mouvements",
           href: "/_dev/test/resource-movement-instances/00000000-0000-0000-0000-000000000059",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "exercices",
           label: "Exercices",
           href: "/_dev/test/exercise",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "mouvements",
           label: "Mouvements",
           href: "/_dev/test/movement",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "instances_de_mouvements",
           label: "Instances de mouvements",
           href: "/_dev/test/movement-instance",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "soldes",
           label: "Soldes",
           href: "/_dev/test/ar-resource-balance",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "crud_absenceright",
           label: "CRUD AbsenceRight",
           href: "/_dev/test/absence-right-crud",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "crud_relativedate",
           label: "CRUD RelativeDate",
           href: "/_dev/test/relative-date",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "crud_period",
           label: "CRUD Period",
           href: "/_dev/test/relative-period",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "crud_arpriority",
           label: "CRUD ArPriority",
           href: "/_dev/test/ar-priority",
           iconKey: "calendarUil",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "pieces_jointes_workflow",
           label: "Pièces jointes workflow",
           href: "/_dev/test/workflow-attachments",
           iconKey: "paperclip",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "erreurs",
           label: "Erreurs",
           href: "/_dev/test/errors",
           iconKey: "shield",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         },
         {
           name: "routes",
           label: "Routes",
           href: "/_dev/routes",
           iconKey: "cornerDownRight",
           isButton: false,
           timeManagementModes: null,
           userRightId: "00000000-7400-0000-0000-000000000001"
         }
       ]
     })

Unknown argument `timeManagementModes`. Available options are marked with ?.
    at Nn (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:33:1363)
    at ei.handleRequestError (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:125:6911)
    at ei.handleAndLogRequestError (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:125:6593)
    at ei.request (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:125:6300)
    at async a (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:134:9551)
    at async seedMenuLinks (/home/youpiwaza/code/cronexia-gta-back/app/prisma/seeds-new/01-required/menu-link/function/seed-menu-links.ts:17:3)
    at async seedMenuLinkCatalog (/home/youpiwaza/code/cronexia-gta-back/app/prisma/seeds-new/01-required/menu-link/menu-link.seed.ts:12:18)
    at async runRequiredSeeds (/home/youpiwaza/code/cronexia-gta-back/app/prisma/seeds-new/01-required/_required.orchestrator.ts:38:28)
    at async main (/home/youpiwaza/code/cronexia-gta-back/app/prisma/seed-dev.ts:29:30) {
  clientVersion: '6.19.0'
}
error: script "reset-bdd-seed-dev" exited with code 1
error: script "reset-bdd" exited with code 1
