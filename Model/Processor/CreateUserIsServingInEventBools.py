from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class CreateUserIsServingInEventBools(AbstractProcessor):
    def process(self, model: Model):
        personServedEvent = {}
        personServedDate = {}
        
        for [person_id, slot_id, event_id], possibility in model.data['possibilities']['all'].items():
            event = model.rota.events[event_id]
            date = (event.date.year, event.date.month, event.date.day)
            if (person_id,date) not in personServedDate:
                personServedDate[(person_id,date)] = []
            if (person_id,event_id) not in personServedEvent:
                personServedEvent[(person_id,event_id)] = []
            personServedDate[(person_id,date)].append(possibility)
            personServedEvent[(person_id,event_id)].append(possibility)

        for (person_id,date), possibilities in personServedDate.items():
            personServedDate[(person_id,date)] = model.model.NewBoolVar(f"worked_on_date__person_{person_id}__date_{date[0]}-{date[1]}-{date[2]}")
            model.model.AddMaxEquality(personServedDate[(person_id,date)], possibilities)

        for (person_id,event_id), possibilities in personServedEvent.items():
            personServedEvent[(person_id,event_id)] = model.model.NewBoolVar(f"worked_on_event__person_{person_id}__event_{event_id}")
            model.model.AddMaxEquality(personServedEvent[(person_id,event_id)], possibilities)

        model.data['personServedDate'] = personServedDate
        model.data['personServedEvent'] = personServedEvent


