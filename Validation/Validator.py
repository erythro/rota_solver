from Services.DataService import DataService

class Validator:
    dataService: DataService
    validTypes = ['morning_1','morning_2','evening']
    def __init__(self, dataService: DataService):
        self.dataService = dataService
        return
    def validate(self):
        self.noNullEventDate()
        self.eventTypes()
        return
    def noNullEventDate(self):
        [[count]] = self.dataService.query('SELECT COUNT(id) FROM event WHERE date_time IS NULL')
        if count != 0:
            raise Exception('validation error, all events should have dates')
    def eventTypes(self):
        types = "'" + "','".join(self.validTypes) + "'"
        [[count]] = self.dataService.query(f"SELECT COUNT(id) FROM event WHERE type NOT IN ({types})")
        if count != 0:
            raise Exception(f"validation error, event type must be in list: {types}")