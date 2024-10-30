from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor
from Services.DataService import DataService, Role, Rota

class ShareEqually(AbstractProcessor):
    dataService: DataService
    rolesPerPersonCounts: dict
    slotsPerRoleCounts: dict
    expectedPeriods: dict
    averageRoleCountsPerEvent: dict
    def __init__(self, dataService: DataService):
        self.dataService = dataService
        self.rolesPerPersonCounts = self.dataService.rolesPerPersonCounts()
        self.slotsPerRoleCounts = self.dataService.slotsPerRoleCounts()
        self.expectedPeriods = self.dataService.expectedPeriods()
        self.averageRoleCountsPerEvent = self.dataService.averageRoleCountsPerEvent()
    def process(self, model: Model):
        toMinimise = 0
        multiplier = 100
        
        for role_id, role in model.roles.items():
            expectedShareOfRole = dict()
            ratioOfRemainingShare = dict()
            for person_id in role.person_ids:
                if (person_id, role_id) in self.expectedPeriods:
                    expectedShareOfRole[person_id] = 1/self.expectedPeriods[(person_id, role_id)]/self.averageRoleCountsPerEvent[role_id]
                else:
                    ratioOfRemainingShare[person_id] = 1/self.rolesPerPersonCounts[person_id]
        
            remainingExpectedShareFromOverrides = 1 - sum(expectedShareOfRole.values())
            totalRatioOfRemainingShare = sum(ratioOfRemainingShare.values())

            for person_id in role.person_ids:
                if person_id not in expectedShareOfRole:
                    if remainingExpectedShareFromOverrides > 0:
                        expectedShareOfRole[person_id] = remainingExpectedShareFromOverrides * ratioOfRemainingShare[person_id] / totalRatioOfRemainingShare
                    else:
                        expectedShareOfRole[person_id] = 0
                
                expectedSlotsForPersonInRole = expectedShareOfRole[person_id] * self.slotsPerRoleCounts[role_id]

                possibilitiesForPersonInRole = model.possibilitiesByRoleAndPerson[(role_id,person_id)]
                sumPossibilitiesForPersonInRole = sum(possibilitiesForPersonInRole)
                absoluteDifference = model.model.NewIntVar(0, multiplier * len(possibilitiesForPersonInRole), f"difference_from_expected__person_{person_id}__in_role_{role_id}")
                model.model.AddAbsEquality(absoluteDifference, int(multiplier * expectedSlotsForPersonInRole) - multiplier * sumPossibilitiesForPersonInRole)
                toMinimise += absoluteDifference
        model.model.minimize(toMinimise)

        
        