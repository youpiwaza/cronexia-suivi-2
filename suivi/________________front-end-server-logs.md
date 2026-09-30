
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ Failed Tests 2 ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/routes/functions/cronexia/declaration-hours/declaration-hours-workflow-create.helpers.spec.ts > buildDeclarationHourlyRowsCreateInput — jours de repos > soumission : repos sans saisie autorisée → { date } seul
AssertionError: expected [ { date: '2026-09-11', …(1) }, …(1) ] to deeply equal [ { date: '2026-09-11' }, …(1) ]

- Expected
+ Received

  [
    {
      "date": "2026-09-11",
+     "eventByDays": {
+       "create": [
+         {
+           "date": "2026-09-11",
+           "duration": 480,
+           "event": {
+             "connect": {
+               "code": "ADEC",
+             },
+           },
+           "eventOrigin": "Input",
+           "isAnomaly": false,
+           "timeEnd": "17:00:00Z",
+           "timeStart": "09:00:00Z",
+         },
+       ],
+     },
    },
    {
      "date": "2026-09-12",
    },
  ]

 ❯ src/routes/functions/cronexia/declaration-hours/declaration-hours-workflow-create.helpers.spec.ts:40:18
     38|     });
     39|
     40|     expect(rows).toEqual([
       |                  ^
     41|       { date: '2026-09-11' },
     42|       { date: '2026-09-12' },

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/2]⎯

 FAIL  src/routes/functions/cronexia/declaration-hours/declaration-hours-workflow-create.helpers.spec.ts > buildDeclarationHourlyRowsCreateInput — jours de repos > brouillon semaine : repos sans saisie autorisée omis
AssertionError: expected [ { date: '2026-09-11', …(1) } ] to deeply equal []

- Expected
+ Received

- []
+ [
+   {
+     "date": "2026-09-11",
+     "eventByDays": {
+       "create": [
+         {
+           "date": "2026-09-11",
+           "duration": 480,
+           "event": {
+             "connect": {
+               "code": "ADEC",
+             },
+           },
+           "eventOrigin": "Input",
+           "isAnomaly": false,
+           "timeEnd": "17:00:00Z",
+           "timeStart": "09:00:00Z",
+         },
+       ],
+     },
+   },
+ ]

 ❯ src/routes/functions/cronexia/declaration-hours/declaration-hours-workflow-create.helpers.spec.ts:54:18
     52|     });
     53|
     54|     expect(rows).toEqual([]);
       |                  ^
     55|   });
     56|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/2]⎯


 Test Files  1 failed | 105 passed | 2 skipped (108)
      Tests  2 failed | 816 passed | 48 skipped (866)
   Start at  11:13:24
   Duration  6.75s (transform 32.74s, setup 0ms, import 65.15s, tests 1.71s, environment 930ms)

error: script "test" exited with code 1
