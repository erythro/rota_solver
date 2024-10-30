from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class PersonCanOnlyServeOncePerEvent(AbstractProcessor):
    def process(self, model: Model):
        for (event_id, person_id), possibilities in model.possibilitiesByEventAndPerson.items():
            model.model.add_at_most_one(possibilities)
