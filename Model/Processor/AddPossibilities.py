from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class AddPossibilities(AbstractProcessor):
    def process(self, model: Model):
        possibilities = {
            'all' : {},
            'byEventAndSlot': {},
            'byEventAndPerson': {},
            'byRoleAndPerson': {}
        }
        for id, event in model.rota.events.items():
            for id, slot in event.slots.items():
                for person_id in model.roles[slot.role_id].person_ids:
                    #each eligible person either serves for that slot for that event or not
                    possibility = model.model.new_bool_var(f"possibility__person_{person_id}__event_{slot.event_id}__slot_{slot.id}")
                    
                    #save to the model struct
                    possibilities['all'][(person_id, slot.id, slot.event_id)] = possibility

                    if (slot.event_id, slot.id) not in possibilities['byEventAndSlot']:
                        possibilities['byEventAndSlot'][(slot.event_id, slot.id)] = []

                    if (slot.event_id, person_id) not in possibilities['byEventAndPerson']:
                        possibilities['byEventAndPerson'][(slot.event_id, person_id)] = []

                    if (slot.role_id, person_id) not in possibilities['byRoleAndPerson']:
                        possibilities['byRoleAndPerson'][(slot.role_id, person_id)] = []

                    possibilities['byEventAndSlot'][(slot.event_id, slot.id)].append(possibility)
                    possibilities['byEventAndPerson'][(slot.event_id, person_id)].append(possibility)
                    possibilities['byRoleAndPerson'][(slot.role_id, person_id)].append(possibility)
        model.data['possibilities'] = possibilities