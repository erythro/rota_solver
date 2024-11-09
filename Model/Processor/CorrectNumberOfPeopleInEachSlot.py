from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class CorrectNumberOfPeopleInEachSlot(AbstractProcessor):
    def process(self, model: Model):
        for slot_id, possibilities in model.data['possibilities']['bySlot'].items():
            if model.slots[slot_id].optional:
                model.model.add_at_most_one(possibilities)
            else:
                model.model.add_exactly_one(possibilities)