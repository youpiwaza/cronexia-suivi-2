# GTA-1709 / ⚡️ Plannings > improve loading performance and perceived fluidity

A month of collective planning can take up to about one second. The period filter already reloads only the visible window. GraphQL `skip` / `take` (as on clockings) does not fit this screen. The gains are: stop waiting on independent work, paint the grid before the slow counters, and make week-to-week / month-to-month navigation feel instant.

---

## Findings

### Pagination

Clockings paginates **rows inside a period that stays large** (`skip` / `take`, about one page of rows at a time). Planning is a matrix of resources × days for `dateStart`–`dateEnd`. Changing week or month already changes that window and calls `resourcesPlanningDatas` again. There is no extra time axis to slice.

Slicing a month into several week requests would make the month view slower. Keep one request per visible period.

`skip` / `take` on **resources** is still a real option when the population is large (load people in batches, or virtualize rows). For a normal team it adds a pager without making the month faster.

### Backend — `getResourcesPlanningDatas`

The favorite already skips blocks the user did not ask for (clockings, schedules, events, anomalies, counters, resource fields). What remains is a chain of waits.

After the favorite and the resource `where` are known, these blocks do not depend on each other and still run one after another:

- resources
- clockings
- schedules (cycle unroll)
- events
- resource fields and their values
- organization levels
- anomalies
- counters

Wall time is the sum. In parallel it becomes the slowest of schedules, events, and counters.

Two smaller items on the same path:

- When the favorite lists specific events, `JSON.stringify(eventsSpecifics)` is logged on every request, outside the `displayLogs` guard.
- Schedule overload rows and overload types are two sequential queries that can run together.

Counters are computed per counter for the whole population and period, after everything else. They are the right piece to stop blocking the grid: return resources, schedules, and events first, and fill counter columns in a second response (placeholder until then). Worth confirming with timings that counters are a large share of the second before splitting the API. Parallelizing the other fetches is worth doing either way.

### Frontend waterfall

Every period change waits on this, in order:

1. `(with-filters)` layout resolves filters and calls `loadResources` for the new period. The page `await parent()` cannot start until that returns.
2. The page then loads, in parallel: planning favorites, the full event catalogue, the full schedule catalogue, and workflow resources.
3. Only then does `loadCollectivePlanningPage` call `resourcesPlanningDatas`. It also fetches workflow resources again, plus the theme config.
4. The page return spreads that second workflow payload, then overwrites it with the first fetch. The duplicate workflow call is discarded.

Favorites, the event catalogue, and the schedule list do not depend on the week. They are needed when a cell popup opens. Every week change currently refetches them and holds the grid behind them.

### After the JSON arrives

`+page.svelte` `JSON.stringify`s the whole planning response in an effect, to avoid notifying the same load error twice. Then `mapPlanningResponse` builds the grid synchronously before anything paints. On a fat month that hitch shows up even when the network was fine. A cheap fingerprint (period + favorite + success/message) is enough for the notification guard.

### Perceived speed (not a smaller query)

- After the current period is on screen, prefetch the previous and next period (same population, resource, and favorite). A week-to-week click then reads from cache. Going back to the period just left should be instant.
- Keep the current grid visible with a thin pending state while the next period loads. The user should not stare at a blank page for the whole second.

---

## Improvements

Each item is meant to become its own plan.

### ✅ 1. Parallelize independent fetches in `getResourcesPlanningDatas` **- ✅ done**

Launch clockings, schedules, events, resource fields, organization levels, anomalies, and counters together once the favorite and the resource `where` are resolved. Merge only after all of them settle.

In the same change: drop the unguarded `JSON.stringify(eventsSpecifics)` log, and run the two schedule-overload queries in parallel inside the schedule unroll.

- @cronexia-gta-back\app\src\resources\functions\planning\get-resources-planning-datas.ts
- @cronexia-gta-back\app\src\resources\resources.resolver.ts (`resourcesPlanningDatas`)
- @cronexia-gta-back\app\src\resources\functions\schedules\resources-schedule-instances-core-by-period.ts

### ✅ 2. Return counters after the grid (async, with a placeholder) **- ✅ done**

Do not block `resourcesPlanningDatas` on `counterResultsAndAnoGroupedByXXX`. Paint resources, schedules, and events first. Fill counter columns in a second response; show a placeholder until it arrives.

Confirm with a trace that counters are a large share of the month load before splitting the contract.

- @cronexia-gta-back\app\src\resources\functions\planning\get-resources-planning-datas.ts
- @cronexia-gta-back\app\src\ct-counters\ct-counters.service.ts (`counterResultsAndAnoGroupedByXXXWithRawInput`)
- @cronexia-gta-front-v2\app\src\lib\graphql\planning\queries\resourcesPlanningDatas.ts
- @cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\collective\planning-data.mapper.ts
- @cronexia-gta-front-v2\app\src\routes\components\cronexia\collective-schedule\CollectiveSchedulePage.svelte

### ✅ 3. Paginate or virtualize resources when the population is large **- ✅ done**

`skip` / `take` on resources (same idea as clockings rows): load people in batches instead of the whole population, plus scroll. Only worth it for large populations. A normal team should stay one request.

Virtualizing rows (DOM only for what is on screen) is the alternative if the request itself is acceptable and the grid is what janks.

- @cronexia-gta-back\app\src\resources\functions\planning\get-resources-planning-datas.ts
- @cronexia-gta-front-v2\app\src\routes\(app)\(with-filters)\clockings\population\[[population]]\resource\[[resource]]\dateStart\[[dateStart]]\dateEnd\[[dateEnd]]\page\[[page]]\+page.server.ts (reference for `skip` / `take`)
- @cronexia-gta-front-v2\app\src\routes\components\cronexia\collective-schedule\CollectiveSchedulePage.svelte

### ✅ 4. Prefetch the previous and next period once the page is loaded **- ✅ done**

After the current grid is shown, load the adjacent period in the background (same population, resource, favorite). Week-to-week and month-to-month clicks, and going back, read from that cache.

- @cronexia-gta-front-v2\app\src\routes\components\common\filters\FilterPeriod.svelte
- @cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\load-collective-planning-page.server.ts
- @cronexia-gta-front-v2\app\src\routes\(app)\(with-filters)\collective-schedule\population\[population]\resource\[resource]\dateStart\[dateStart]\dateEnd\[dateEnd]\+page.svelte

### ✅ 5. Start the planning query without waiting on the catalogues, and fetch workflow once **- ✅ done**

`resourcesPlanningDatas` currently starts only after favorites, the event catalogue, the schedule catalogue, and the first workflow fetch have finished. Start it in the same `Promise.all`.

`fetchPlanningWorkflowResources` runs in both the page load and `loadCollectivePlanningPage`. The page return keeps the first result and drops the second. Call it once.

- @cronexia-gta-front-v2\app\src\routes\(app)\(with-filters)\collective-schedule\population\[population]\resource\[resource]\dateStart\[dateStart]\dateEnd\[dateEnd]\+page.server.ts
- @cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\load-collective-planning-page.server.ts
- @cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\fetch-planning-workflow-resources.ts
- @cronexia-gta-front-v2\app\src\routes\(app)\(with-filters)\+layout.server.ts (`await parent()` → `loadResources` still runs before the page load; leave that dependency alone unless it shows up in a trace)

### ✅ 6. Stop refetching catalogues on every period change **- ✅ done**

Favorites, events grouped by type, and the full schedule list do not change with the week. They are popup dependencies. Cache them (or load them from a parent that does not depend on `dateStart` / `dateEnd`) and refetch only when the favorite or the catalogues themselves change. Lazy-load the popup catalogues on first modal open if that is simpler.

- @cronexia-gta-front-v2\app\src\routes\(app)\(with-filters)\collective-schedule\population\[population]\resource\[resource]\dateStart\[dateStart]\dateEnd\[dateEnd]\+page.server.ts
- @cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\favorites\load-planning-favorites.server.ts
- @cronexia-gta-front-v2\app\src\routes\(app)\(with-filters)\+layout.server.ts

### ✅ 7. Replace the full-payload `JSON.stringify` guard **- ✅ done**

The effect stringifies the entire planning response to skip a duplicate error toast. Compare a small fingerprint (period, favorite id, success, message) instead. `mapPlanningResponse` still has to run before paint; this item is only the notification diff.

- @cronexia-gta-front-v2\app\src\routes\(app)\(with-filters)\collective-schedule\population\[population]\resource\[resource]\dateStart\[dateStart]\dateEnd\[dateEnd]\+page.svelte
- @cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\collective\planning-data.mapper.ts

---
---
---

## Retours et ajustements

Favorites (1–2) are regressions. Scroll batching (4) is not: the load-time gain stays; the follow-up only removes the freeze while scrolling. Treat each item as its own pass.

---

### 1. Favoris > regroupement par modalité de gestion & le reste par défaut > des compteurs sont affichés

Regroupement does not turn counters on. A saved favorite with empty counter columns does not persist counters (`emptyFavoriteFormState` → `counters: {}` in `@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\favorites\favorite-form.ts`).

Every user already has a non-custom default favorite. `@cronexia-gta-back\app\prisma\seeds-new\02-recommended\planning-favorites\planning-favorites.recommended.seed.ts` seeds three shared favorites (no `userId`): collective, individual, team. UUID prefix `00000000-9f00-0000-0000-`, allocator from `…0001`. Matches the frontend constants:

- collectif `COLLECTIVE_PLANNING_FAVORITE_ID` = `…0001`
- individuel `…0002`
- équipe `…0003`

The collective seed (`@cronexia-gta-back\app\prisma\seeds-new\02-recommended\planning-favorites\planning-collective-default.recommended.seed.ts`) is: all schedules, daily absences, other events, theoretical clockings, shortcuts CP / RTT / MAL. No counter columns. PTO was removed from collective and individual defaults on 28/05/2026 (GTA-1265).

The **old** display is still hardcoded when the client has no resolved favorite (`selectedFavorite === null`):

- `applyPlanningFavorite(null)` → `activeLines: []` (`@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\favorites\apply-planning-favorite.ts`)
- empty `activeLines` = **every** line, including counters (`visibleScheduleLines` in `@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\collective\collective-schedule.data.ts`)
- `planningShowsCounters(null)` reserves `PTO` / `PVA` (`@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\collective\planning-data.mapper.ts` + `@cronexia-gta-front-v2\app\src\config\counters-required-config.ts`)
- backend path 1 does the same when no favorite id is sent (`@cronexia-gta-back\app\src\resources\functions\planning\functions\build-planning-counter-input.ts`)

That null path is wider than the current collective seed (hourly absences, real clockings, anomalies, and counters the seed does not have).

The usual way `selectedFavorite` becomes null while the grid still used a favorite id: cookie / `planning.favoriteId` not found in `favorites.all` (same failure as item 2). The server query can still send the id, so regroupement **fields** come back, while the client paints default counters.

#### 1.1 Check the planning favorite data flow

Trace one collective load before changing display code:

1. Seed id `…0001` is the fallback in the collective `+page.server.ts` when `resolvePlanningFavoriteId` has no URL segment and no cookie (`@cronexia-gta-front-v2\app\src\_utility\planning\resolve-planning-favorite-id.server.ts`).
2. That id is sent to `resourcesPlanningDatas`. With a favorite id and no counter columns, the backend must **not** take the PTO/PVA path.
3. Cronexia list (non-custom) + user favorites are loaded, then `selectedFavorite = favorites.all.find(...)`. That lookup runs **before** `isInternalPlanningFavorite` hides “Favori par défaut” from the selector (`@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\favorites\is-internal-planning-favorite.ts`). Hiding it from the menu must not drop it from `selectedFavorite`.
4. `applyPlanningFavorite(selectedFavorite)` and `planningShowsCounters(selectedFavorite)` decide lines and the async counters request.

Note where the chain breaks: cookie id missing from `favorites.all` (item 2), lookup after the visible filter, or `selectedFavorite` null while the query still used `…0001`. In that last case the grid paints the old hardcode on top of seed data.

**1.1 confirmation (code):** lookup-before-filter is already correct. Collective / individual / team all do `favorites.all.find(...)` then return `visiblePlanningFavorites(favorites.all)` — hiding the seed from the menu does not drop it from `selectedFavorite`. The null paint is the cache miss (item 2): the query still used a real id, that id is absent from `favorites.all`, `selectedFavorite` is null, and the grid paints PTO/PVA + every line on top of seed data. The grid is not reading `COUNTERS_REQUIRED_CONFIG` while a real favorite is selected.

#### 1.2 Align the hardcoded planning default with the current seed

When the client has no resolved favorite, stop painting every line and PTO/PVA. Use the collective seed shape: all schedules, daily absences, other events, theoretical clockings; no hourly absences, no real clockings, no anomalies, no counters.

Keep `COUNTERS_REQUIRED_CONFIG` for summary, the counters page, and the planning guard unless 1.1 shows the **grid** is reading it while a real favorite (seed or custom) is selected. Those other screens are a different default. A custom favorite that actually has counter columns still shows them.

- `@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\favorites\apply-planning-favorite.ts`
- `@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\collective\planning-data.mapper.ts`
- `@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\collective\collective-schedule.data.ts`

---

### 2. Favoris créés à la volée > ne sont pas affichés

`invalidateAll` after create already runs (`@cronexia-gta-front-v2\app\src\_utility\planning\select-planning-favorite.ts`). The list stays stale because the process cache is cleared under the **wrong key**.

- Page loads key the cache as `` `${login}::${profileId}` `` via `planningCatalogueUserKeyFromAuth` (`@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\favorites\planning-catalogue-cache.server.ts`).
- Create / update / delete call `clearPlanningFavoritesCache` with the same helper, but `/api/*` skips auth hydration (`@cronexia-gta-front-v2\app\src\_utility\navigation\navigation-cronexia.ts`). `extractDatasFromEvent` leaves `currentUser: null` and only sets `selectedUserProfileInstanceId`.
- Clear therefore hits `::${profileId}` and leaves `${login}::${profileId}` untouched. The next `invalidateAll` is a cache hit.

Event and schedule catalogues already wipe **every** map entry (`clearEventsCatalogueCache` / `clearScheduleCatalogueCache`). Favorites do not.

Same cache is used by collective, individual, and team schedule loads. Calendar, absences, anomalies, and summary do not load this list.

**Fix:** `clearPlanningFavoritesCache` clears `favorites` / `favoritesInflight` on every map entry (same pattern as events). Callers stay as-is. Guard the inflight write: if a clear happens while `loadPlanningFavorites` is in flight, do not store the stale result back into the slot.

- `@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\favorites\planning-catalogue-cache.server.ts`
- `@cronexia-gta-front-v2\app\src\routes\api\planning\planning-favorite\create\+server.ts` (same for update / delete)

---

### 3. Infos de regroupement mal affichées (modalité de gestion)

Seeds store `resourceTimeManagementMethod` (label “Modalité de gestion”) as an `EnumString` on `resourceEnumVals`.

Two different fields on each planning resource:

- `resourceTimeManagementMethod`: resolved in `@cronexia-gta-back\app\src\resources\functions\planning\get-resources-planning-datas.ts` from enum vals effective at `dateStart`. Used only for `hideHours` / `hasRealClockings`.
- `regroupementsValues`: filled by `getResourceFieldsValues` + `mergeResourceFieldsValues` for the favorite’s resource fields. The chip and group headers read **only** this, via `groupValues` in the mapper (~566–572) and `resource.groupValues[metaField.key] ?? '—'` in `CollectiveScheduleGrid.svelte`.

`pickValue` does read `enumString`. An empty chip means `regroupementsValues` did not yield that field name, not that the seed is empty. The mapper also keeps the latest non-empty value of any date, while the top-level field keeps the value effective at period start — so the two can disagree even when both are present.

**Payload check (code + GraphQL selection; live `resourcesPlanningDatas` unreachable):** when the favorite connects “Modalité de gestion”, `regroupements[].name` is `resourceTimeManagementMethod` (label from the ResourceField). `getResourceFieldsValues` + `mergeResourceFieldsValues` put that field on `regroupementsValues.dates[]` as `EnumString` (`value.enumString`), GraphQLDate `YYYY-MM-DD`, **without** dropping dates after `dateStart`. Top-level `resourceTimeManagementMethod` is the latest `resourceEnumVals.effectDate` ≤ `dateStart` (identity query). The chip reads only `groupValues`. Last-write in the mapper therefore showed a future historisation when dates had one, and `—` when that field name never landed in `dates`. Merge already maps `enumString`; no backend change. Mapper now keeps the latest date ≤ `dateStart` for every regroupement field, and copies the identity modality only when `resourceTimeManagementMethod` is still missing.

Keep other regroupement fields on `regroupementsValues` only. Align the chosen value with the period start (latest `effectDate` ≤ `dateStart`), so a future historised value does not replace the current one.

- `@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\collective\planning-data.mapper.ts`
- `@cronexia-gta-front-v2\app\src\routes\components\cronexia\collective-schedule\CollectiveScheduleGrid.svelte`
- `@cronexia-gta-back\app\src\resources\functions\planning\get-resources-planning-datas.ts`
- `@cronexia-gta-back\app\src\resources\functions\planning\merge\merge-resource-fields-values.ts`

---

### 4. Saccades au scroll (upgrade, not a regression)

Resource batches are the load-time win from item 3 above. Do **not** go back to loading the whole population in one request.

What is left is a freeze while scrolling: the next people are fetched only when the sentinel is reached, so the list stops, shows “Chargement…”, then jumps taller. Hide that wait; keep the batching.

Single constant: `PLANNING_RESOURCE_BATCH_SIZE = 10` in `@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\collective\planning-resource-batch.ts`. Initial load, adjacent-period prefetch, and the next-matricule slice all use it. Backend `take` has no hardcoded 10. Next pages are an explicit `matricules` list, not `skip`. A batch of **15** covers a tall screen so the first paint already fills the viewport.

Only collective schedule on a population batches. Scroll uses an `IntersectionObserver` sentinel (`rootMargin: 160px`) in `CollectiveScheduleGrid.svelte`. Appended rows live in `CollectiveSchedulePage` state and are **not** written into the period cache.

Adjacent-period prefetch (`@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\prefetch-adjacent-planning-periods.ts`) stores only the first `take` page. It cannot feed scroll. The same idea — warm the next slice once the current one is on screen — applies to the next resource batch.

**Fix (shipped):** batching stays; the wait is hidden behind a one-batch buffer.

- `PLANNING_RESOURCE_BATCH_SIZE = 15`: the first response fills a tall screen.
- `PLANNING_RESOURCE_SENTINEL_MARGIN_PX = 600`: the sentinel fires about one screen before the bottom, instead of 160px.
- The next slice is fetched into `bufferedBatch` and is **not** painted. When the sentinel is reached, the buffer is appended with no network, then the next slice is fetched behind it. The buffer is refilled only by user scroll, so the whole population is never loaded.
- The buffer is first filled 200ms after the first paint of each server load. The delay drops the wasted request when a period change repaints twice (cached neighbour, then confirmed load).
- One batch request at a time (`batchInflight`); a second caller awaits the same promise. `Chargement…` shows only when the buffer was empty on arrival (`batchAwaited`). `batchLoading` and `loadNextResourceBatch` are gone.
- Counters for a slice still go on the second request, started as soon as the slice is buffered. `resourcesWithCounterOverlay` only paints overlay rows that are already on screen, so a buffered slice never leaks into the grid.
- A new server load (period, favorite, population, save) clears appended rows, buffer and in-flight request. Scrolled rows stay out of the period cache.
- Pure helpers `nextResourceBatchMatricules` / `resourcesWithCounterOverlay` are covered by `planning-resource-batch.spec.ts`.

- `@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\collective\planning-resource-batch.ts`
- `@cronexia-gta-front-v2\app\src\routes\functions\cronexia\planning\collective\planning-resource-batch.spec.ts`
- `@cronexia-gta-front-v2\app\src\routes\components\cronexia\collective-schedule\CollectiveSchedulePage.svelte`
- `@cronexia-gta-front-v2\app\src\routes\components\cronexia\collective-schedule\CollectiveScheduleGrid.svelte`
