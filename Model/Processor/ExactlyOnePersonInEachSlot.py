from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class ExactlyOnePersonInEachSlot(AbstractProcessor):
    def process(self, model: Model):
        for (event_id, slot_id), possibilities in model.possibilitiesByEventAndSlot.items():
            model.model.add_exactly_one(possibilities)