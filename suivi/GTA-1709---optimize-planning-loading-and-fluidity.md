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
