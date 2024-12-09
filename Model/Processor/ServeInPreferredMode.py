from Services.DataService import DataService
from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class ServeInPreferredMode(AbstractProcessor):
    weight: int
    oncePerDate: list
    notEvenings: list
    notMornings: list
    preferNot1: list
    preferNot2: list
    preferBoth: list
    eitherMorningsOrEvening: list
    def __init__(self, dataService: DataService, weight: int):
        self.weight = weight
        self.oncePerDate = []
        self.notEvenings = []
        self.notMornings = []
        self.preferNot1 = []
        self.preferNot2 = []
        self.preferBoth = []
        self.eitherMorningsOrEvening = []
    def process(self, model: Model):
        for person_id, person in model.people.items():
            match person.preferredServingMode:
                case 'only_one_of_mornings':
                    self.oncePerDate.append(person_id)
                    self.notEvenings.append(person_id)
                case 'only_mornings':
                    self.notEvenings.append(person_id)
                case 'only_mornings_prefer_1':
                    self.preferNot2.append(person_id)
                    self.notEvenings.append(person_id)
                case 'only_mornings_prefer_2':
                    self.preferNot1.append(person_id)
                    self.notEvenings.append(person_id)
                case 'only_mornings_prefer_both':
                    self.preferBoth.append(person_id)
                    self.notEvenings.append(person_id)
                case 'only_evening':
                    self.notMornings.append(person_id)
                case 'only_one_of_date':
                    self.oncePerDate.append(person_id)
                case 'only_mornings_or_evening':
                    self.eitherMorningsOrEvening.append(person_id)
                case 'any':
                    pass #skip
        self.processAll(model)

    def processAll(self, model: Model):
        self.processOncePerDate(model)
        self.processNotEventType(model)
        self.processEventsOnDatePreferences(model)

    def processOncePerDate(self, model: Model):
        for [person_id, date], count in model.data['personServedDateCount'].items():
            if person_id not in self.oncePerDate:
                continue
            model.model.Add(count == 1)

    def processNotEventType(self, model: Model):
        for  [person_id, event_id], personIsServingThisEvent in model.data['personServedEvent'].items():
            personModeNotEvenings = person_id in self.notEvenings
            personModeNotMornings = person_id in self.notMornings

            if not personModeNotMornings and not personModeNotEvenings:
                continue #nothing to filter out, move on to next event/person entry

            if model.rota.events[event_id].type == 'evening': # this event is an evening
                if personModeNotEvenings: # the person will not serve it
                    model.model.Add(personIsServingThisEvent == 0) # don't serve it
                continue # move on to next event/person entry
            
            # this event is therefore a morning
            if personModeNotMornings:#the person will not serve it
                model.model.Add(personIsServingThisEvent == 0) # don't serve it
    
    def processEventsOnDatePreferences(self, model: Model):
        toMinimise = 0
        for date, events in model.data['eventsByDate'].items():
            mornings = list(filter(lambda event: event.event_type != 'evening',events))
            morning1s = list(filter(lambda event: event.event_type == 'morning_1',events))
            morning2s = list(filter(lambda event: event.event_type == 'morning_2',events))
            evenings = list(filter(lambda event: event.event_type == 'evening',events))

            #prefer not 1
            if len(morning1s) > 0 and len(self.preferNot1) > 0:
                toMinimise += self.preferNotEventsScore(morning1s, self.preferNot1, model)

            #prefer not 2
            if len(morning2s) > 0 and len(self.preferNot2) > 0:
                toMinimise += self.preferNotEventsScore(morning2s, self.preferNot2, model)

            #prefer both (or neither)
            if len(mornings) == 2:
                for person_id in self.preferBoth:
                    morningPossibilities = {model.data['possibilities']['byEventAndPerson'][(event_id, person_id)] for event_id in map(mornings, lambda event: event.id)}
                    # sum(morningPossibilities) can only be 0, 1, or 2, because they are either not serving, serving one, or serving both.
                    # the values 0 or 2 are preferred, 1 is not, so if we pick the expression:
                    # sum(morningPossibilities) * (2 - sum(morningPossibilities))
                    # it will in each of those cases be 0, 1, or 0, so asking the model to minimise this encourages the neither and
                    # both states, and punishes putting them down to serve one
                    toMinimise += self.weight * sum(morningPossibilities) * (2 - sum(morningPossibilities))

            #prefer either serving the evening or the morning but not both
            if len(mornings) > 0 and len(evenings) > 0 and len(self.eitherMorningsOrEvening):
                self.restrictEitherMorningsOrEvenings(mornings, evenings, self.eitherMorningsOrEvening, date, model)
        model.toMinimise += toMinimise

    #punish the model for selecting a person for one of the passed events
    def preferNotEventsScore(self, events: list, person_ids: list, model: Model):
        score = 0
        for person_id in person_ids:
            eventPossibilities = {model.data['possibilities']['byEventAndPerson'][(event_id, person_id)] for event_id in map(events, lambda event: event.id)}
            score += sum(eventPossibilities) * self.weight
        return score
    
    def restrictEitherMorningsOrEvenings(self, mornings: list, evenings: list, person_ids: list, date, model: Model):
        for person_id in person_ids:
            #are they serving in the morning
            morningPossibilities = []
            for event_id in map(lambda event: event.id, mornings):
                if (event_id, person_id) in model.data['possibilities']['byEventAndPerson']:
                    for morningPossibility in model.data['possibilities']['byEventAndPerson'][(event_id, person_id)]:
                        morningPossibilities.append(morningPossibility)

            #are they serving in the evening
            eveningPossibilities = []
            for event_id in map(lambda event: event.id, evenings):
                if (event_id, person_id) in model.data['possibilities']['byEventAndPerson']:
                    for eveningPossibility in model.data['possibilities']['byEventAndPerson'][(event_id, person_id)]:
                        eveningPossibilities.append(eveningPossibility)

            if len(morningPossibilities) > 0 and len(eveningPossibilities) > 0:
                servingInMorning = model.model.NewBoolVar(f"serving_in_morning_on_date__person_{person_id}__date_{date[0]}-{date[1]}-{date[2]}")
                model.model.AddMaxEquality(servingInMorning, morningPossibilities)
                servingInEvening = model.model.NewBoolVar(f"serving_in_evening_on_date__person_{person_id}__date_{date[0]}-{date[1]}-{date[2]}")
                model.model.AddMaxEquality(servingInEvening, eveningPossibilities)

                #they must not serve in both, the sum must be less than 2
                model.model.Add((servingInMorning + servingInEvening) < 2)
