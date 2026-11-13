# GTA-1915 / États des events sur un event de compteur

Découpe de [01---GTA-1915-compteurs-gestion-etat-des-events-pour-aggregats-uniquement.md](01---GTA-1915-compteurs-gestion-etat-des-events-pour-aggregats-uniquement.md), complément du 13/11 : le paramètre `Event`, pas l'agrégat.

Même règle que [02---GTA-1915---implement-events-states-for-counters-event-aggregation.md](02---GTA-1915---implement-events-states-for-counters-event-aggregation.md). Ce fichier ne recrée ni la table des états, ni le filtre Validé. Il lit les seaux déjà posés pour les agrégats, et il y branche le paramètre `entityType: Event`.

Une formule peut citer deux fois le même event, avec deux jeux d'états :

> Var cpValide = Event "CP Etat Validé"
>
> Var cpAValider = Event "CP Etat A valider"

Sans état, le paramètre ne compte que Validé. Un `Event` nu déjà en base ne change pas de chiffre.

[04---GTA-1915---adjust-existing-counters.md](04---GTA-1915---adjust-existing-counters.md) réécrit CPPA / RTTPA / TTPA et retire `VALEUR_EVENT_ETAT` / `SOMME_ANNEE_ETAT`. Tant que ce fichier-là n'est pas fait, ces fonctions gardent leur second argument.

Hors de ce fichier : agrégats, formules de congés, somme de quantités, contrôle de droits, affichage planning.

Estimation proposée : ⏱️ ~1 j. La table et les where du fichier 02 sont livrés avant.

---

## Règle cible

Même tableau que le fichier 02. Le jeu d'états vit sur le `CtParam` (`entityType: Event`). Plusieurs états = OU. Une liste écrite remplace le défaut.

| Jeu d'états sur le paramètre | Event compté |
| --- | --- |
| Aucun (défaut) | Validé seul |
| `validated` — Validé, seul | Validé seul |
| `pending` — A valider, seul | A valider seul |
| `validated` + `pending` | Validé ou A valider |
| `awaitingAttachements`, `draft`, `refused`, `cancelled` | Seulement si l'état est dans la liste |

Validé = demande `validated`, ou saisie directe sans workflow. Le défaut et la ligne `validated` seule ont le même effet, la même clé.

Jours et heures : les where du fichier 02, appelés tels quels. Jours, deux branches : `workflowResourceId: null`, ou `state: validated`. Heures, trois branches : `declarationHourlyId: null`, déclaration avec `workflowResourceId: null`, ou déclaration `validated`. Une saisie en heures sans déclaration, ou une déclaration sans workflow, compte avec Validé.

`eventReturnType` ne change pas. Le filtre choisit quelles occurrences entrent. Le paramètre lit ensuite `duration`, `quantity`, `typeDay`, `typeDayStart`, `typeDayEnd`, `timeStart` ou `timeEnd`.

---

## État des lieux

L'affichage d'un paramètre `Event`, dans `functions/display/counter/param.ts`, est `Event "CP" (Absence) <quantity><Float>`. Le libellé affiché est `labelShort`. Le commentaire du seed CPT23 écrit `Event.CP<quantity>`.

Le calcul journalier d'un event nu :

1. `extract/custom-fields/param.ts` pose `notFromAggreg` et recopie `eventReturnType` et les bornes horaires sur l'objet event. Deux paramètres sur le même event mutent le même objet : le second jeu d'états effacerait le premier si on le copiait ainsi.
2. `02-get-resources-with-mixed-events.ts` ne charge que Validé (`buildCountedWorkflowStateWhere`, `buildCountedDeclarationEventByDayWhere`). Le fichier 02 élargit ce chargement à l'union des jeux demandés par les agrégats. Ce fichier ajoute les jeux demandés par les paramètres `Event`.
3. `03-merge-mixed-events.ts` groupe par `event.code`. Plusieurs plages du même code, le même jour, s'additionnent dans un seul `values[date]`. Un CP Validé et un CP A valider le même jour deviennent un seul nombre. On ne peut plus les séparer après.
4. `01-reformat-for-counter.ts` copie ce groupe vers `EVENT__${code}`. Après la somme d'agrégat, les events seulement membres d'une agrégation sont retirés de cette map (vers 285). Un event avec `notFromAggreg` y reste.
5. `ct-counters.service.ts` (vers 4050) cherche `EVENT__${originalCustomField.name}` dans cette map et l'écrit dans `${counterCode}_EVENTS_VALUES`. `manage/param.ts` relit `EVENT__${event.name}`.

`code` d'un côté, `name` de l'autre. Les seeds les rendent égaux (`CP` / `CP`). Ce fichier ne corrige pas l'écart. Le défaut ne suffixe pas la clé : elle reste `EVENT__CP`. Un autre jeu d'états ajoute le même `stateKey` des trois côtés (reformat, boucle, `manageParam`).

`VALEUR_EVENT_ETAT` et `SOMME_ANNEE_ETAT` sont un autre chemin : préchargement par état dans `ct-counters.service.ts` (vers 2977 et 3086), lecture dans `functions/manage/function.ts`. `manageFunction` appelle d'abord `manageParam` sur l'argument `Event`, puis ignore ce retour et lit le préchargement. Le second argument est une constante (`null`, `validated`, `pending`), pas une ligne `workflowStates`. Ces fonctions ne passent pas par `EVENT__`. Ce fichier ne les ouvre pas.

Front admin. Le bloc `counter_event_ref` a le code d'event et le type de retour. Pas d'état. `blockToParam` l'ignore encore : le fichier 02 n'enregistre que le bloc agrégat. `block-builder.ts` rouvre le bloc depuis `param.event.code`.

Seeds sans état, à laisser ainsi : `CPT13_EVENT_VMED_DURATION.ts` (`VMED`, `duration`), `CPT14_EVENT_MAL_QUANTITY.ts` (`MAL`, `quantity`), `CPT23_EVENT_CP_QUANTITY.ts` (`CP`, `quantity`). L'orchestrateur les exécute (`counters.orchestrator.ts`, lignes 139, 144, 185). Ils sont le cas « event nu » en base. `events.seed.ts` laisse `name` = `code`.

---

## Ce qu'il convient de faire

### 1. Étendre l'union de chargement

Tant que chaque paramètre `Event` et chaque paramètre d'agrégat du compteur est sans état, ou `validated` seul, la requête ne change pas. Elle appelle les where du fichier 02, puis `mergeMixedEvents`, puis le reformat actuel. `mergeMixedEvents` n'est pas réécrit sur ce chemin. Séparer `workflowResourceId: null` de `state: validated` retire les saisies directes et les events générés de `EVENT__` : CPT13, CPT14, CPT23 et la somme des membres de `PVA` tombent à zéro.

Le `paramSecond` de `VALEUR_EVENT_ETAT` et de `SOMME_ANNEE_ETAT` n'est pas une liste `workflowStates`. CPPD, CPPA, et les jumeaux RTT / TT restent donc sur ce chemin par défaut. `function.ts` et les préchargements (vers 2878–3174) ne s'ouvrent pas.

L'union n'est élargie que si un paramètre `Event` de ce compteur demande un autre état. Ce jeu s'ajoute à l'union déjà prise pour les agrégats du même compteur. Un `pending` sur un autre compteur ne change pas cette requête.

`mergeMixedEvents` additionne ensuite toutes les occurrences d'un `event.code` dans un seul `values[date]`. Élargir le `where` sans couper avant cette addition fait entrer un `pending` dans `EVENT__${code}`. Un agrégat sans état du même compteur le compterait, et un event nu aussi.

Les seaux, un par `event.code` et par état, n'existent que sur ce chemin d'union, avant l'addition du jour. Deux CP le même jour, états différents, ne s'additionnent pas. Deux occurrences du même état, le même jour, additionnent encore `quantity` et `duration` comme le `+=` actuel. `typeDay`, `typeDayStart`, `typeDayEnd`, `timeStart` et `timeEnd` restent ceux de la première écriture. Le `null` reste `null` sur la valeur nue. Le passage de `null` à 0 reste celui du rollup d'agrégat, pas celui de l'event nu. Le seau Validé de l'union garde les lignes sans workflow (deux branches en jours, trois en heures).

Le seau d'un event nu garde l'objet du jour entier. La somme d'agrégat ne conserve que `duration` et `quantity`. Réutiliser cette forme pour l'event nu fait perdre `typeDay` et les heures de début et de fin.

### 2. Clé du paramètre Event

Le fichier 02 laisse `EVENT__${code}` comme seau Validé, sans suffixe. La somme d'agrégat lit cette clé. Ce fichier ne la déplace pas. La renommer en `EVENT__${code}__validated` vide la clé que lit la somme des membres de `PVA`, et rate CPT13, CPT14, CPT23.

- Défaut, liste absente, liste vide, ou `validated` seul : le reformat écrit `EVENT__${code}`. La boucle (ligne 4055, elle construit `EVENT__${originalCustomField.name}`, elle ne copie pas un nom de champ) et `manageParam` lisent `EVENT__${name}`. Aucun des trois n'ajoute `__validated` ni un autre suffixe. Quand `name` et `code` valent `CP`, les deux sont `EVENT__CP`. Un spec qui injecte `EVENT__CP` reste bon. `name` et `code` restent tels quels.
- Autre jeu : le reformat écrit `EVENT__${code}__${stateKey}`, la boucle et `manageParam` lisent `EVENT__${name}__${stateKey}`. `stateKey` est celui du fichier 02 (`pending`, `pending+validated`). Le suffixe est posé une fois dans chacun des trois. Un seul des trois met l'event nu à 0. La boucle construit la clé de lecture : ce n'est pas le double suffixe des agrégats. Un second suffixe sur la clé par défaut tombe sur l'objet zéro déjà écrit quand la clé manque (boucle vers 4122).

Ce `pending` n'est pas écrit dans `EVENT__${code}`, y compris quand ce compteur a chargé un `pending` pour un paramètre nu. Il n'entre pas dans une clé `EVENT_AGGREG__` dont le jeu ne le contient pas. Le seau Validé lu par la somme d'agrégat reste `EVENT__${code}` sans suffixe.

Aujourd'hui la boucle tourne une fois par event dédoublonné. Deux jeux sur le même code demandent une lecture par paramètre `Event`. Chaque lecture écrit sa propre clé. Les itérations qui partagent la clé par défaut remplacent `EVENT__${name}`. Elles ne l'additionnent pas une seconde fois, et elles n'y écrivent pas l'objet zéro.

L'extract garde un jeu d'états par paramètre, sur une copie, avant `deduplicateArrayContentsInObjectProps`. Le jeu n'est pas écrit sur l'objet event partagé. `notFromAggreg` reste sur l'entrée nue. Un event seulement membre d'une agrégation est encore retiré de la map directe après la somme d'agrégat. Ses seaux d'agrégat ne deviennent pas un paramètre `Event`.

`manageParam` lit la clé, puis le champ `eventReturnType`. Absent ce jour-là : les zéros déjà écrits par la boucle (`duration` 0, `quantity` 0, `typeDay*` `'null'`, heures `null`).

`originalCustomFields` est rejoué depuis `CtCounter.preprocessedDatas` quand `preprocessedDatasViaDatabase` est vrai. Les events en cache n'ont pas de propriété d'état. Absente ou vide, sur l'event en cache et sur le paramètre vivant : where actuel et `EVENT__` sans suffixe, des trois côtés. Une liste manquante compte Validé sous la clé actuelle. Elle ne compte pas « rien », et elle ne prend pas le suffixe `__validated` des agrégats.

### 3. Affichage

`functions/display/counter/param.ts`, cas `Event`. Avec des états : `Event "CP" Etat Validé`, en gardant le type de retour déjà affiché. Plusieurs : `Etat Validé, A valider`, mêmes libellés métier que le fichier 02. Sans état : libellé actuel.

### 4. Front admin

Bloc `counter_event_ref` : le même multi-choix que l'agrégat, après le type de retour. Rien de coché = pas de lignes en base = Validé.

`blockToParam` enregistre ce bloc : `entityType: Event`, `eventReturnType`, `event` connecté par `code`, `workflowStates.create` pour chaque état coché.

`block-builder.ts` recolle les états à l'ouverture.

`workflowStates` reste optionnel sur l'input de création. Rien de coché, et les clients qui ne l'envoient pas, créent zéro ligne.

### 5. Seeds

Payloads de create inchangés :

- CPT13 / `VMED` / `duration`
- CPT14 / `MAL` / `quantity`
- CPT23 / `CP` / `quantity`
- compteurs CP / RTT / TT (CPPD, CPPA, et les jumeaux)
- `events.seed.ts` : `name` reste égal à `code`

Les appels de l'orchestrateur (lignes 139, 144, 185) restent. Aucune ligne d'état sur ces paramètres. Ce fichier ne crée pas la table des états et n'émet pas de migration. Pas de colonne obligatoire sur `CtParam`.

Exemple dev : nouveau fichier, nouveau code de compteur. Deux variables sur `CP`, une sans état (`quantity`), une avec `pending` seul, puis une somme. Il ne remplace pas CPPA, CPT23, ni les seeds de congés. CPPA reste sur `SOMME_ANNEE_ETAT` jusqu'au fichier 04.

---

## Inventaire des impacts

### Fichiers dont le résultat change

- `cronexia-gta-back\app\src\ct-counters\functions\extract\custom-fields\param.ts`
- `cronexia-gta-back\app\src\ct-counters\functions\histo\04-events\02-get-resources-with-mixed-events.ts` (l'union inclut les paramètres `Event`)
- `cronexia-gta-back\app\src\ct-counters\functions\histo\04-events\03-merge-mixed-events.ts` — seaux seulement sur le chemin d'union. Le chemin par défaut garde la fonction actuelle
- `cronexia-gta-back\app\src\ct-counters\functions\histo\utility\01-reformat-for-counter.ts` — `EVENT__${code}` sans suffixe pour le défaut
- `cronexia-gta-back\app\src\ct-counters\ct-counters.service.ts` — la boucle ligne 4055 construit `EVENT__${name}`, suffixe une seule fois pour un autre jeu
- `cronexia-gta-back\app\src\ct-counters\functions\manage\param.ts` — même clé que la boucle
- `cronexia-gta-back\app\src\ct-counters\functions\display\counter\param.ts`
- `cronexia-gta-front-v2\app\src\routes\(app)\(without-filters)\admin\counter\blockly-renderer\blocks\registry.ts`
- `cronexia-gta-front-v2\app\src\lib\utils\counter\blockly-to-gql.ts`
- `cronexia-gta-front-v2\app\src\routes\(app)\(without-filters)\admin\counter\blockly-renderer\builders\block-builder.ts`

Un compteur dont tous les paramètres `Event` et tous les agrégats sont sans état, ou `validated` seul, lit les mêmes occurrences, par la même requête, puis `mergeMixedEvents`. La clé reste `EVENT__${code}` / `EVENT__${name}`, sans suffixe, dans le reformat, la boucle et `manageParam`. Le chiffre de CPT13, CPT14 et CPT23 ne change pas. `PVA` continue de sommer ses membres sur `EVENT__${code}`. Un preprocess déjà stocké sans propriété d'état suit le même chemin.

### Déjà conforme, à ne pas retoucher

- Table `CtParamWorkflowState`, corps des where du fichier 02, et migration.
- Clés `EVENT_AGGREG__` et somme d'agrégat, y compris le seau Validé `EVENT__${code}` sans suffixe.
- `PVA`, `PVAJ`, CPT15, CPT16, CPT17.
- `function.ts`, préchargements `SOMME_ANNEE`, `SOMME_ANNEE_ETAT`, `VALEUR_EVENT_ETAT`.
- Seeds CP / RTT / TT, payloads CPT13, CPT14, CPT23, `events.seed.ts`, appels d'orchestrateur lignes 139, 144, 185.
- Somme de quantités et `isWorkflowStateInEventRightsForecast`.

### Hors impact

- Génération d'anomalies, conflits, planning.
- Restriction horaire : le `OR` des plages et le filtre d'état restent côte à côte, comme le fichier 02. Rien de nouveau sur cette branche.

---

## Non-régression

### Specs à écrire

À lancer à la main.

- Un paramètre `Event` sans état, et un avec `validated` seul : les where du fichier 02, pas le helper d'union. Même clé `EVENT__${name}`, sans suffixe, dans le reformat, la boucle ligne 4055 et `manageParam`. Saisie directe, event généré, et déclaration sans workflow compris. `pending` ignoré. `EVENT__${code}` est encore là pour la somme d'agrégat. Le chemin par défaut reste `mergeMixedEvents`.
- `pending` seul : clé `EVENT__${name}__pending` seulement. Cet état, sans la branche sans workflow, sans les Validés. Rien n'est écrit dans `EVENT__${code}`.
- Deux paramètres, même event, jeux différents : deux clés, deux valeurs. Les lectures qui partagent la clé par défaut remplacent la valeur, elles ne l'additionnent pas. Le `pending` n'entre pas dans `EVENT__${code}` ni dans une clé `EVENT_AGGREG__` sans cet état.
- Deux occurrences le même état, le même jour : `quantity` et `duration` s'additionnent comme le `+=` actuel. `typeDay` et les heures restent ceux de la première écriture. `null` n'est pas converti en 0 sur la valeur nue. Deux états différents restent dans deux seaux. L'objet du jour garde `typeDay`, `typeDayStart`, `typeDayEnd`, `timeStart`, `timeEnd`.
- Heures : sans déclaration, ou déclaration sans workflow, compte avec Validé. Déclaration `pending` compte seulement si `pending` est dans le jeu.
- Un compteur dont les paramètres `Event` ne sont que des arguments de `VALEUR_EVENT_ETAT` / `SOMME_ANNEE_ETAT` (`paramSecond` constante) ne prend pas le chemin d'union.
- Preprocess déjà stocké, sans propriété d'état : même where, même clé `EVENT__` sans suffixe, des deux côtés (reformat et `manageParam`). Pas de suffixe `__validated`.
- Relance des specs de formule qui injectent `EVENT__${name}`. Cette clé ne prend pas de suffixe pour le défaut. CPT23 n'a pas de spec dédié aujourd'hui.

### Recette

Event `CP`, ou `MAL`, ou `VMED`. Rejouer en jours et en heures. « Sans état » et « Validé seul » : mêmes chiffres. Quantity (CPT23, CPT14) et duration (CPT13).

| État de l'event | Sans état, ou Validé seul | A valider seul | Validé + A valider |
| --- | --- | --- | --- |
| Pas de workflow | Compte | Ignoré | Compte |
| Validé | Compte | Ignoré | Compte |
| A valider | Ignoré | Compte | Compte |
| En attente de justificatif | Ignoré | Ignoré | Ignoré |
| Brouillon | Ignoré | Ignoré | Ignoré |
| Refusé | Ignoré | Ignoré | Ignoré |
| Annulé | Ignoré | Ignoré | Ignoré |

Deux variables additionnées (Validé + A valider) : le total égale la troisième colonne. Un agrégat `GROUPE_TT` sans état, dans le même compteur qu'un event `pending`, ne prend pas ce `pending` : `EVENT__${code}` ne contient que le Validé. Deux plages Validé le même jour restent additionnées. Un paramètre en `typeDay` ou en heure de début lit encore ces champs.

Écran d'admin : poser les deux variables, enregistrer, rouvrir. Les états cochés sont là. Rien de coché : aucune ligne d'état, libellé sans « Etat ».

`SOMME_ANNEE_ETAT(CP, pending)` de CPPA compte encore A valider. Ce n'est pas ce paramètre `Event`. Le fichier 04 le remplace.

### Jeux de données

- Events recommandés : `cronexia-gta-back\app\prisma\seeds-new\02-recommended\event\events.seed.ts` (`CP`, `MAL`, `VMED`, `name` = `code`)
- Event nu : `cronexia-gta-back\app\prisma\seeds\counter\CPT23_EVENT_CP_QUANTITY.ts` (CPT13, CPT14 à côté)
- Demandes à faire vivre : mêmes jeux que le fichier 02. Annulé : seeds dev du ticket conflits de GTA-1911. L'UI ne pose pas `cancelled`.

---

## Questions PO

Pas de question nouvelle. La confirmation sur `awaitingAttachements` est celle du fichier 02 : il ne compte que s'il est coché.

---

## Dev

### Emplacements des fichiers

- Déjà livrés par le fichier 02
  - table des états du `CtParam`
  - `cronexia-gta-back\app\src\resources\functions\events\times\build-counted-workflow-state-where.ts`
- Lecture event
  - `cronexia-gta-back\app\src\ct-counters\functions\extract\custom-fields\param.ts` (jeu par paramètre, sur une copie, avant le dédoublonnage)
  - `cronexia-gta-back\app\src\ct-counters\functions\histo\04-events\02-get-resources-with-mixed-events.ts` (union seulement si ce compteur demande un autre état)
  - `cronexia-gta-back\app\src\ct-counters\functions\histo\04-events\03-merge-mixed-events.ts` (corps actuel sur le chemin par défaut)
  - `cronexia-gta-back\app\src\ct-counters\functions\histo\utility\01-reformat-for-counter.ts` (`EVENT__${code}` sans suffixe pour le défaut)
  - `cronexia-gta-back\app\src\ct-counters\ct-counters.service.ts` (boucle ligne 4055 : construit `EVENT__${name}`)
  - `cronexia-gta-back\app\src\ct-counters\functions\manage\param.ts` (même clé, liste absente ou vide = sans suffixe)
  - `cronexia-gta-back\app\src\ct-counters\functions\display\counter\param.ts`
- Laissé au fichier 04
  - `cronexia-gta-back\app\src\ct-counters\functions\manage\function.ts`
  - préchargements `SOMME_ANNEE_ETAT` et `VALEUR_EVENT_ETAT` dans `ct-counters.service.ts`
- Front
  - `cronexia-gta-front-v2\app\src\routes\(app)\(without-filters)\admin\counter\blockly-renderer\blocks\registry.ts`
  - `cronexia-gta-front-v2\app\src\routes\(app)\(without-filters)\admin\counter\blockly-renderer\builders\block-builder.ts`
  - `cronexia-gta-front-v2\app\src\lib\utils\counter\blockly-to-gql.ts`
- Seeds, payloads inchangés. L'orchestrateur les appelle déjà
  - `cronexia-gta-back\app\prisma\seeds-new\150-post-dev\counter\counters.orchestrator.ts` (lignes 139, 144, 185)
  - `cronexia-gta-back\app\prisma\seeds\counter\CPT13_EVENT_VMED_DURATION.ts`
  - `cronexia-gta-back\app\prisma\seeds\counter\CPT14_EVENT_MAL_QUANTITY.ts`
  - `cronexia-gta-back\app\prisma\seeds\counter\CPT23_EVENT_CP_QUANTITY.ts`
  - `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-CP.seed.ts`
  - `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-RTT.seed.ts`
  - `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-TT.seed.ts`
  - `cronexia-gta-back\app\prisma\seeds-new\02-recommended\event\events.seed.ts` (`name` = `code`)
  - exemple PO : nouveau fichier, nouveau code
