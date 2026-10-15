# Audit front pour permettre l'audit RGAA

Pas de contournement des droits. Pas de variable `.env`. Les seeds dev sont hors sujet (on suppose qu'ils sont déjà chargés). Les pages `/admin` restent hors échantillon.

## Connexion

Sans `accessToken`, une page applicative redirige vers `/login`. `/login`, les routes API et les fichiers statiques ne passent pas par ce contrôle. Un audit de page Asqatasun sans session note donc l'écran de connexion.

Les droits viennent du profil sélectionné, chargé par `hydrate-auth.ts` depuis le back. `SUPER_ADMIN` ouvre toutes les pages mappées (`assert-page-access.ts`) et ignore les droits `PAGE_*` des liens de menu. Les liens `RTM_*` suivent le mode de gestion du temps de la ressource, y compris pour ce profil. Ce n'est pas un rôle qu'on force dans le navigateur.

## Compte à utiliser

`pierre-olivier.courtois`, matricule `987654B`, profil **HR_MANAGER** seulement. L'accueil est `HomeHrManager`.

Le POC ne change pas de profil pendant l'audit. Un audit de page ne peut pas cliquer le sélecteur de profil. Le profil EMPLOYEE du même compte réécrit population, ressource et dates vers `987654B` et aujourd'hui (`(with-filters)/+layout.server.ts`), donc avril 2024 et `All_Resources` seraient perdus.

HR_MANAGER ouvre les pages de gestion : planning, dossier, anomalies, pointages, populations, absences, compteurs, synthèse, rapports, et les demandes à valider (`/request-management`, équivalent valideur de `/demands`). Il n'a pas `PAGE_DEMANDS`, `PAGE_VACATION_RIGHTS` ni `PAGE_CALENDAR`.

Autres comptes :

- `maxime.chevasson` — EMPLOYEE + MANAGER, matricule `123456A`. C'est la ressource affichée dans les pages « une personne ».
- `murielle.colbert` — MANAGER + EMPLOYEE
- `super.admin` — SUPER_ADMIN, sans ressource. L'accueil est `HomeSuperAdmin`. Secours si une page de gestion répond 403.

## Filtres

Une URL suffit. `persistFiltersToCookies` enregistre population, ressource et dates. Les pages filtrées suivantes relisent ces cookies.

Le segment `resource` est un matricule, pas un login. `all` est accepté seulement sur les pages qui listent tout le monde. Pour Maxime Chevasson : `123456A`.

Population `All_Resources`, période `2024-04-01` → `2024-04-14`.

Exemple :

`http://localhost:4173/collective-schedule/population/All_Resources/resource/all/dateStart/2024-04-01/dateEnd/2024-04-14`

## Échantillon

Deux audits, pas un seul parcours.

1. **Sans identifiants** — `/login` seulement. C'est la seule page publique. Sans session, Accueil redirige vers cette page.
2. **Connecté** — `pierre-olivier.courtois` en HR_MANAGER. Authentification d'abord, puis Accueil (`HomeHrManager`) : `/` n'est pas accessible sans être connecté.

Contact, mentions légales, aide et déclaration d'accessibilité n'existent pas.

| Page | URL |
| --- | --- |
| Authentification | `/login` — audit 1, sans identifiants |
| Accueil | `/` — audit 2, après connexion. `HomeHrManager` |
| Demandes | `/request-management` — même famille d'écrans que `/demands`, côté valideur. Redirige vers `/request-management/<onglet>/population/All_Resources/resource/all/dateStart/2024-04-01/dateEnd/2024-04-14` |
| Planning collectif | `/collective-schedule/population/All_Resources/resource/all/dateStart/2024-04-01/dateEnd/2024-04-14` |
| Dossier | `/employee-file/population/All_Resources/resource/123456A/dateStart/2024-04-01/dateEnd/2024-04-14` |
| Anomalies | `/anomalies/population/All_Resources/resource/all/dateStart/2024-04-01/dateEnd/2024-04-14` |
| Pointages | `/clockings/population/All_Resources/resource/all/dateStart/2024-04-01/dateEnd/2024-04-14` |
| Populations | `/populations/population/All_Resources/resource/all/dateStart/2024-04-01/dateEnd/2024-04-14` |
| Absences / toutes | `/absences/all/population/All_Resources/resource/all/dateStart/2024-04-01/dateEnd/2024-04-14` |
| Compteurs | `/counters/period/population/All_Resources/resource/all/dateStart/2024-04-01/dateEnd/2024-04-14` |
| Synthèse | `/summary/population/All_Resources/resource/all/dateStart/2024-04-01/dateEnd/2024-04-14` |
| Document | `/reports` |

Le dossier refuse `resource/all`. Il lui faut `123456A`.

Ouvrir d'abord l'URL du planning collectif : les cookies de filtres servent ensuite à `/request-management`, anomalies, pointages, absences, synthèse, populations et compteurs.

## Hors de ce POC

Rester sur HR_MANAGER. Ne pas basculer sur EMPLOYEE.

- `/demands` — pas dans l'échantillon. Les demandes sont couvertes par `/request-management`.
- `/individual-schedule` — même écran que le planning collectif, pour une personne. Pas utile dans ce POC.
- `/vacation-rights` — ignoré. Petite page, pas prioritaire. Réservée au profil EMPLOYEE (`PAGE_VACATION_RIGHTS`).
- `/calendar` — **page importante, reportée**. Réservée au profil EMPLOYEE (`PAGE_CALENDAR`). L'équivalent valideur n'existe pas encore. On la saute pour garder un seul profil, `pierre-olivier.courtois` en HR_MANAGER, sur tout le parcours. À reprendre quand un calendrier valideur existera, ou lors de l'audit définitif.
- `/_dev/routes` — plan du site, réservé au dev. Beaucoup trop gros pour ce POC.
