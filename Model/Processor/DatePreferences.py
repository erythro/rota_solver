from Services.DataService import DataService
from Model.ModelFactory import Model
from Model.Processor.AbstractProcessor import AbstractProcessor
import datetime

class DatePreferences(AbstractProcessor):
    weight: int
    preferences: dict
    def __init__(self, dataService: DataService, weight: int):
        self.preferences = dataService.getPersonDatePreferences()
        self.weight = weight
    def process(self, model: Model):
        for (person_id, dateString, preference) in self.preferences:
            date = datetime.datetime.strptime(dateString,'%Y-%m-%d')
            date = (date.year, date.month, date.day)
            servingOnDate = model.data['personServedDateCount'][(person_id, date)]
            match(preference):
                case 'not_serve':
                    model.model.Add(servingOnDate == 0)
                case 'prefer_serve':
                    model.toMinimise += (1 - servingOnDate) * self.weight