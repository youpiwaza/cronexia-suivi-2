# 💾 Back / 🌊✔️Workflows / 🔧 Onglets / 🐯🌐 NestJs > 🛣️ Route workflowsNotAffectedToTabs

## 👨‍💻 Dev

~ Récupération des **workflows non affectés** à un onglet (pool organize), ordonnés

🚨 Ce ne sont **pas** des onglets : ce sont les workflows sans tab. Patron RF : `resourceFieldsNotAffectedToTabs` / `GET /api/resource-field/not-affected-to-tabs`. Pas d’option « inactif » — le filtre **est** le non-affecté (`workflowTabId = null`).

---

## 🔨 Tech

`workflowsNotAffectedToTabs` :

- Jointures `workflowTabId = null` (un row max par workflow grâce à l'index unique partiel)
- `orderBy: { position: asc }`
- Nested `workflow { id, code, name, type, isActive, labelShort, targetEventForTypeEventRangeOnResource { type, isRemoteWork, isOnCallDuty, isTravelling, code, name } }` — même sélection que GTA-1628
- `workflow.isActive` et les flags Event sont **dans le payload** (organize : ligne disabled / pastilles). Ce n’est pas le filtre de la query.
- Un `eventRangeOnResource` sans Event cible = `targetEvent` null (pastilles admin)

Complète GTA-1628 (onglets ± non affectés). Ensemble = Backend-04 gather. Ne pas changer `resourcesGetWorkflowResource` / `userProfileInstanceGetWorkflowResource`.
