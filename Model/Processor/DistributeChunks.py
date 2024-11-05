from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class DistributeChunks(AbstractProcessor):
    weight: int
    def __init__(self, weight: int):
        self.weight = weight
    def process(self, model: Model):
        self.setSinceLastServedVars(model)
        self.minimiseGaps(model)
        

    def setSinceLastServedVars(self, model: Model):
        eventCount = len(model.rota.events)
        sinceLastServed = dict()
        prevDate = None
        for date, events in model.data['eventsByDate'].items():
            for person_id in model.people.keys():
                sinceLastServed[person_id, date] = model.model.NewIntVar(0, eventCount, f"time_since_last_served__person_{person_id}__date_{date[0]}-{date[1]}-{date[2]}")
                if prevDate == None:
                    model.model.Add(sinceLastServed[person_id, date] == 0)
                else:
                    model.model.Add(sinceLastServed[person_id, date] == 0).OnlyEnforceIf(model.data['personServedDate'][person_id, prevDate])
                    model.model.Add(sinceLastServed[person_id, date] == sinceLastServed[person_id, prevDate] + 1).OnlyEnforceIf(model.data['personServedDate'][person_id, prevDate].Not())
            prevDate = date
        model.data['sinceLastServed'] = sinceLastServed
    
    def minimiseGaps(self, model: Model):
        eventCount = len(model.rota.events)
        toMinimise = 0
        for person_id in model.people.keys():
            maxTimeSinceLastServed = model.model.NewIntVar(0, eventCount, f"max_time_since_last_served__person_{person_id}")
            model.model.AddMaxEquality(maxTimeSinceLastServed, (model.data['sinceLastServed'][person_id, date] for date in model.data['eventsByDate'].keys()))
            toMinimise += maxTimeSinceLastServed
        model.toMinimise += toMinimise * self.weight