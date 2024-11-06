from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class ExactlyOnePersonInEachSlot(AbstractProcessor):
    def process(self, model: Model):
        for slot_id, possibilities in model.data['possibilities']['bySlot'].items():
            model.model.add_exactly_one(possibilities)