---

PrismaClientExceptionFilter

---

PrismaClientKnownRequestError:

Invalid `tx.workflowOnWorkflowTab.createMany()` invocation in

/Users/pierre-olivier/cronexia/cronexia-gta-back/app/src/workflow-tabs/workflow-tabs.service.ts:323:40



  320   await tx.workflowOnWorkflowTab.createMany({ data: joinRows });

  321 }

  322 if (poolRows.length > 0) {

→ 323   await tx.workflowOnWorkflowTab.createMany(

Unique constraint failed on the fields: (`workflowId`)

    at ei.handleRequestError (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:125:7268)

    at ei.handleAndLogRequestError (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:125:6593)

    at ei.request (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:125:6300)

    at async a (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:134:9551)

    at async <anonymous> (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/src/workflow-tabs/workflow-tabs.service.ts:323:9)

    at async Proxy._transactionWithCallback (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:134:8120) {

  code: 'P2002',

  meta: { modelName: 'WorkflowOnWorkflowTab', target: [ 'workflowId' ] },

  clientVersion: '6.19.0'

}

---

---

---

WorkflowOnWorkflowTab > (workflowId): la valeur renseignée est déjà utilisée et doit être unique.

═══════════════════════════════════════════════════════

🔴 MERCURIUS ERROR DEBUG

═══════════════════════════════════════════════════════

Error message: Conflict

Error path: [ 'replaceWorkflowTabsOrganization' ]

Error locations: [

  {

    "line": 3,

    "column": 5

  }

]

Error extensions: {}

───────────────────────────────────────────────────────

Original Error name: ConflictException

Original Error message: Conflict

Original Error: ConflictException: Conflict

    at catch (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/src/_utility/filters/exception/prisma-exception.filter.ts:268:15)

    at ExternalExceptionsHandler.invokeCustomFilters (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/@nestjs/core/exceptions/external-exceptions-handler.js:31:32)

    at ExternalExceptionsHandler.next (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/@nestjs/core/exceptions/external-exceptions-handler.js:14:29)

    at Object.replaceWorkflowTabsOrganization (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/@nestjs/core/helpers/external-proxy.js:14:42)

    at async Object.fastifyGraphQl [as graphql] (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/mercurius/index.js:650:23) {

  response: {

    statusCode: 409,

    message: 'Conflict',

    details: {

      description: 'La valeur renseignée est déjà utilisée et doit être unique.',

      prisma: [Object]

    },

    errorCronexia: null

  },

  status: 409,

  options: {}

}

───────────────────────────────────────────────────────

All execution errors:

  [0] Conflict

      at line 3, column 5

═══════════════════════════════════════════════════════

More details

---

ConflictException: Conflict

    at catch (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/src/_utility/filters/exception/prisma-exception.filter.ts:268:15)

    at ExternalExceptionsHandler.invokeCustomFilters (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/@nestjs/core/exceptions/external-exceptions-handler.js:31:32)

    at ExternalExceptionsHandler.next (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/@nestjs/core/exceptions/external-exceptions-handler.js:14:29)

    at Object.replaceWorkflowTabsOrganization (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/@nestjs/core/helpers/external-proxy.js:14:42)

    at async Object.fastifyGraphQl [as graphql] (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/mercurius/index.js:650:23) {

  path: [ 'replaceWorkflowTabsOrganization' ],

  locations: [ { line: 3, column: 5 } ],

  extensions: [Object: null prototype] {}

}

---

---
