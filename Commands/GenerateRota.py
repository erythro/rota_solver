import sqlite3

import os
from Services.DataService import DataService
from ortools.sat.python import cp_model
from Model.ModelFactory import ModelFactory
from Model.Processor.AddPossibilities import AddPossibilities
from Model.Processor.CreateUserIsServingInEventVars import CreateUserIsServingInEventVars
from Model.Processor.CorrectNumberOfPeopleInEachSlot import CorrectNumberOfPeopleInEachSlot
from Model.Processor.PersonCanOnlyServeOncePerEvent import PersonCanOnlyServeOncePerEvent
from Model.Processor.ShareEqually import ShareEqually
from Model.Processor.ServeInPreferredMode import ServeInPreferredMode
from Model.Processor.DistributeChunks import DistributeChunks
from Model.Processor.PersonRelationships import PersonRelationships
from Model.Processor.DatePreferences import DatePreferences
from Model.Processor.PrefilledRota import PrefilledRota
from Services.ValidationService import ValidationService
from Commands.AbstractCommand import AbstractCommand

class GenerateRota(AbstractCommand):
    validator: ValidationService
    dataService: DataService
    connection = None
    def __init__(
        self,
        validator: ValidationService,
        dataService: DataService,
        connection
    ):
        self.validator = validator
        self.dataService = dataService
        self.connection = connection
    def getName(self) -> str:
        return 'generateRota'
    def getDesc(self) -> str:
        return 'Generates the rota from the database data'
    def configure(self, parser):
        pass
    def execute(self, args):
        self.validator.validate()

        (rota, slots) = self.dataService.getRotaAndSlots()
        people = self.dataService.getPeople()
        roles = self.dataService.getRoles()

        modelFactory = self.makeModelFactory()

        model = modelFactory.create(
            rota,
            slots,
            people,
            roles
        )

        # Creates the solver and solve.
        solver = cp_model.CpSolver()
        result = solver.solve(model.model, cp_model.ObjectiveSolutionPrinter())

        if result == cp_model.MODEL_INVALID:
            print('Model Invalid')
        elif result == cp_model.INFEASIBLE:
            print('No Solution Found')
        elif result == cp_model.FEASIBLE:
            print('Feasible Solution Found')
            self.exportSolution(model, solver)
        elif result == cp_model.OPTIMAL:
            print('Optimal Solution Found')
            self.exportSolution(model, solver)
        else:
            print('Unknown result code')
        self.connection.close()
    def makeModelFactory(self):
        return ModelFactory([
            #processing steps
            AddPossibilities(),
            CreateUserIsServingInEventVars(),
            CorrectNumberOfPeopleInEachSlot(),
            PersonCanOnlyServeOncePerEvent(),
            ShareEqually(self.dataService, int(os.environ.get('SHARE_EQUALLY_MULTIPLIER'))), #ones with an integer argument like this are weighted and can be tweaked
            ServeInPreferredMode(self.dataService, int(os.environ.get('SERVE_IN_PREFERRED_MODE_MULTIPLIER'))),
            DistributeChunks(int(os.environ.get('DISTRIBUTE_CHUNKS_MULTIPLIER'))),
            PersonRelationships(self.dataService, int(os.environ.get('PERSON_RELATIONSHIPS_MULTIPLIER'))),
            DatePreferences(self.dataService, int(os.environ.get('DATE_PREFERENCES_MULTIPLIER'))),
            PrefilledRota(self.dataService)
        ])
    def exportSolution(self, model, solver):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM solution')
        toInsert = []
        for (person_id, slot_id), possibility in model.data['possibilities']['all'].items():
            if solver.boolean_value(possibility):
                toInsert.append((slot_id,person_id))
        cursor.executemany("INSERT INTO solution VALUES(?, ?)", toInsert)
        self.connection.commit()