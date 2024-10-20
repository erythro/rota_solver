import sqlite3

from Services.DataService import DataService
from Model.ModelFactory import ModelFactory
from Model.SolutionExporter import SolutionExporter
from ortools.sat.python import cp_model

connection = sqlite3.connect("var/data.db")
dataService = DataService(connection)

rota = dataService.getRota()
roles = dataService.getRoles()
#constraints = dataService.getConstraints() #todo

modelFactory = ModelFactory()

model = modelFactory.create(
    rota,
    roles,
    #constraints #todo
)

solution_exporter = SolutionExporter(
    model, connection
)

# Creates the solver and solve.
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
# Enumerate all solutions.
solver.parameters.enumerate_all_solutions = True
solver.solve(model.model, solution_exporter)