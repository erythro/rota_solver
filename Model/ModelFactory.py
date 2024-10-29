from ortools.sat.python import cp_model
from Services.DataService import Rota, Event, Slot
from dataclasses import dataclass

@dataclass
class Model:
    model: cp_model
    rota: Rota
    roles: dict
    possibilities = {}
    possibilitiesByEventAndSlot = {}
    possibliitiesByEventAndPerson = {}

class ModelFactory:
    processors: list
    def __init__(self, processors: list):
        self.processors = processors

    def create(self, rota: Rota, roles: dict) -> Model:
        model = Model(cp_model.CpModel(), rota, roles)
        self.addPossibilities(model)
        for processor in self.processors:
            processor.process(model)
        return model

    def addPossibilities(self, model: Model):
        model.possibilities = {}
        for id, event in model.rota.events.items():
            for id, slot in event.slots.items():
                for person_id in model.roles[slot.role_id].person_ids:
                    #each eligible person either serves for that slot for that event or not
                    possibility = model.model.new_bool_var(f"possibility__person_{person_id}__event_{slot.event_id}__slot_{slot.id}")
                    
                    #save to the model struct
                    model.possibilities[(person_id, slot.id, slot.event_id)] = possibility

                    if (slot.event_id, slot.id) not in model.possibilitiesByEventAndSlot:
                        model.possibilitiesByEventAndSlot[(slot.event_id, slot.id)] = []


                    if (slot.event_id, person_id) not in model.possibliitiesByEventAndPerson:
                        model.possibliitiesByEventAndPerson[(slot.event_id, person_id)] = []

                    model.possibilitiesByEventAndSlot[(slot.event_id, slot.id)].append(possibility)
                    model.possibliitiesByEventAndPerson[(slot.event_id, person_id)].append(possibility)
        

        