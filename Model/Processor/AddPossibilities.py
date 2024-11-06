from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class AddPossibilities(AbstractProcessor):
    def process(self, model: Model):
        possibilities = {
            'all' : {},
            'bySlot': {},
            'byEventAndPerson': {},
            'byRoleAndPerson': {}
        }
        for id, event in model.rota.events.items():
            for id, slot in event.slots.items():
                for person_id in model.roles[slot.role_id].person_ids:
                    #each eligible person either serves for that slot for that event or not
                    possibility = model.model.new_bool_var(f"possibility__person_{person_id}__event_{slot.event_id}__slot_{slot.id}")
                    
                    #save to the model struct
                    possibilities['all'][(person_id, slot.id)] = possibility

                    if slot.id not in possibilities['bySlot']:
                        possibilities['bySlot'][slot.id] = []

                    if (slot.event_id, person_id) not in possibilities['byEventAndPerson']:
                        possibilities['byEventAndPerson'][(slot.event_id, person_id)] = []

                    if (slot.role_id, person_id) not in possibilities['byRoleAndPerson']:
                        possibilities['byRoleAndPerson'][(slot.role_id, person_id)] = []

                    possibilities['bySlot'][slot.id].append(possibility)
                    possibilities['byEventAndPerson'][(slot.event_id, person_id)].append(possibility)
                    possibilities['byRoleAndPerson'][(slot.role_id, person_id)].append(possibility)
        model.data['possibilities'] = possibilities