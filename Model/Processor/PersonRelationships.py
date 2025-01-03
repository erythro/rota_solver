from Services.DataService import DataService
from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor

class PersonRelationships(AbstractProcessor):
    relationships: list
    weight: int
    possibilityLookup: dict
    def __init__(self, dataService: DataService, weight: int):
        self.relationships = dataService.getRelationships()
        self.weight = weight
    def process(self, model: Model):
        toMinimise = 0
        for from_id, to_id, relationship_type in self.relationships:
            match relationship_type:
                case 'serve_same_event':
                    toMinimise += self.weight * self.getAbsDiff(from_id, to_id, 'event', model)
                case 'serve_same_date':
                    toMinimise += self.weight * self.getAbsDiff(from_id, to_id, 'date', model)
                case 'serve_different_event':
                    toMinimise += self.weight * (len(model.rota.events.keys()) - self.getAbsDiff(from_id, to_id, 'event', model))
                case 'serve_different_date':
                    toMinimise += self.weight * (len(model.data['eventsByDate'].keys()) - self.getAbsDiff(from_id, to_id, 'date', model))
        model.toMinimise += toMinimise

    # this function gets the sum of the differences in the booleans for whether the person served an event or a date
    # so e.g. if the person served the exact same dates as another, this will be be 0, if the person served completely
    # different dates this will be equal to the number of dates.
    def getAbsDiff(self, from_id: int, to_id: int, possiblityType: str, model: Model):
        differences = []
        if possiblityType == 'event':
            for event_id in model.rota.events.keys():
                difference = model.model.NewBoolVar(
                    f"difference_between_people_for_events__person_from_{from_id}__person_to_{to_id}__event_{event_id}"
                )
                #this will be 1 if they didn't work on the same event, and 0 if they did
                model.model.AddAbsEquality(
                    difference,
                    sum(model.data['possibilities']['byEventAndPerson'][(event_id,from_id)]) - sum(model.data['possibilities']['byEventAndPerson'][(event_id,to_id)])
                )
                differences.append(difference)
            return sum(differences)

        for date in model.data['eventsByDate'].keys():
            difference = model.model.NewBoolVar(
                f"difference_between_people_for_date__person_from_{from_id}__person_to_{to_id}__date_{date[0]}-{date[1]}-{date[2]}"
            )
            #this will be 1 if they didn't work on the same date, and 0 if they did
            model.model.AddAbsEquality(
                difference,
                model.data['personServedDate'][(from_id, date)] - model.data['personServedDate'][(to_id, date)]
            )
            differences.append(difference)
        return sum(differences)
