from ortools.sat.python import cp_model
from Services.DataService import Rota
from dataclasses import dataclass


@dataclass
class Model:
    model: cp_model
    possibilities = {}

class ModelFactory:
    def create(self, rota: Rota, roles: dict) -> Model:
        model = Model(cp_model.CpModel())

        model.possibilities = {}
        for id, event in rota.events.items():
            eventPersonPossibilities = {}
            for id, slot in event.slots.items():
                slotPossibilities = []
                for person_id in roles[slot.role_id].person_ids:
                    #each eligible person either serves for that slot for that event or not
                    possibility = model.model.new_bool_var(f"possibility__person_{person_id}__event_{event.id}__slot_{slot.id}")
                    
                    #save to the model struct
                    model.possibilities[(person_id, slot.id, event.id)] = possibility
                    
                    #record all possibilties for this slot, as we only want one of these to actually happen
                    slotPossibilities.append(possibility)

                    #(intitialise)
                    if person_id not in eventPersonPossibilities:
                        eventPersonPossibilities[person_id] = []
                    
                    #record all possibilities for a person this event, as they can only serve in one way
                    eventPersonPossibilities[person_id].append(possibility)
                model.model.add_exactly_one(slotPossibilities)
            for id, personPossibilities in eventPersonPossibilities.items():
                model.model.add_at_most_one(personPossibilities)
        return model

        

        