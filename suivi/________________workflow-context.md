# WorkflowResource context

## Code structure

1. Employee (resource & profile "employee", grouped as UserProfileInstance (= UPI)) can create demands instances (= WorkflowResource @cronexia-gta-back/app/prisma/schema/workflow-resource.prisma  = WR) with several levels of validations (= WorkflowResourceLevelState = WRLS @cronexia-gta-back/app/prisma/schema/workflow-resource-level-state.prisma ) , based on dynamic templating from @cronexia-gta-back/app/prisma/schema/workflow.prisma @cronexia-gta-back/app/prisma/schema/workflow-level.prisma

2. Those WRLS can be either validated or refused by Users with specific higher Profiles, typically "Manager" or "RhManager" (= "Gestionnaire RH" in french labels), also called "Validators"

3. A demand is considered validated is all levels have been validated, and refused if a single level is refused

4. Demands can have several levels : in order for a level to pass as "pending" validation, all lower levels must be already validated

5. Higher Profiles can overstep validation or refuses

## Code locations

- employee WR gathering :@resources.resolver.ts (2862-2902)
- employee demand creation : @workflow-resources.resolver.ts (427-440)

- validators WR gathering:
- validators WR status change:@user-profile-instances.resolver.ts (740-809) @user-profile-instances.resolver.ts (1364-1413)

## Comon testing employees and validators

- employee: Patrick
- validator level 1, profile "Manager" : Murielle
- validator level 2, profile "HrManager" : Pierre-Olivier

---

## Tab navigation (post GTA-1631)

- Source of truth: backend `WorkflowTab` + `WorkflowOnWorkflowTab`, query `workflowTabsForNavigation` (`affected: true` for `/demands` and `/request-management`).
- URL segment = catalog **`name`** (derived from `code`, e.g. `schedule-change` → `scheduleChange`). Kebab / old FR aliases redirect via `legacyEmployeeTabSegmentToName`.
- Synthetic tabs (not DB rows), always first: collab `summary`, validator `my-requests`. Keep `declaration-view`.
- Nav lists **affected** tabs only. Unassigned pool (`workflowTabId` null): `WORKFLOW_SCHEDULE_OVERLOAD_TT` (STO) — no UI. Clockings / CMAR / ENFM / hours-declaration stay `affected: false` until organize (out of scope).
- Columns = union of display families on the tab’s workflows. Create list = workflows on the tab ∩ `isActive` ∩ rights ∩ existing modal.

---
