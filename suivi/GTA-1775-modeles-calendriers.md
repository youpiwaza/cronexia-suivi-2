# 📅🧰 Modèles de calendriers : récapitulatif du travail

Tickets :

- **GTA-1775** — 💾 BACK / 🧹 Cleaner les classes/CRUD relatives aux calendriers
- **GTA-1776** — 💾 BACK / 🎨🌐 GraphQL & API > Mise en place des bases
-**GTA-1783**  — 📅🧰 Modèles calendriers / 💾 BACK / 🦾 Fonctions & propriétés relatives aux jours chômés / non chômés

Doc fonctionnelle et technique du module : [`app/src/calendars/README.md`](../../app/src/calendars/README.md).

---

## 1. Le besoin

### Informations à gérer (Excel)

| Page                     | Champs                                                                                                                                                   |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Jours particuliers       | code, libellé court, libellé long, description de l'effet (texte libre), fonction associée, événement associé, période (matin, après-midi, journée ou heures de début et de fin) |
| Calendriers              | code, libellé court, libellé long, jours particuliers saisissables, population cible                                                                     |
| Paramétrage des calendriers | calendrier, date, jour particulier (parmi ceux associés au calendrier)                                                                                |

### Effets par type de jour

| Jour particulier           | Fonction à prévoir              | Effets                                                                                                                                             |
| -------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Jour férié chômé           | Désactivation sur jour / demi-jour | génération de l'événement associé sur toute la population ; désactivation de la valorisation des autres absences de la journée (sauf celles gérées en jours calendaires) ; désactivation des conflits de chevauchement |
| Jour férié non chômé       | Non                             | génération d'un événement neutre sur toute la population                                                                                            |
| RTT employeur              | Désactivation sur jour / demi-jour | idem jour férié chômé                                                                                                                            |
| Rentrée scolaire (si simple) | Désactivation sur plage horaire | génération de l'événement ; désactivation de la valorisation et des conflits sur la même plage horaire                                           |

**Hors scope** : l'application réelle des effets. Elle sera traitée dans un ticket séparé.

---

## 2. Analyse de l'existant

### Base de données

- `Calendar` : `code`, `labelShort` et `labelLong`, **tous les trois `@unique`**.
- `CalendarDay` : `date` **`@unique` sur toute la base**, `labelShort`, `labelLong`, et un `dayName` saisi à la main (valeur par défaut `Lundi`).
- Relation n-m **implicite** `Calendar` ⟷ `CalendarDay`.
- Trio d'enum dynamique (valeurs `String` uniquement) :
  - `CalendarDayEnum` : le champ (ex. `dayType`) ;
  - `CalendarDayEnumStrVal` : les valeurs possibles ;
  - `CalendarDayEnumVal` : l'affectation d'une valeur à un jour.

### Seeds (`app/prisma/seeds/calendars/calendar.seed.ts`)

- Calendriers : « Calendrier normal », « Calendrier Alsace Moselle ».
- Enum `dayType` avec deux valeurs : « Jour férié chômé », « Jour férié non chômé ».
- Jours : Veille de Noël, Noël, Lundi de Pentecôte, plus des jours de test.

### NestJS & GraphQL

- Les 5 modules CRUD existaient, **générés « à l'ancienne »** depuis le boilerplate.
- Aucun autre module ne les utilisait : ni ressources, ni populations, ni compteurs, ni événements.
- Le front ne les appelait pas non plus.


### Historique du nommage


## 4. Modèle de données final

```
                allowedSpecialDays (n-m)             populations (n-m, ≤ 10)
  SpecialDay ◄──────────────────────────── Calendar ──────────────────────────► Population
   (type)                                     │ 1
     │ 1                                      │
     │                                        │ n
     └───────────────── n ──────────────► CalendarDay ◄─── n ─── CalendarDayEnumVal
                                        date, label                  (champs libres)
                                        @@unique([calendarId, date])
```

| Modèle Prisma | Fichier | Rôle |
| ------------- | ------- | ---- |
| `SpecialDay` (nouveau) | `app/prisma/schema/special-day.prisma` | type de jour : code, libellés, description de l'effet, `functionCode`, événement, période (`typeDay` ou `timeStart` + `timeEnd`) |
| `Calendar` (refait) | `app/prisma/schema/calendar.prisma` | code (seul champ unique), libellés, jours particuliers autorisés, populations |
| `CalendarDay` (refait) | `app/prisma/schema/calendar-day.prisma` | un jour particulier positionné à une date, dans **un** calendrier (supprimé avec lui) |
| `CalendarDayEnum*` (conservés) | `calendar-day-enum*.prisma` | champs dynamiques des jours |
| `Event`, `Population` | relations inverses ajoutées | `specialDays`, `calendars` |

Changements notables sur `CalendarDay` :

- `date` n'est plus unique globalement, mais **par calendrier** ;
- `dayName` est supprimé : il se déduit de la date ;
- `labelShort` / `labelLong` sont remplacés par un seul `label` (ex. « Noël »). Le type du jour est porté par `SpecialDay`.

Contraintes d'intégrité :

- supprimer un calendrier supprime ses dates (`onDelete: Cascade`) ;
- un `SpecialDay` encore positionné à une date ne peut pas être supprimé (`onDelete: Restrict`) ;
- un `Event` associé à un `SpecialDay` ne peut pas être supprimé (`onDelete: Restrict`).

---

## 5. Catalogue des fonctions spéciales

Fichier : `app/src/special-days/functions/special-day-functions.catalog.ts`.

- Même principe que les fonctions de compteurs (`src/_utility/functions/function-definition.ts`) : codé en dur, pas en base.
- Indexé par l'enum Prisma `SpecialDayFunctionEnum` : ajouter une valeur à l'enum sans la décrire dans le catalogue **ne compile pas**.
- Exposé au front par la query `specialDayFunctions` (code, libellé, description, `isImplemented`).

| `functionCode` | Période exigée | Exemples |
| -------------- | -------------- | -------- |
| `none` | libre | jour férié non chômé (événement neutre) |
| `deactivateDayOrHalfDay` | `typeDay` (AM, PM, Day) | jour férié chômé, RTT employeur |
| `deactivateTimeSlot` | `timeStart` + `timeEnd` | rentrée scolaire |

Toutes les fonctions sont marquées `isImplemented: false` : le branchement des effets est hors scope.

---

## 6. Code NestJS

### Modules

| Module | Contenu |
| ------ | ------- |
| `app/src/special-days/` (nouveau) | CRUD `SpecialDay`, catalogue, règle de période + tests |
| `app/src/calendars/` (refait) | CRUD `Calendar`, règles du calendrier + tests, README |
| `app/src/calendar-days/` (refait) | CRUD `CalendarDay`, affectation en batch |
| `app/src/calendar-day-enum*/` (conservés) | exemples GraphQL mis à jour (`dayName` → `label`) |

### Structure d'un module refait

Sur le modèle de `ct-counters-groups`, le module le plus propre du dépôt :

```
<module>/
├── <module>.module.ts
├── <module>.resolver.ts      ← gardes + @Right, helpers privés toWhereUniqueInput / renameIdKey / toFindArgs
├── <module>.service.ts       ← Prisma, transactions, relations
├── dto/                      ← create, create-many, update, where, order-by, find args, find-unique, nested/
├── entities/  models/  enums/
├── functions/                ← règles métier pures + *.spec.ts
└── _tests_all_queries        ← requêtes GraphQL d'exemple
```

### Bonnes pratiques appliquées

- **Dépendances cycliques** : `import { type X }` plus `require()` dans la factory du `@Field` (comme `CtCountersGroupModel`). Les services lisent leurs relations via l'API fluent de Prisma (`findUnique(...).relation()`). Aucun module n'importe un autre, donc plus de `forwardRef`.
- **Écritures nestées** : seulement `connect` / `disconnect` / `set` sur des éléments existants, avec des clés au format Prisma (`idSpecialDay` ou `code`, `idPopulation` ou `name`, `idCalendar` ou `code`), transmises telles quelles à Prisma.
- **Règles vérifiées après écriture, dans la même transaction** : un `connect` / `set` nesté ne dit pas à lui seul ce que contiendra la relation. Relire l'état final couvre tous les cas, et l'exception annule la transaction.
- **Mise à jour partielle** d'un `SpecialDay` : la période est validée sur l'état final (valeurs envoyées combinées avec celles en base).
- **Heures** comparées sur leur seule partie horaire (UTC) : Prisma relit un `@db.Time` au 1970-01-01, le scalaire GraphQL le date du jour.

### API GraphQL

| Entité | Queries | Mutations |
| ------ | ------- | --------- |
| `SpecialDay` | `specialDay`, `specialDayFindFirst`, `specialDays`, `specialDayFunctions` | `createSpecialDay`, `createManySpecialDays`, `updateSpecialDay` (+ `disconnectEvent`), `deleteSpecialDay` |
| `Calendar` | `calendar`, `calendarFindFirst`, `calendars` | `createCalendar`, `createManyCalendars`, `updateCalendar`, `deleteCalendar` |
| `CalendarDay` | `calendarDay`, `calendarDayFindFirst`, `calendarDays` | `createCalendarDay`, `createManyCalendarDays` (batch, tout ou rien), `updateCalendarDay`, `deleteCalendarDay` |

Vue d'une année, pour le front :

```graphql
{
  calendar(code: "CALEND_NORM") {
    code
    allowedSpecialDays { code labelShort functionCode }
    populations { name }
    calendarDays(dateStart: "2026-01-01", dateEnd: "2026-12-31") {
      idCalendarDay
      date
      label
      specialDay { code labelShort }
      calendarDayEnumVals { fieldnameHelper }
    }
  }
}
```

---

## 7. Erreurs (`cronexia-error-dictionnary.ts`)

Nouvelle section « Modèles de calendrier / Jours particuliers », messages en français et en anglais :

| Code | Cas |
| ---- | --- |
| `CRO_CAL_000000001` | recherche par critère unique sans exactement un critère (`id` ou `code`) |
| `CRO_CAL_000000002` | plus de 10 populations ciblées par un calendrier |
| `CRO_CAL_000000003` | date portant un jour particulier non autorisé par son calendrier |
| `CRO_CAL_000000004` | une seule des deux heures renseignée |
| `CRO_CAL_000000005` | heure de début postérieure ou égale à l'heure de fin |
| `CRO_CAL_000000006` | portion de journée ET heures renseignées |
| `CRO_CAL_000000007` | fonction « jour / demi-jour » sans portion de journée |
| `CRO_CAL_000000008` | fonction « plage horaire » sans heures |

Deux cas restent gérés par la base : date en double dans un calendrier (Prisma `P2002`) et suppression d'un élément encore utilisé (Prisma `P2003`).

---

## 8. Droits

Tous les resolvers passent par `@UseGuards(GqlJwtAuthGuard, RightsGuard)`.

| Code | Opérations |
| ---- | ---------- |
| `API_CALENDAR_READ` | toutes les queries, dont `specialDayFunctions` |
| `API_CALENDAR_CREATE` | `create*`, `createMany*` |
| `API_CALENDAR_UPDATE` | `update*` |
| `API_CALENDAR_DELETE` | `delete*` |

- Ajoutés en fin de `user-right.seeds.ts` : les UUID du seed sont alloués à la suite, un ajout au milieu aurait décalé tous les suivants.
- Donnés au profil `ADMIN`. `SUPER_ADMIN` passe toujours.

---

## 9. Seed (`app/prisma/seeds/calendars/calendar.seed.ts`)

Même fonction `seedCalendar`, donc l'orchestrateur `post-common` n'a pas changé.

- **4 jours particuliers** : `JFC` (férié chômé, événement `JF`), `JFNC` (férié non chômé), `RTTE` (RTT employeur), `RENTREE` (rentrée scolaire, 08:00 → 10:00).
- **2 calendriers** :
  - `CALEND_NORM` : les 4 jours autorisés, population `Cadres_Global` ;
  - `CALEND_ALSM` : `JFC` et `JFNC` autorisés.
- **Jours fériés 2026** : les 11 fériés nationaux (lundi de Pentecôte en non chômé) ; Alsace-Moselle en plus : Vendredi saint et Saint-Étienne ; rentrée scolaire le 01/09 dans le calendrier normal.
- L'événement `JF` et la population `Cadres_Global` ne sont rattachés que s'ils existent : le seed reste jouable seul.

---

## 10. Documentation

- `app/src/calendars/README.md` : doc du module (besoin, modèle, fonctions, règles, droits, API, seed, tests).
- `_docs/04.3-graphql-relations.md` : l'exemple de relation n-m implicite utilise désormais `Calendar` ⟷ `SpecialDay`, l'ancien exemple n'existant plus.
- `_tests_all_queries` réécrits pour `calendars` et `calendar-days`, et créé pour `special-days`.

---

## 11. Vérifications

Faites dans une **copie** du projet (répertoire temporaire), sans les fichiers restant à supprimer (§ 12) :

| Vérification | Résultat |
| ------------ | -------- |
| `prisma validate` | ✅ schéma valide |
| `prisma generate` | ✅ |
| `tsc --noEmit` | ✅ aucune erreur dans les fichiers créés ou modifiés. Le projet a déjà environ 670 erreurs ailleurs ; seul écart avec `HEAD` : +3 erreurs de typage circulaire dans `pop-criterias.service.with-ts-jest.spec.ts`, qui en compte déjà 399 et dont le nombre varie avec les modèles Prisma |
| Jest | ✅ 2 suites, 13 tests (`assert-special-day-period.spec.ts`, `assert-calendar-consistency.spec.ts`) |
| ESLint | ✅ aucune erreur sur `calendars`, `calendar-days`, `special-days` |

**Non testé** : les écritures transactionnelles contre une vraie base, et l'API démarrée.

---


### Tester l'API

- Via le MCP `graphql` ou GraphiQL (`http://localhost:3000/graphql`), avec les requêtes des `_tests_all_queries`.
- Les resolvers sont protégés : il faut un JWT avec les droits `API_CALENDAR_*`, ou retirer temporairement les gardes en local (sans commiter ce retrait).

