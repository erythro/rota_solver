from Services.DataService import DataService
from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class PrefilledRota(AbstractProcessor):
    prefilledRota: list
    def __init__(self, dataService: DataService):
        self.prefilledRota = dataService.getPrefilledRota()
    def process(self, model: Model):
        for(slot_id,person_id) in self.prefilledRota:
            if person_id == None:
                slotPossibilities = sum(model.data['possibilities']['bySlot'][slot_id])
                model.model.Add(slotPossibilities == 0)
            else:
                possibility = model.data['possibilities']['all'][(person_id,slot_id)]
                model.model.Add(possibility == 1)