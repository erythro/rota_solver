from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class CreateUserIsServingInEventVars(AbstractProcessor):
    def process(self, model: Model):
        personServedEvent = {}
        personServedDate = {}
        personServedDateCount = {}
        eventsByDate = {}
        
        for [person_id, slot_id, event_id], possibility in model.data['possibilities']['all'].items():
            event = model.rota.events[event_id]
            date = (event.date.year, event.date.month, event.date.day)
            if (person_id,date) not in personServedDate:
                personServedDate[(person_id,date)] = []
                personServedDateCount[(person_id,date)] = []
            if (person_id,event_id) not in personServedEvent:
                personServedEvent[(person_id,event_id)] = []
            personServedDate[(person_id,date)].append(possibility)
            personServedEvent[(person_id,event_id)].append(possibility)

        for (person_id,date), possibilities in personServedDate.items():
            personServedDate[(person_id,date)] = model.model.NewBoolVar(f"worked_on_date__person_{person_id}__date_{date[0]}-{date[1]}-{date[2]}")
            model.model.AddMaxEquality(personServedDate[(person_id,date)], possibilities)
            
            personServedDateCount[(person_id,date)] = model.model.NewIntVar(0, 3, f"worked_count_on_date__person_{person_id}__date_{date[0]}-{date[1]}-{date[2]}")
            model.model.Add(personServedDateCount[(person_id,date)] == sum(possibilities))

        for (person_id,event_id), possibilities in personServedEvent.items():
            personServedEvent[(person_id,event_id)] = model.model.NewBoolVar(f"worked_on_event__person_{person_id}__event_{event_id}")
            model.model.AddMaxEquality(personServedEvent[(person_id,event_id)], possibilities)
        
        for event in model.rota.events.values():
            date = (event.date.year, event.date.month, event.date.day)
            if date not in eventsByDate:
                eventsByDate[date] = []
            eventsByDate[date].append(event)
        model.data['personServedDate'] = personServedDate
        model.data['personServedDateCount'] = personServedDateCount
        model.data['personServedEvent'] = personServedEvent
        model.data['eventsByDate'] = eventsByDate


