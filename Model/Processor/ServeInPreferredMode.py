from Services.DataService import DataService
from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class ServeInPreferredMode(AbstractProcessor):
    weight: int
    preferredServingModes: dict
    oncePerDate: list
    notEvenings: list
    notMornings: list
    eitherMorningsOrEvening: list
    def __init__(self, dataService: DataService, weight: int):
        self.weight = weight
        self.preferredServingModes = dataService.preferredServingModes()
        self.oncePerDate = []
        self.notEvenings = []
        self.notMornings = []
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
                    #todo
                    self.notEvenings.append(person_id)
                case 'only_mornings_prefer_2':
                    #todo
                    self.notEvenings.append(person_id)
                case 'only_mornings_prefer_both':
                    #todo
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
        self.processEitherMorningsOrEvening(model)

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
    
    def processEitherMorningsOrEvening(self, model: Model):
        for date, events in model.data['eventsByDate'].items():
            mornings = list(filter(lambda event: event.event_type != 'evening',events))
            evenings = list(filter(lambda event: event.event_type == 'evening',events))
            if len(mornings) == 0 or len(evenings) == 0:
                continue

            for person_id in eitherMorningsOrEvening:
                morningPossibilities = {model.data['byEventAndPerson'][(event_id, person_id)] for event_id in map(mornings, lambda event: event.id)}
                servingInMorning = model.model.NewBoolVar(f"serving_in_morning_on_date__person_{person_id}__date_{date[0]}-{date[1]}-{date[2]}")
                model.model.AddMaxEquality(servingInMorning, morningPossibilities)

                eveningPossibilities = {model.data['byEventAndPerson'][(event_id, person_id)] for event_id in map(evenings, lambda event: event.id)}
                servingInEvening = model.model.NewBoolVar(f"serving_in_evening_on_date__person_{person_id}__date_{date[0]}-{date[1]}-{date[2]}")
                model.model.AddMaxEquality(servingInEvening, eveningPossibilities)

                model.model.Add((servingInMorning + servingInEvening) < 2)