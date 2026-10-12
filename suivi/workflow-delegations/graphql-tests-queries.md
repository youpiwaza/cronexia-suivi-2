# Requêtes GraphQL — délégations

`POST http://localhost:3000/graphql`. Mot de passe commun : [________________graphiql-auth.md](../________________graphiql-auth.md). Header des requêtes suivantes : `Authorization: Bearer ACCESS_TOKEN` (le `accessToken` du login, pas le refresh).

Lectures exécutées le 12 octobre 2026 sur la base alors en cours. Cette base a les slots `delegue*` mais **aucun** `ResourceBolVal` `isDelegationActive` / `isDelegationWhenAbsent`, donc aucune délégation n'est effective. Les mutations et le bloc « après reset » ne sont pas exécutés.

Pas d'argument `actingAs`. `userProfileInstance` est l'UPI d'autorisation (UPI du titulaire). Le JWT reste la personne réelle.

UPI seed :

| Qui | Id |
| --- | --- |
| Georges Malville, Gestionnaire RH | `00000000-0000-0000-ffff-000000000001` |
| Maxime Durand, Manager | `00000000-0000-0000-ffff-000000000002` |
| Murielle Colbert, Manager | `00000000-0000-0000-ffff-000000000003` |
| Pierre-Olivier Courtois, Gestionnaire RH | `00000000-0000-0000-ffff-000000000005` |
| Patrick, Collaborateur (slot délégué, pas le `supi` JWT de ce login) | `00000000-0000-0000-ffff-00000000000a` |

Patrick : matricule `05a7_Patrick_gere_en_heure_pointage_theoriques`. Workflow 2 niveaux : `WORKFLOW_SCHEDULE_OVERLOAD` (`scheduleOverload`), rang 1 Manager, rang 2 Gestionnaire RH. Mêmes rangs sur CMAR et ENFM.

## Auth

Logins qui répondent 200 : `maxime.durand`, `patrick.gere-en-heure`, `georges.malville`, `murielle.colbert`, `amelie.dupont`, `super.admin`.

JWT lus : Maxime `supi` `…0002` / `supc` `MANAGER`. Georges `supi` `…0001` / `HR_MANAGER`. Murielle `supi` `85151205-19a3-4b5a-bfac-5820ba114171` / `ADMIN` (son UPI Manager `…0003` est une autre instance, qu'elle possède). Patrick `supi` `0bb4f7ec-e252-4769-a2bf-03f6af1f1764` / `EMPLOYEE` (pas `…000a`).

```graphql
mutation Login($data: LoginInput!) {
  login(data: $data) {
    accessToken
    tokenType
  }
}
```

```json
{
  "data": {
    "login": "maxime.durand",
    "password": "<voir ________________graphiql-auth.md>"
  }
}
```

Sans header, `myActiveDelegations` : HTTP 401, `errors.message` `Unauthorized`, `statusCode` 401.

## Menu — base courante

Même requête pour chaque persona. Résultat exécuté : `[]` pour Maxime, Patrick, Georges, Murielle, Amélie. Les slots existent (Murielle `delegue1` = Maxime ; Pierre-Olivier `delegue1` = Maxime et `delegue2` = Georges) mais les drapeaux sont absents, donc la délégation n'est pas effective.

```graphql
query MyActiveDelegations {
  myActiveDelegations {
    resourceId
    matricule
    label
    photoId
    userProfileInstances {
      idUserProfileInstance
      label
      userProfileCode
      userProfileLabel
    }
  }
}
```

```json
{}
```

```json
{
  "Authorization": "Bearer ACCESS_TOKEN"
}
```

## Menu — après reset

Exécuté le 12/10/2026 après reset dev. Murielle `isDelegationActive` true. Pierre-Olivier `isDelegationWhenAbsent` true, CP jusqu'au 30/06/2027. Maxime Durand : menu vide côté titulaire (les deux drapeaux false).

Même query `MyActiveDelegations`.

- Maxime : Pierre-Olivier (`987654B`), `[0]` = `…0005` `HR_MANAGER`, puis le profil Collaborateur. Murielle (`f5be_Murielle_manager`) : `[0]` = `06a07993-e657-40f1-a56b-cbf3bd11b03b` `ADMIN`, `[1]` = `…0003` `MANAGER`, `[2]` Collaborateur. Le tri par rang met Admin avant Manager. L'UPI à passer pour valider est `…0003`, pas `[0]`.
- Georges : Pierre-Olivier seulement (`…0005`). Pas Murielle.
- Patrick : Murielle seulement (slot `delegue2` = `…000a`). Même ordre de profils : Admin en `[0]`, Manager `…0003` en `[1]`.
- Murielle : `[]`. Amélie : `[]`.

## Liste titulaire

Exécuté en Murielle, argument `…0003` (elle possède cette UPI), Patrick, `ignorePeriod: true`. HTTP 200, 60 demandes. Ne pas sélectionner `workflowResource.resource` : la liste répond alors HTTP 500 (panic Prisma `findUniqueOrThrow`).

Sur la liste, `lastValidatorId` et `lastDelegatedForValidatorId` reviennent `null`. Les scalaires du niveau (`delegatedForValidatorId`, `validatorId`) sont remplis. Les scalaires de la demande sont lisibles via `workflowResource(id)` plus bas.

```graphql
query ListeTitulaire(
  $userProfileInstance: FindUniqueUserProfileInstanceInput!
  $resource: ResourceInput
  $period: DayOrPeriodInput
  $ignorePeriod: Boolean
) {
  userProfileInstanceGetWorkflowResource(
    userProfileInstance: $userProfileInstance
    resource: $resource
    period: $period
    ignorePeriod: $ignorePeriod
  ) {
    workflowResources {
      workflowResource {
        idWorkflowResource
        state
        currentRank
        lastValidatorId
        lastDelegatedForValidatorId
        lastValidatorHelper
        lastDelegatedForValidatorHelper
        workflowResourceLevelStates {
          idWorkflowResourceLevelState
          state
          validatorId
          delegatedForValidatorId
          validatorHelper
          delegatedForValidatorHelper
          resourceCurrentValidatorUpiId
          resourceCurrentValidatorFirstname
          resourceCurrentValidatorLastname
          workflowLevel {
            rank
          }
        }
      }
    }
  }
}
```

```json
{
  "userProfileInstance": {
    "idUserProfileInstance": "00000000-0000-0000-ffff-000000000003"
  },
  "resource": {
    "matricule": "05a7_Patrick_gere_en_heure_pointage_theoriques"
  },
  "ignorePeriod": true
}
```

Header : token Murielle.

Six demandes portent une trace `delegatedFor*` : surcharge `…0109` / `…0110`, CMAR `…0809` / `…0810`, ENFM `…0909` / `…0910`.

Surcharge scénario 21, `de700000-3500-0000-0000-000000000109` : `state` `pending`, `currentRank` 2. Rang 1 `validated`, `validatorId` `…0002`, `delegatedForValidatorId` `…0003`. Validateur courant de la resource : Murielle Colbert / `…0003` (le titulaire, pas l'acteur).

Surcharge scénario 22, `…0110` : `state` `validated`, `currentRank` 2. Rang 1 : Murielle, `delegatedForValidatorId` null. Rang 2 : `validatorId` `…0001`, `delegatedForValidatorId` `…0005`. Validateur courant : Pierre-Olivier Courtois / `…0005`.

## Trace demande (scalaires WR)

La query directe renvoie la paire que la liste omet. Exécuté.

```graphql
query WorkflowResource($idWorkflowResource: String) {
  workflowResource(idWorkflowResource: $idWorkflowResource) {
    idWorkflowResource
    state
    currentRank
    lastValidatorId
    lastValidatorHelper
    lastDelegatedForValidatorId
    lastDelegatedForValidatorHelper
  }
}
```

`…0109` : `lastValidatorId` `…0002`, helper Maxime Durand Manager. `lastDelegatedForValidatorId` `…0003`, helper Murielle / `f5be_Murielle_manager`.

`…0110` : `lastValidatorId` `…0001` (Georges). `lastDelegatedForValidatorId` `…0005`, helper Pierre-Olivier / `987654B`.

Même forme sur `…0809` / `…0810` et `…0909` / `…0910`.

## Liste délégué — base courante

Même query `ListeTitulaire`. Exécuté avec le token Maxime, Patrick, Georges ou Amélie, UPI Murielle `…0003` ou Pierre-Olivier `…0005`.

Résultat : `CRO_WR_UPI_000000004`, « Cette délégation n'est plus active. » Le gate refuse avant la liste. Ce n'est pas `000000005` : sans drapeau effectif, un appelant qui n'est pas propriétaire reçoit 004, y compris quelqu'un qui n'a jamais été délégué.

```json
{
  "userProfileInstance": {
    "idUserProfileInstance": "00000000-0000-0000-ffff-000000000003"
  },
  "resource": {
    "matricule": "05a7_Patrick_gere_en_heure_pointage_theoriques"
  },
  "ignorePeriod": true
}
```

Header : token Maxime (puis répéter Georges, Patrick, Amélie, et `…0005`).

## Négatifs exécutés

UPI inconnue, token Maxime, même query `ListeTitulaire` :

```json
{
  "userProfileInstance": {
    "idUserProfileInstance": "00000000-0000-0000-ffff-00000000dead"
  },
  "ignorePeriod": true
}
```

`CRO_WR_UPI_000000003`, « L'instance de profil utilisateur est introuvable. »

Token d'un autre utilisateur, UPI Maxime `…0002` : encore `000000003`. Sur cette base Maxime n'a pas de resource (`resource(matricule: "f5bf_Maxime_Durand")` → `CRO_000000001`). Le gate traite une UPI dont l'utilisateur n'a pas de `resourceId` comme introuvable. Le contrôle inactif S4 (drapeaux false, `delegue1` = Murielle) n'est donc pas observable ici.

## Recette Patrick après reset

Listes exécutées le 12/10/2026. Mutations toujours non exécutées. Deux demandes sur `WORKFLOW_SCHEDULE_OVERLOAD`, octobre 2026. Les scénarios 21 et 22 restent des traces : ne pas les revalider.

Même query `ListeTitulaire`, période octobre.

```json
{
  "userProfileInstance": {
    "idUserProfileInstance": "00000000-0000-0000-ffff-000000000003"
  },
  "resource": {
    "matricule": "05a7_Patrick_gere_en_heure_pointage_theoriques"
  },
  "period": {
    "dateStart": "2026-10-01",
    "dateEnd": "2026-10-31"
  },
  "ignorePeriod": false
}
```

Attendu, token Maxime :

- UPI `…0003` : `de700000-3500-0000-0000-000000001101` (12/10/2026), `currentRank` 1. Rang 1 `pending`. Rang 2 `pending` / `pendingLowerLevel`.
- UPI `…0005` : `de700000-3500-0000-0000-000000001102` (13/10/2026), `currentRank` 2. Rang 1 `validated` par Murielle (`delegatedForValidatorId` null). Rang 2 `pending`.

Token Georges, UPI `…0005` : la même demande rang 2. UPI `…0003` : `CRO_WR_UPI_000000005`, « Vous n'êtes pas délégué actif de ce titulaire. » (délégation Murielle effective, Georges n'est pas son délégué).

Token Amélie, UPI `…0003` ou `…0005` : `000000005` aussi. Token Murielle, UPI `…0003` : même ensemble que Maxime, elle est propriétaire.

### Valider le rang 1 (Maxime pour Murielle) de la demande de patrick du 12/10/2026

Non exécuté. Niveau rang 1 de `…1101` : `de700000-3515-0000-0000-000000001101`.

```graphql
mutation Cascade(
  $userProfileInstance: FindUniqueUserProfileInstanceInput!
  $workflowResourceLevelState: FindUniqueWorkflowResourceLevelStateInput!
  $newState: WorkflowStateEnum!
  $validatorComment: String
) {
  userProfileInstanceUpdateWrlsStatusWithCascade(
    userProfileInstance: $userProfileInstance
    workflowResourceLevelState: $workflowResourceLevelState
    newState: $newState
    validatorComment: $validatorComment
  ) {
    wrls {
      idWorkflowResourceLevelState
      state
      validatorId
      delegatedForValidatorId
      validatorHelper
      delegatedForValidatorHelper
      workflowLevel {
        rank
      }
      workflowResource {
        idWorkflowResource
        state
        currentRank
        lastValidatorId
        lastDelegatedForValidatorId
        lastValidatorHelper
        lastDelegatedForValidatorHelper
      }
    }
    warnings {
      cronexiaCode
      messageHuman
    }
  }
}
```

```json
{
  "userProfileInstance": {
    "idUserProfileInstance": "00000000-0000-0000-ffff-000000000003"
  },
  "workflowResourceLevelState": {
    "idWorkflowResourceLevelState": "de700000-3515-0000-0000-000000001101"
  },
  "newState": "validated",
  "validatorComment": null
}
```

Header : token Maxime. Attendu : `validatorId` `…0002`, `delegatedForValidatorId` `…0003`, `lastValidatorId` / `lastDelegatedForValidatorId` la même paire, `currentRank` passe à 2, `state` resource `pending`. Notification validateur : Murielle + Maxime (fan-out GTA-1658). Pas de toast.

Même mutation, token Georges : `CRO_WR_UPI_000000005` avant toute écriture.

### Valider le rang 2 (Maxime ou Georges pour Pierre-Olivier) de la demande de patrick du 12/10/2026

Non exécuté. Même demande que le rang 1 : `de700000-3500-0000-0000-000000001101`. Niveau rang 2 : `de700000-3515-0000-0000-000000001102`. À lancer après la validation du rang 1 ci-dessus (`currentRank` passé à 2). Même mutation. Header : token Maxime, puis le même corps avec le token Georges.

```json
{
  "userProfileInstance": {
    "idUserProfileInstance": "00000000-0000-0000-ffff-000000000005"
  },
  "workflowResourceLevelState": {
    "idWorkflowResourceLevelState": "de700000-3515-0000-0000-000000001102"
  },
  "newState": "validated",
  "validatorComment": null
}
```

Attendu Maxime : `validatorId` `…0002`, `delegatedForValidatorId` `…0005`, resource `validated`. Attendu Georges : `validatorId` `…0001`, `delegatedForValidatorId` `…0005`. Ne valider la demande qu'une fois. Notification validateur : Pierre-Olivier + Maxime + Georges.

## Refuser le rang 2 (Maxime ou Georges pour Pierre-Olivier) de la demande de patrick du 13/10/2026

```json
{
  "userProfileInstance": {
    "idUserProfileInstance": "00000000-0000-0000-ffff-000000000005"
  },
  "workflowResourceLevelState": {
    "idWorkflowResourceLevelState": "de700000-3515-0000-0000-000000001104"
  },
  "newState": "refused",
  "validatorComment": "Nope par délégation"
}
```

## Mutations documentées, non exécutées

Refus sans commentaire, token Maxime, UPI Murielle, un WRLS encore `pending` : `CRO_WRLS_UPI_000000006`, « En cas de refus, le commentaire du validateur est obligatoire. » Même mutation `Cascade` avec `"newState": "refused"` et `"validatorComment": null` ou `""`.

`CRO_RUPIV_000000001` — soi-même sur un slot `delegue*` (`excludeSelf`). Murielle, son UPI Manager sur sa propre fiche :

```graphql
mutation CreateRupiv($params: CreateResourceUserProfileInstanceValInput) {
  createResourceUserProfileInstanceVal(params: $params) {
    idResourceUserProfileInstanceVal
  }
}
```

```json
{
  "params": {
    "effectDate": "2026-10-12",
    "fieldnameHelper": "delegue2",
    "resource": { "connect": { "matricule": "f5be_Murielle_manager" } },
    "resourceField": { "connect": { "name": "delegue2" } },
    "userProfileInstance": {
      "connect": {
        "idUserProfileInstance": "00000000-0000-0000-ffff-000000000003"
      }
    }
  }
}
```

« Ce champ n'accepte pas une instance de profil de la même ressource. »

`CRO_RUPIV_000000002` — même personne déjà sur un autre `delegue*`. Maxime est déjà `delegue1` de Murielle (`a143`). Le remettre sur `delegue2` :

```json
{
  "params": {
    "effectDate": "2026-10-12",
    "fieldnameHelper": "delegue2",
    "resource": { "connect": { "matricule": "f5be_Murielle_manager" } },
    "resourceField": { "connect": { "name": "delegue2" } },
    "userProfileInstance": {
      "connect": {
        "idUserProfileInstance": "00000000-0000-0000-ffff-000000000002"
      }
    }
  }
}
```

« Cette personne est déjà désignée comme délégué. »

## Notifications lues

Token Murielle. Exécuté : tableau vide. Aucune notification de délégation n'a été créée (aucune validation lancée).

```graphql
query Notifications($take: Int) {
  notifications(take: $take) {
    idNotification
    message
    isRead
  }
}
```

```json
{
  "take": 5
}
```

## Hors GraphQL

Le front s'arrête aux builders GTA-1659. Confirmé dans le code (étape 2) ; le passage navigateur est l'étape 6.

- Pas d'entrée de menu Délégation, pas d'appel Svelte à `myActiveDelegations`.
- Gestion des demandes : redirection si le profil n'est pas Manager, Gestionnaire RH, Admin ou Super admin. La liste part de l'UPI personnelle (`selectedUserProfileInstanceId`), pas de l'UPI titulaire.
- Les mappers de timeline ignorent `delegatedFor*`. `ValidatedFromDelegation` n'est jamais assigné.
- Les booléens du dossier passent par le champ générique. `excludeSelf` n'est pas sélectionné ; le picker masque le matricule courant via `excludeMatricule`.
- Le texte de notification s'affiche tel quel. Le lien part vers la boîte personnelle ou `/demands`, pas vers la file du titulaire.
- Widget validation : hors sujet (GTA-1664).
