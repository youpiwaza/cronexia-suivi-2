# 👨‍💻 Dev

## workflow-tab.prisma

Même idée que resource-field-tab.prisma @cronexia-gta-back\app\prisma\schema\resource-field-tab.prisma , plus le split name / code déjà présent sur Workflow et Event. (ResourceFieldTab n'a pas encore name — ne pas normaliser ici, OOS.)

idWorkflowTab, timestamps, createdBy / updatedBy

name unique —  Dérivé de code : toCamelCase(removeSpecialChars(code)) (ex. code schedule-change → name scheduleChange). C'est le segment [[name]].

code unique — saisi admin / lisible. Unique aussi. Un changement de code régénère name (collision refusée). Pas le segment d'URL brut (accents / espaces / / exclus via la normalisation).

label unique — titre affiché (ex. Absences)

position Int

affected Boolean default false (barre vs zone « non affectés »)

iconKey String? optionnel — clé icon-config

---

## workflow-on-workflow-tab.prisma

Miroir de resource-field-on-resource-field-tab.prisma @cronexia-gta-back\app\prisma\schema\resource-field-on-resource-field-tab.prisma :

idWorkflowOnWorkflowTab

position Int?

workflowTab optionnel (workflowTabId null = pool non assigné)

workflow obligatoire

@@unique([workflowTabId, workflowId]) — autorise le même workflowId sur plusieurs onglets (ids de tab non-null)

Index unique partiel (même migration Backend-01) : workflowId WHERE workflowTabId IS NULL

---

## Relations

Mise à jour des jointures dans les tables concernées

---

## Tech ntoes

Pourquoi le partiel : en Postgres, UNIQUE (workflowTabId, workflowId) ne collisionne pas deux lignes (NULL, même workflowId) (NULL ≠ NULL). Sans index partiel, le pool « non assignés » peut contenir le même workflow deux fois. Les onglets (FK non-null) sont déjà protégés par le @@unique.

Relations inverses sur Workflow. Pas de groupes (les « items » d'un onglet sont les workflows). Un même workflow peut être sur plusieurs onglets. S'il est sur au moins un onglet, il n'a pas de ligne pool (workflowTabId null) — l'organize (wipe + recreate) maintient cet invariant. Pas deux fois dans le pool.

Pas de contrainte d'homogénéité. Un onglet peut mélanger des WorkflowTypeEnum et des sous-familles Event. La table union les extras ; la popup de création liste tous les workflows créables de l'onglet. L'admin autorise n'importe quel drop (CP + TT + Horaires sur le même onglet). Hint optionnel si l'onglet devient trop large — ne pas refuser le drop.

Note front : displayFamily se résout par workflow (type, puis flags Event si eventRangeOnResource). Les colonnes de l'onglet = union de ces familles.
