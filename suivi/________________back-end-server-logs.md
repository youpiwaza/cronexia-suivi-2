

/home/youpiwaza/code/cronexia-gta-back/app/node_modules/ts-node/src/index.ts:859
    return new TSError(diagnosticText, diagnosticCodes, diagnostics);
           ^
TSError: ⨯ Unable to compile TypeScript:
prisma/seed-demo-arte.ts:59:7 - error TS2322: Type 'DemoSchedulesSeedResult' is not assignable to type 'DevSchedulesSeedResult | DemoSchedulesSeedResult'.
  Type 'DemoSchedulesSeedResult' is missing the following properties from type 'DemoSchedulesSeedResult': scheduleHvar8hP, scheduleHvar7hP, scheduleHvar8hT, scheduleHvar7hT

59       schedules: demo.demoSchedules,
         ~~~~~~~~~

  prisma/seeds-new/100-post-comon/interface/post-common-seeds-deps.interface.ts:13:3
    13   schedules: DevSchedulesSeedResult;
         ~~~~~~~~~
    The expected type comes from property 'schedules' which is declared here on type 'PostCommonSeedsDeps'
prisma/seed-demo-arte.ts:60:7 - error TS2322: Type 'DemoCyclesSeedResult' is not assignable to type 'DevCyclesSeedResult | DemoCyclesSeedResult'.
  Type 'DemoCyclesSeedResult' is missing the following properties from type 'DemoCyclesSeedResult': cycleCvar39hP, cycleCvar40hP, cycleCvar39hT, cycleCvar40hT

60       cycles: demo.demoCycles,
         ~~~~~~

  prisma/seeds-new/100-post-comon/interface/post-common-seeds-deps.interface.ts:14:3
    14   cycles: DevCyclesSeedResult;
         ~~~~~~
    The expected type comes from property 'cycles' which is declared here on type 'PostCommonSeedsDeps'

    at createTSError (/home/youpiwaza/code/cronexia-gta-back/app/node_modules/ts-node/src/index.ts:859:12)
    at reportTSError (/home/youpiwaza/code/cronexia-gta-back/app/node_modules/ts-node/src/index.ts:863:19)
    at getOutput (/home/youpiwaza/code/cronexia-gta-back/app/node_modules/ts-node/src/index.ts:1077:36)
    at Object.compile (/home/youpiwaza/code/cronexia-gta-back/app/node_modules/ts-node/src/index.ts:1433:41)
    at Module.m._compile (/home/youpiwaza/code/cronexia-gta-back/app/node_modules/ts-node/src/index.ts:1617:30)
    at node:internal/modules/cjs/loader:2096:10
    at Object.require.extensions.<computed> [as .ts] (/home/youpiwaza/code/cronexia-gta-back/app/node_modules/ts-node/src/index.ts:1621:12)
    at Module.load (node:internal/modules/cjs/loader:1678:32)
    at Module._load (node:internal/modules/cjs/loader:1470:12)
    at wrapModuleLoad (node:internal/modules/cjs/loader:261:19) {
  diagnosticCodes: [ 2322, 2322 ]
}
error: script "reset-bdd-seed-demo-arte" exited with code 1
