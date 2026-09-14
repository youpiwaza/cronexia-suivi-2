{
  resourcesGetWorkflowResource(
    # resource: {matricule: "123456A"}
    # resource: {lastName: "Chevasson"}
    # resource: {lastName: "Courtois"}
    # resource: {populationName: "String_lastName_startsWith_c"}
    # resource: {matricule: "05a7_Patrick_gere_en_heure_pointage_theoriques"} # Pointages théoriques cas 1, CYCLE_FIX7H_1
    # resource: {matricule: "A4B6_RouxE"} # Pointages théoriques cas 2, CYCLE_FIX7H_2
    # resource: {populationName: "generated_resources"}

    # period: {dateStart: "2024-04-01", dateEnd: "2024-04-07"}
    # period: {dateStart: "2024-04-01"}
    # workflowType: remoteWorkByEventRangeOnResource

    # Avec plusieurs niveaux de validation
    # resource: {matricule: "05a7_Patrick_gere_en_heure_pointage_theoriques"}
    # period: {dateStart: "2024-07-01", dateEnd: "2024-07-31"}
    # workflowType: scheduleOverload

    # Déclarations en jours
    resource: {matricule: "0b0b_Bob_gestion_en_jours"}
    period: {dateStart: "2024-04-01", dateEnd: "2024-04-15"}
    workflowType: declarationDays

    # Déclarations en heures
    # resource: {matricule: "05a7_Patrick_gere_en_heure_pointage_theoriques"}
    # period: {dateStart: "2024-04-01", dateEnd: "2024-04-15"}
    # workflowType: declarationHours
  ) {
    resources {
      idResource
      matricule
      lastName
      firstName

      workflowResources {
        workflowResource {
          idWorkflowResource

          workflow {
            type
          }

          submissionDate
          state
          stateDebug
          currentRank
          isCurrentDemandCancel
          resourceComment
          lastValidatorHelper

          workflowResourceLevelStates {
            idWorkflowResourceLevelState
            stateChangedAt
            state
            stateDebug
            validatorComment
            validatorHelper

            # Champ virtuel : Validateur attendu, pour certaines requêtes uniquement
            resourceCurrentValidatorUpiId
            resourceCurrentValidatorUpiEmail
            resourceCurrentValidatorMatricule
            resourceCurrentValidatorLastname
            resourceCurrentValidatorFirstname

            validator {
              description
              label

              user {
                resource {
                  matricule
                  firstName
                  lastName
                }
              }
            }

            workflowLevel {
              rank
            }
          }
        }

        typedRemoteWorkBySTO {
          periodFirstDate
          periodLastDate
          calculatedDays
          scheduleTypeOverLoads {
            effectDate
            overloadedType
          }
        }
        typedClocking {
          placeholder
        }
        typedRemoteWorkByEvent {
          dateStart
          dateEnd
          typeDayStart
          typeDayEnd
          calculatedDays
          eventRangeByDays {
            date
            quantity
            duration
            typeDay
          }
        }
        typedScheduleOverload {
          placeholder
        }
        typedDeclaration {
          idDeclaration
          type
          submissionDate
          isCheckboxChecked
          comment
          dateStart
          dateEnd
          calculatedDays
          declarationDailies {
            date
            enumValue
            value
            isCheckboxChecked
            comment
          }
          declarationHourlies {
            date
            theoreticalClockingOverload1
            theoreticalClockingOverload2
            theoreticalClockingOverload3
            theoreticalClockingOverload4
            isCheckboxChecked
            comment
          }
        }
      }
    }
  }
}
