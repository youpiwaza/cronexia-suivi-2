# 💾 Back / 🌊 ✅ Workflows / 🔧 Onglets / 🌱 Seeds

## 👨‍💻 Dev

Rétablir les onglets existants, mais de manière dynamique (remplacer le hardcode)

🙇 **Attention**, on ne rentre que les codes, les names seront calculés à partir des codes. La fonction doit être commune aux seeds et à NestJs (cf. nouvelles seeds > workflows pour similarités de fonctionnement ; **ON RESTE DRY**).

---

## 🔨 Chop²

### Seeds — restaurer les onglets hardcodés actuels

Référence front actuelle : `cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/employee-demands-tabs.ts`

Noms de workflows : `cronexia-gta-back/app/prisma/seeds-new/02-recommended/workflow/workflow.seed.ts`

| position | name | code | label | affected | Workflows |
| --- | --- | --- | --- | --- | --- |
| 1 | `scheduleChange` | `schedule-change` | Horaires | true | `WORKFLOW_SCHEDULE_OVERLOAD` |
| 2 | `remoteWorkByEvent` | `remote-work-by-event` | Télétravail | true | `WORKFLOW_EVENT_TT` |
| 3 | `absences` | `absences` | Absences | true | `WORKFLOW_EVENT_CP`, `WORKFLOW_EVENT_RTT`, plus le dump actuel : `MARIAGE_ATTACHMENT_REQUIRED`, `SICK_CHILD_ATTACHMENT_REQUIRED_DEFERRED` |
| 4 | `clockings` | `clockings` | Pointages | true | aucun tant qu'il n'y a pas de workflow pointage (onglet affiché ; collab le cache si gereEnJours) |
| 5 | `daysDeclaration` | `days-declaration` | Déclaratifs en jours | true | `WORKFLOW_DECLARATION_DAILY` uniquement |

`name` = toCamelCase(removeSpecialChars(code)) (pas du CONSTANT_CASE).

## 🚨 Notes

Pool non assigné (`workflowTabId` null) :

- `WORKFLOW_SCHEDULE_OVERLOAD_TT` — **conserver le template et le seed. Rester non assigné. Mapping création, discriminateur, et route orpheline `/request-management/remote-work-schedule-overload` : disabled ou commentés jusqu'à un ticket dédié. Ne pas supprimer.**
- `WORKFLOW_DECLARATION_HOURLY` (type séparé, UI non implémentée)

Préférer un seed **recommended / post-common** (même layout dev + demo), après **seedWorkflowAndLevels()**.
