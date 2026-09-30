═══════════════════════════════════════════════════════

Error message: Graphql validation error

Error path: undefined

Error locations: undefined

Error extensions: {}

───────────────────────────────────────────────────────

Original Error name: FastifyError

Original Error message: Graphql validation error

Original Error: FastifyError [Error]: Graphql validation error

    at Object.fastifyGraphQl [as graphql] (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/mercurius/index.js:611:21)

    at _Reply.graphql (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/mercurius/index.js:302:16)

    at executeQuery (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/mercurius/lib/routes.js:240:18)

    at executeRegularQuery (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/mercurius/lib/routes.js:253:12)

    at Object.<anonymous> (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/mercurius/lib/routes.js:415:14)

    at process.processTicksAndRejections (node:internal/process/task_queues:95:5) {

  code: 'MER_ERR_GQL_VALIDATION',

  statusCode: 400,

  errors: [

    GraphQLError: Field "historisedEnumValueId" of required type "String!" was not provided.

        at coerceInputValueImpl (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/graphql/utilities/coerceInputValue.js:108:13)

        at /Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/graphql/utilities/coerceInputValue.js:75:16

        at Function.from (<anonymous>)

        at coerceInputValueImpl (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/graphql/utilities/coerceInputValue.js:73:20)

        at coerceInputValueImpl (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/graphql/utilities/coerceInputValue.js:117:34)

        at coerceInputValueImpl (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/graphql/utilities/coerceInputValue.js:117:34)

        at coerceInputValueImpl (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/graphql/utilities/coerceInputValue.js:49:14)

        at coerceInputValue (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/graphql/utilities/coerceInputValue.js:32:10)

        at coerceVariableValues (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/graphql/execution/values.js:132:69)

        at getVariableValues (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/graphql/execution/values.js:45:21)

        at buildExecutionContext (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/graphql/execution/execute.js:280:63)

        at Object.fastifyGraphQl [as graphql] (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/mercurius/index.js:602:32)

        at _Reply.graphql (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/mercurius/index.js:302:16)

        at executeQuery (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/mercurius/lib/routes.js:240:18)

        at executeRegularQuery (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/mercurius/lib/routes.js:253:12)

        at Object.<anonymous> (/Users/pierre-olivier/cronexia/cronexia-gta-back/app/node_modules/mercurius/lib/routes.js:415:14) {

      message: 'Variable "$data" got invalid value { effectDate: "2026-01-01", description: "city \\"undefined\\" le 2026-01-01", fieldnameHelper: "city", matriculeHelper: "300009F", resourceEnum: { connect: [Object] }, resourceField: { connect: [Object] }, resourceEnumStrVal: { connect: {} } } at "data.resourceEnumVals.create[0]"; Field "historisedEnumValueId" of required type "String!" was not provided.',

      path: undefined,

      locations: [Array],

      extensions: [Object: null prototype] {}

    }
