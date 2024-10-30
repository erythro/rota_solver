from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor
from Services.DataService import DataService, Role, Rota

class ShareEqually(AbstractProcessor):
    dataService: DataService
    rolesPerPersonCounts: dict
    slotsPerRoleCounts: dict
    def __init__(self, dataService: DataService):
        self.dataService = dataService
        self.rolesPerPersonCounts = self.dataService.rolesPerPersonCounts()
        self.slotsPerRoleCounts = self.dataService.slotsPerRoleCounts()

    def process(self, model: Model):
        toMinimise = 0
        multiplier = 100
        
        for role_id, role in model.roles.items():
            divisor = 0
            for person_id in role.person_ids:
                divisor += 1 / self.rolesPerPersonCounts[person_id]
            for person_id in role.person_ids:
                expectedSlotsForPersonInRole = self.slotsPerRoleCounts[role_id] / divisor / self.rolesPerPersonCounts[person_id]
                possibilitiesForPersonInRole = model.possibilitiesByRoleAndPerson[(role_id,person_id)]
                sumPossibilitiesForPersonInRole = sum(possibilitiesForPersonInRole)
                absoluteDifference = model.model.NewIntVar(0, multiplier * len(possibilitiesForPersonInRole), f"difference_from_expected__person_{person_id}__in_role_{role_id}")
                model.model.AddAbsEquality(absoluteDifference, int(multiplier * expectedSlotsForPersonInRole) - multiplier * sumPossibilitiesForPersonInRole)
                toMinimise += absoluteDifference
        model.model.minimize(toMinimise)

        
        