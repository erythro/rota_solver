from ortools.sat.python import cp_model
from Services.DataService import Rota, Event, Slot
from dataclasses import dataclass

@dataclass
class Model:
    model: cp_model
    rota: Rota
    people: dict
    roles: dict
    data: dict
    toMinimise = 0

class ModelFactory:
    processors: list
    def __init__(self, processors: list):
        self.processors = processors

    def create(self, rota: Rota, people:dict, roles: dict) -> Model:
        model = Model(cp_model.CpModel(), rota, people, roles, {})
        for processor in self.processors:
            processor.process(model)
        model.model.minimize(model.toMinimise)
        return model
        

        