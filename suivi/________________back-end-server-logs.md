[Nest] 24366  - 09/01/2026, 3:09:23 PM   ERROR [createWorkflowResourceAndAssociateUploads] createWorkflowResource: association PJ échouée, rollback WR (resourceId 00000000-05a7-0000-0000-000000000097)
BadRequestException: Bad Request Exception
    at associateUploadsToWorkflowResource (/home/youpiwaza/code/cronexia-gta-back/app/src/workflow-resources/functions/associate-uploads-to-workflow-resource.ts:68:15)
    at async <anonymous> (/home/youpiwaza/code/cronexia-gta-back/app/src/workflow-resources/functions/create-workflow-resource-and-associate-uploads.ts:48:9)
    at async Proxy._transactionWithCallback (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:134:8120)
    at async WorkflowResourcesResolver.createWorkflowResource (/home/youpiwaza/code/cronexia-gta-back/app/src/workflow-resources/workflow-resources.resolver.ts:748:21)
═══════════════════════════════════════════════════════
🔴 MERCURIUS ERROR DEBUG
═══════════════════════════════════════════════════════
Error message: Bad Request Exception
Error path: [ 'createWorkflowResource' ]
Error locations: [
  {
    "line": 3,
    "column": 5
  }
]
Error extensions: {}
───────────────────────────────────────────────────────
Original Error name: BadRequestException
Original Error message: Bad Request Exception
Original Error: BadRequestException: Bad Request Exception
    at associateUploadsToWorkflowResource (/home/youpiwaza/code/cronexia-gta-back/app/src/workflow-resources/functions/associate-uploads-to-workflow-resource.ts:68:15)
    at async <anonymous> (/home/youpiwaza/code/cronexia-gta-back/app/src/workflow-resources/functions/create-workflow-resource-and-associate-uploads.ts:48:9)
    at async Proxy._transactionWithCallback (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:134:8120)
    at async WorkflowResourcesResolver.createWorkflowResource (/home/youpiwaza/code/cronexia-gta-back/app/src/workflow-resources/workflow-resources.resolver.ts:748:21) {
  response: {
    errorCronexia: {
      cronexiaCode: 'CRO_WR_000000027',
      criticity: 'error',
      'fr-FR': [Object],
      'en-US': [Object],
      messageTech: 'WorkflowResources > associateUploadsToWorkflowResource > upload type is not DOCUMENT (idUpload 3a7401b7-eea7-4d6b-b99c-7a5a38df137c)'
    }
  },
  status: 400,
  options: {}
}
───────────────────────────────────────────────────────
All execution errors:
  [0] Bad Request Exception
      at line 3, column 5
═══════════════════════════════════════════════════════
More details
---
BadRequestException: Bad Request Exception
    at associateUploadsToWorkflowResource (/home/youpiwaza/code/cronexia-gta-back/app/src/workflow-resources/functions/associate-uploads-to-workflow-resource.ts:68:15)
    at async <anonymous> (/home/youpiwaza/code/cronexia-gta-back/app/src/workflow-resources/functions/create-workflow-resource-and-associate-uploads.ts:48:9)
    at async Proxy._transactionWithCallback (/home/youpiwaza/code/cronexia-gta-back/app/prisma/generated/client/runtime/library.js:134:8120)
    at async WorkflowResourcesResolver.createWorkflowResource (/home/youpiwaza/code/cronexia-gta-back/app/src/workflow-resources/workflow-resources.resolver.ts:748:21) {
  path: [ 'createWorkflowResource' ],
  locations: [ { line: 3, column: 5 } ],
  extensions: [Object: null prototype] {}
}
