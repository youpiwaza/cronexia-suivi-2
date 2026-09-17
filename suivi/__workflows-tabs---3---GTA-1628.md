# 💾 Back / 🌊✔️Workflows / 🔧 Onglets / 🐯🌐 NestJs > 🛣️ Route workflowTabsForNavigation

## 👨‍💻 Dev

~ Récupération des onglets, ordonnés, & workflows groupés à l’intérieur

🚨 Option afin de récupérer ou non les onglets **non affectés** (`affected: false`) — pour l’admin organize. Défaut = `affected: true` (nav `/demands` + `/request-management`). Source unique = `WorkflowTab.affected` (même patron `ResourceFieldTab`). **Pas** de flag `isActive` d’onglet.

---

## 🔨 Tech

`workflowTabsForNavigation` (nom TBD) :

- Défaut : `where: { affected: true }`, `orderBy: { position: asc }`
- Arg admin : `includeUnaffectedTabs` (défaut `false`) — si `true`, pas de filtre `affected` (organize splitte ensuite sur `affected`, comme RF)
- Nested `workflowTab { name, code, label, position, iconKey, affected }` + `workflow { id, code, name, type, isActive, labelShort, targetEventForTypeEventRangeOnResource { type, isRemoteWork, isOnCallDuty, isTravelling, code, name } }`
- `workflow.isActive` et les flags Event sont **dans le payload** (visibilité + discriminateur **côté front**). Ce n’est pas le filtre de la query.
- Un `eventRangeOnResource` sans Event cible = `targetEvent` null (pastilles admin)

Patron lecture : gather dédié (Prisma `include` pour éviter le N+1 des ResolveFields). CRUD `workflowTabs` inchangé.
