import sqlite3

from Services.DataService import DataService
from Model.ModelFactory import ModelFactory
from ortools.sat.python import cp_model
from Model.Processor.ExactlyOnePersonInEachSlot import ExactlyOnePersonInEachSlot
from Model.Processor.PersonCanOnlyServeOncePerEvent import PersonCanOnlyServeOncePerEvent
from Model.Processor.ShareEqually import ShareEqually

connection = sqlite3.connect("var/data.db")
dataService = DataService(connection)

rota = dataService.getRota()
roles = dataService.getRoles()

modelFactory = ModelFactory([
    ExactlyOnePersonInEachSlot(),
    PersonCanOnlyServeOncePerEvent(),
    ShareEqually(dataService, 1),
])

model = modelFactory.create(
    rota,
    roles
)

# Creates the solver and solve.
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
solver.parameters.enumerate_all_solutions = True
# Enumerate all solutions.
result = solver.solve(model.model, cp_model.ObjectiveSolutionPrinter())

def exportSolution(connection, model, solver):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM solution')
    toInsert = []
    for (person_id, slot_id, event_id), possibility in model.possibilities.items():
        if solver.boolean_value(possibility):
            toInsert.append((event_id,slot_id,person_id))
    cursor.executemany("INSERT INTO solution VALUES(?, ?, ?)", toInsert)
    connection.commit()

if result == cp_model.MODEL_INVALID:
    print('Model Invalid')
elif result == cp_model.INFEASIBLE:
    print('No Solution Found')
elif result == cp_model.FEASIBLE:
    print('Feasible Solution Found')
    exportSolution(connection, model, solver)
elif result == cp_model.OPTIMAL:
    print('Optimal Solution Found')
    exportSolution(connection, model, solver)
else:
    print('Unknown result code')
connection.close()