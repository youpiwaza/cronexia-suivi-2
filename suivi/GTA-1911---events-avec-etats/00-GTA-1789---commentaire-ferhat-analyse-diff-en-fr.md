# GTA-1789 / Décision après confrontation avec les tickets 02 et 03

Source : [00-GTA-1789---commentaire-ferhat-possibilite-doublon.md](00-GTA-1789---commentaire-ferhat-possibilite-doublon.md). Comparé à [02-GTA-1911---anomaly-generation.md](02-GTA-1911---anomaly-generation.md) et [03-GTA-1911---conflicts-generation-and-management.md](03-GTA-1911---conflicts-generation-and-management.md), vérifié dans le code, tranché en réunion avec Ferhat le 12/11/2026, puis revu le soir même sur son push `hfix-1789-ajustement`.

Historique GTA-1789, déjà dans `main` : branche `hfix-1789-adec-pdec-chevauchement`. Back PR #87, merge `8108995b` du 09/11/2026. Front PR #194, merge `8ec059ef` du même jour.

Push du 12/11 au soir, pas encore dans `main` : branche `hfix-1789-ajustement`. Back `4f6cb56a`. Front `ef25e855` (anneau de survol sur la frise d'anomalies, pas le prédicat de conflit).

---

## Décision

Il y a deux contrôles de conflit, et ils n'appliquent pas la même règle.

- Formulaires, front : popup à la saisie, à la soumission et à la validation. Une demande A valider occupe la période. C'est le périmètre que Ferhat rattache à GTA-1789, et la partie popup ADEC / PDEC y est déjà livrée. Les tickets 02 et 03 ne la refont pas.
- Génération, back : anomalies et CONFLI* produits par le générateur. Le filtre d'état est livré le 12/11 au soir. La régénération à l'entrée et à la sortie de Validé, et les données déjà générées, restent le ticket 02.

Règle du générateur, livrée dans `4f6cb56a` : un event compte seulement s'il n'a pas de workflow, ou si sa demande est Validé. Jours et heures. A valider ne compte plus. Le commentaire du fichier ignore aussi l'attente de justificatif, au même titre que brouillon, refusée et annulée. La popup compte toujours « en attente ».

Écart avec la décision écrite juste avant ce push : les branches GTA-1789 ont été effacées, pas commentées. `WORKFLOW_STATES_NOT_COUNTED_AS_INPUT` est retiré du fichier. Les rétablir demande de les réécrire. Si la marche arrière doit rester dans le source, les remettre en commentaire sur cette branche.

ADEC / PDEC ne comptent qu'une fois la déclaration validée. Déjà en place des deux côtés (générateur et popup). Rien à refaire.

La phrase de son commentaire « une demande en attente compte comme absence, dans le générateur comme dans la popup » décrivait GTA-1789. Elle ne tient plus pour le générateur. La popup continue de compter A valider. Le générateur non. Les deux tickets 02 et 03 sont écrits sur cette séparation.

---

## Ce que Ferhat a livré

Trois commits du 07/11/2026, auteur Ferhat SAIDOUN.

- Back `4f44db70`. Crée `build-counted-workflow-state-where.ts` et son spec, branchés sur les deux requêtes de saisies manuelles. Brouillon, Refusé et Annulé sont ignorés. A valider compte encore. ADEC / PDEC ne comptent qu'une fois la déclaration validée. Les events restent créés dès le brouillon, pour l'affichage (GTA-1770).
- Back `c53e350a`. Plusieurs saisies actives du même type justifient ensemble l'absence, du début le plus tôt à la fin la plus tardive. Voir plus bas : ce comportement est conservé par le remplacement ultérieur.
- Front `92a8b9a7`. `isAbsenceCountedForConflicts` ne compte un ADEC / PDEC généré que si sa déclaration est validée. Le filtre d'affichage de la page absences reste inchangé : le brouillon reste visible.

Le spec de ce premier livrable attendait un `notIn [draft, refused, cancelled]`. `4f6cb56a` le passe à « null ou `validated` », libellé GTA-1911, pour les deux fonctions.

---

## Écart, après décision

| Point des tickets | Déjà en place | Reste à faire |
| --- | --- | --- |
| 02 §1. Filtre « sans workflow, ou Validé » | Livré dans `4f6cb56a`, jours et heures. `pending` et `awaitingAttachements` ignorés. Spec à jour. Pas encore dans `main` | Remettre les branches effacées en commentaire, si on veut pouvoir rétablir A valider sans les réécrire |
| 02 §2. Régénérer à l'entrée et à la sortie de Validé | Rien | Tout le point. Brouillon → A valider n'empile pas : les deux états sont ignorés |
| 02 §3. Données déjà générées | Rien | Tout le point, et la question PO qui va avec |
| 03 §1. Le front ignore `cancelled` dans `isConflictingWorkflowState` | Rien. Son commit front ne touche pas ce prédicat | Tout le point. Côté formulaires, pas le générateur |
| 03 §2. Filtre d'état sur les events en heures des formulaires | Rien sur ces fichiers. Son changement porte sur les ADEC / PDEC générés | Tout le point : `check-workflow-demand-conflicts.ts`, branches `catch` de `HoursAbsence.svelte` |
| 03 §3. Le brouillon dans les gardes back du même event | Rien. Les gardes excluent `refused` et `cancelled`, et gardent `draft` | Tout le point, sous réserve de la question PO. `pending` reste bloquant |
| 03 §4. Génération des CONFLI* | Le filtre du générateur est celui de `4f6cb56a` | Aucun code de filtre ici. L'empilement à l'entrée et à la sortie de Validé reste le ticket 02. La recette CONFLI* attend le merge |

Côté formulaires, vérifié dans le code actuel et inchangé par la décision :

- `isConflictingWorkflowState` exclut Refusé et Brouillon. Il ne connaît pas `cancelled`. A valider passe, et doit continuer de passer.
- `check-workflow-demand-conflicts.ts` filtre les events en jours par `isUserInput` puis le prédicat, et les events en heures par `isUserInput` seul.
- Les deux `catch` de `HoursAbsence.svelte` filtrent par `isAbsenceCountedForConflicts` seul.
- `DaysAbsence.svelte` et `check-timeline-event-conflicts.ts` appliquent les deux filtres, jours et heures.

---

## Deux absences qui justifient ensemble la plage

Son second correctif (ADEC validé + DEL conservés : plus d'AINJ sur la plage commune, le chevauchement reste un CONFLIMLTP) est conservé.

Le commit `bdd79147` du 09/11/2026, après le merge de sa PR, retire l'appel à `mergeSameAttendanceManualEvents` et le remplace par `resolvingManualEventCoverage`. `4f6cb56a` supprime le helper et son spec, qui n'avaient plus d'appelant.

Comparé à ce qu'il a livré : pas de régression sur le cas qu'il a livré. Deux absences du même type justifient encore du début le plus tôt à la fin la plus tardive. Une seule saisie résout encore seulement si son type correspond. La comparaison de fin de journée (secondes à 59) est gardée, sur une copie : la pile n'est plus mutée.

Le seul écart est une pile mixte, une absence et une présence actives en même temps. Chez lui, les types différents ne justifient rien : l'AINJ reste ouverte, y compris sur la part couverte par l'absence. Le remplacement ne garde que les saisies du même type que l'anomalie en cours. L'absence ferme l'AINJ. La présence ne prolonge pas la plage. C'est le comportement asserté par `resolve-anomaly-against-coverage.spec.ts`. Le chemin CONFLIMLTP n'était ni dans son commit ni dans `bdd79147`.
