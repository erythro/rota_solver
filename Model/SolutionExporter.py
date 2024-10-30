from ortools.sat.python import cp_model
from Model.ModelFactory import Model

class SolutionExporter(cp_model.CpSolverSolutionCallback):
    model: Model = None
    connection = None
    cursor = None

    def __init__(self, model: Model, connection):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.model = model
        self.connection = connection
        self.cursor = connection.cursor()
    
    def on_solution_callback(self):
        self.cursor.execute('DELETE FROM solution')
        toInsert = []
        for (person_id, slot_id, event_id), possibility in self.model.possibilities.items():
            if self.value(possibility):
                toInsert.append((event_id,slot_id,person_id))
        self.cursor.executemany("INSERT INTO solution VALUES(?, ?, ?)", toInsert)
        self.connection.commit()  
        self.stop_search()