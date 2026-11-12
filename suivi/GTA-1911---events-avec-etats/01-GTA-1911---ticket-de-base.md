# GTA-1911 / Gestion des impacts de l'état des events

A l'heure actuelle l'impact de l'état des events sur différents points fonctionnels n'est gérée que partiellement.

Or, un event à l'état "Validé" ne doit bien sûr pas avoir les mêmes conséquences métiers qu'un event à l'état "Refusé": ignorer l'état revient peu ou prou à éliminer tout intérêt à la notion de workflow de validation.

Note dev : Certains Event peuvent ne pas être associés à un workflow (flux de validation), ils sont considérés comme ayant été créés par un administrateur (ou gestionnaire RH) et sont donc considérés comme "Validé".

## Ce qu'il convient de faire

### Traiter les events à l'état "Annulé" "Brouillon" et "Refusé"

- Traiter les events à l'état "Annulé" "Brouillon" et "Refusé" comme devant être ignorés (comme s'ils n'existaient pas). C'est à dire que les events associés à cet état ne doivent avoir aucun impact sur:
  - ✂️ Compteurs > extrait dans [son propre ticket](https://cronexia.atlassian.net/jira/browse/GTA-1915) // OUT OF SCOPE
  - La génération des anomalies: KO actuellement
  - La gestion des conflits entre events → C'est ok aujourd'hui pour "Refusé" et "Brouillon". C'est KO pour "Annulé".

---

### Traiter les états "A valider"

Traiter les états "A valider" comme ceci:

- Pas d'impact sur les calculs de compteurs qui s'appuient sur des events KO actuellement ⏱️ 0,25j
- Pas d'impact sur la génération des anomalies (ces events doivent être ignorés) KO actuellement ⏱️ 0,1j
- Prise en compte dans la gestion des conflits entre events → C'est ok aujourd'hui
  - // à vérifier rapidement, s'assurer que cela fonctionne effectivement correctement

---

### Traiter les états "Validé" // OUT OF SCOPE

Pour l'état "Validé", les comportements actuels sont conformes.

---

## Points purement front à prévoir

- Les états des events dans les pages synthèses et anomalies ne sont pas visibles sans afficher de pop-up: il faut ajouter la même représentation des états dans ces écrans que celle déjà existante dans les plannings, l'emploi du temps et le calendrier des absences.⏱️ 0,25j
- Il faut ajouter une option permettant aux utilisateurs de choisir s'ils veulent visualiser ou masquer dans le front les events à l'état "Annulé" ou "Refusé".⏱️ 0,1j

---

## Dev

### Emplacements des fichiers

- Backend > base de données & tables
  - Event: cronexia-gta-back\app\prisma\schema\event.prisma
  - Workflows:
    - cronexia-gta-back\app\prisma\schema\workflow.prisma
      - contient les différents états dans `enum WorkflowStateEnum`
    - cronexia-gta-back\app\prisma\schema\workflow-level.prisma
    - cronexia-gta-back\app\prisma\schema\workflow-resource.prisma
    - cronexia-gta-back\app\prisma\schema\workflow-resource-level-state.prisma
- Backend seeds for examples
  - Events: cronexia-gta-back\app\prisma\seeds-new\02-recommended\event\events.seed.ts
  - Workflows (content heavy, so here's the recap documentation): cronexia-gta-back\app\prisma\seeds-new\02-recommended\workflow\workflow.seed.md
- Backend > Génération des events & détection des conflits
  - cronexia-gta-back\app\src\resources\functions\events\generate
  - appelé principalement depuis cronexia-gta-back\app\src\resources\resources.resolver.ts

- Frontend
  - anomalies page : cronexia-gta-front-v2\app\src\routes\(app)\(with-filters)\anomalies
  - summary / synthèse page : cronexia-gta-front-v2\app\src\routes\(app)\(with-filters)\summary
