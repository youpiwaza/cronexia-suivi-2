═══════════════════════════════════════════════════════
🔴 MERCURIUS ERROR DEBUG
═══════════════════════════════════════════════════════
Error message: Forbidden Exception
Error path: [ 'createEventByDay' ]
Error locations: [
  {
    "line": 3,
    "column": 5
  }
]
Error extensions: {}
───────────────────────────────────────────────────────
Original Error name: ForbiddenException
Original Error message: Forbidden Exception
Original Error: ForbiddenException: Forbidden Exception
    at EventByDaysResolver.createEventByDay (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/src/event-by-days/event-by-days.resolver.ts:1215:15)
    at /Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/@nestjs/core/helpers/external-context-creator.js:67:33 {
  response: {
    errorCronexia: {
      cronexiaCode: 'CRO_EROR_000000003',
      criticity: 'error',
      'fr-FR': [Object],
      messageTech: 'EventRangeOnResourcesResolver/EventByDaysResolver > createEvent(RangeOnResource|ByDay) > eventId not resolvable from event.connect'
    }
  },
  status: 403,
  options: {}
}
───────────────────────────────────────────────────────
All execution errors:
  [0] Forbidden Exception
      at line 3, column 5
═══════════════════════════════════════════════════════
More details
---
ForbiddenException: Forbidden Exception
    at EventByDaysResolver.createEventByDay (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/src/event-by-days/event-by-days.resolver.ts:1215:15)
    at /Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/@nestjs/core/helpers/external-context-creator.js:67:33 {
  path: [ 'createEventByDay' ],
  locations: [ { line: 3, column: 5 } ],
  extensions: [Object: null prototype] {}
}
---
---
---
{"level":30,"time":1790000296781,"pid":12257,"hostname":"MacBookPro.lan","reqId":"req-1e1","res":{"statusCode":403},"responseTime":18.513416999951005,"msg":"request completed"}
