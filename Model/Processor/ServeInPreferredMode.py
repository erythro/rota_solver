from Services.DataService import DataService
from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class ServeInPreferredMode(AbstractProcessor):
    weight: int
    preferredServingModes: dict
    oncePerDate: list
    notEvenings: list
    notMornings: list
    preferNot1: list
    preferNot2: list
    preferBoth: list
    eitherMorningsOrEvening: list
    def __init__(self, dataService: DataService, weight: int):
        self.weight = weight
        self.preferredServingModes = dataService.preferredServingModes()
        self.oncePerDate = []
        self.notEvenings = []
        self.notMornings = []
        self.preferNot1 = []
        self.preferNot2 = []
        self.preferBoth = []
        self.eitherMorningsOrEvening = []
    def process(self, model: Model):
        for person_id, preferredServingMode in self.preferredServingModes.items():
            match preferredServingMode:
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
                continue #nothing to filter out

            if model.rota.events[event_id].type == 'evening':
                if personModeNotEvenings:
                    model.model.Add(personIsServingThisEvent == 0)
                continue
            
            if personModeNotMornings:
                model.model.Add(personIsServingThisEvent == 0)
    
    def processEventsOnDatePreferences(self, model: Model):
        toMinimise = 0
        for date, events in model.data['eventsByDate'].items():
            mornings = list(filter(lambda event: event.event_type != 'evening',events))
            morning1s = list(filter(lambda event: event.event_type == 'morning_1',events))
            morning2s = list(filter(lambda event: event.event_type == 'morning_2',events))
            evenings = list(filter(lambda event: event.event_type == 'evening',events))

            
            if len(morning1s) > 0 and len(self.preferNot1) > 0:
                toMinimise += self.preferNotEventsScore(morning1s, self.preferNot1, model)

            if len(morning2s) > 0 and len(self.preferNot2) > 0:
                toMinimise += self.preferNotEventsScore(morning2s, self.preferNot2, model)

            if len(mornings) == 2:
                for person_id in preferBoth:
                    morningPossibilities = {model.data['byEventAndPerson'][(event_id, person_id)] for event_id in map(mornings, lambda event: event.id)}
                    # sum(morningPossibilities) can be 0, 1, or 2.  So sum(morningPossibilities) * (2 - sum(morningPossibilities)) will
                    # in each of those cases be 0, 1, or 0
                    toMinimise += self.weight * sum(morningPossibilities) * (2 - sum(morningPossibilities))

            if len(mornings) > 0 and len(evenings) > 0 and len(self.eitherMorningsOrEvening):
                self.restrictEitherMorningsOrEvenings(mornings, evenings, self.eitherMorningsOrEvening, date, model)


    def preferNotEventsScore(self, events: list, person_ids: list, model: Model):
        score = 0
        for person_id in person_ids:
            eventPossibilities = {model.data['byEventAndPerson'][(event_id, person_id)] for event_id in map(events, lambda event: event.id)}
            score += sum(eventPossibilities) * self.weight
        return score
    
    def restrictEitherMorningsOrEvening(self, mornings: list, evenings: list, person_ids: list, date, model: Model):
        for person_id in person_ids:
            morningPossibilities = {model.data['byEventAndPerson'][(event_id, person_id)] for event_id in map(mornings, lambda event: event.id)}
            servingInMorning = model.model.NewBoolVar(f"serving_in_morning_on_date__person_{person_id}__date_{date[0]}-{date[1]}-{date[2]}")
            model.model.AddMaxEquality(servingInMorning, morningPossibilities)

            eveningPossibilities = {model.data['byEventAndPerson'][(event_id, person_id)] for event_id in map(evenings, lambda event: event.id)}
            servingInEvening = model.model.NewBoolVar(f"serving_in_evening_on_date__person_{person_id}__date_{date[0]}-{date[1]}-{date[2]}")
            model.model.AddMaxEquality(servingInEvening, eveningPossibilities)

            model.model.Add((servingInMorning + servingInEvening) < 2)