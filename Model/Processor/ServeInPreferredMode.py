from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class ServeInPreferredMode(AbstractProcessor):
    preferredServingModes: dict
    onlyOneOfMornings: list
    def __init__(self, dataService: DataService, weight: int):
        self.preferredServingModes = dataService.preferredServingModes()
        self.oncePerDate = []
        self.notEvenings = []
        self.notMornings = []
    def process(self, model: Model):
        for person_id, preferredServingMode in self.preferredServingModes
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
                    #todo
                case 'any':
                    #skip
        self.processAll(model)

    def processAll(self, model: Model):
        self.processOncePerDate(model)
        self.processNotEventType(model)

    def processOncePerDate(self, model: Model):
        for [person_id, date], count in model.data['personServedDateCount'].items():
            if person_id not in self.oncePerDate
                continue
            model.model.Add(count == 1)

    def processNotEventType(self, model: Model):
        for  [person_id, event_id], personIsServingThisEvent in model.data['personServedEvent'].items():
            personModeNotEvenings = person_id in self.notEvenings
            personModeNotMornings = person_id in self.notMornings
            
            if not personModeNotMornings and not personModeNotEvenings 
                continue #nothing to filter out

            if model.rota.events[event_id].type == 'evening'
                if personModeNotEvenings
                    model.model.Add(personIsServingThisEvent == 0)
                continue
            
            if personModeNotMornings 
                model.model.Add(personIsServingThisEvent == 0)
            