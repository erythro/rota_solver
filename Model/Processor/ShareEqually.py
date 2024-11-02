from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor
from Services.DataService import DataService, Role, Rota

class ShareEqually(AbstractProcessor):
    dataService: DataService
    rolesPerPersonCounts: dict
    slotsPerRoleCounts: dict
    onOneInXEvents: dict
    averageRoleCountsPerEvent: dict
    weight: int
    def __init__(self, dataService: DataService, weight: int):
        self.dataService = dataService
        self.rolesPerPersonCounts = self.dataService.rolesPerPersonCounts()
        self.slotsPerRoleCounts = self.dataService.slotsPerRoleCounts()
        self.onOneInXEvents = self.dataService.onOneInXEvents()
        self.averageRoleCountsPerEvent = self.dataService.averageRoleCountsPerEvent()
        self.weight = weight
    def process(self, model: Model):
        toMinimise = 0
        multiplier = 100
        
        for role_id, role in model.roles.items():
            expectedShareOfRole = dict()
            ratioOfRemainingShare = dict()
            for person_id in role.person_ids:
                if (person_id, role_id) in self.onOneInXEvents:
                    # someone should be on for example 1 in 3 events, so we can calculate now what their expected share will be of slots with that role
                    expectedShareOfRole[person_id] = 1/self.onOneInXEvents[(person_id, role_id)]/self.averageRoleCountsPerEvent[role_id]
                else:
                    # if we don't know how often they should be on, we share it out equally based on how many other roles they have, so we save that for later
                    ratioOfRemainingShare[person_id] = 1/self.rolesPerPersonCounts[person_id]
        
            # the remainder that isn't accounted for by the preset expected periods
            remainingExpectedShareFromOverrides = 1 - sum(expectedShareOfRole.values())

            # the total ratio we are sharing out the remainder by
            totalRatioOfRemainingShare = sum(ratioOfRemainingShare.values())

            for person_id in role.person_ids:
                if person_id not in expectedShareOfRole:
                    if remainingExpectedShareFromOverrides > 0:
                        expectedShareOfRole[person_id] = remainingExpectedShareFromOverrides * ratioOfRemainingShare[person_id] / totalRatioOfRemainingShare
                    else: # floor at 0, we can't ask the solver to give a negative number of slots
                        expectedShareOfRole[person_id] = 0
                
                # now we have the share, we can convert that into a slot count
                expectedSlotsForPersonInRole = expectedShareOfRole[person_id] * self.slotsPerRoleCounts[role_id]

                # we have to do this to create an abs value to minimise.  Basically we want the difference between
                # expectedSlotsForPersonInRole and the slots per role in the solution to be as small as possible.
                # To make the difference small we need to set the absolute value to be small, as without that a 
                # negative value would be better and better.  E.g. without abs if the target is 1 in 3, 1 in 7 
                # would be better than 1 in 4.  I imagine it would end up with one person being rota-d as much as
                # possible!
                possibilitiesForPersonInRole = model.data['possibilities']['byRoleAndPerson'][(role_id,person_id)]
                sumPossibilitiesForPersonInRole = sum(possibilitiesForPersonInRole) #this is an expression of what the sum would be when solved, not a number
                # setting up a new variable that tracks the absolute value of the difference
                absoluteDifference = model.model.NewIntVar(
                    0,
                    multiplier * len(possibilitiesForPersonInRole),
                    f"difference_from_expected__person_{person_id}__in_role_{role_id}"
                )
                # telling the model that the new variable should be the abs value of the difference.  Multiplier is because it needs to be an integer
                model.model.AddAbsEquality(
                    absoluteDifference,
                    int(multiplier * expectedSlotsForPersonInRole) - multiplier * sumPossibilitiesForPersonInRole # this is an expression not a number
                )

                toMinimise += absoluteDifference # this is an expression not a number

        model.toMinimise = toMinimise * self.weight


        
        