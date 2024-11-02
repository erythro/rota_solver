from Services.DataService import DataService

class Validator:
    dataService: DataService
    def __init__(self, dataService: DataService):
        self.dataService = dataService
        return
    def validate(self):
        self.noNullEventDate()
        return
    def noNullEventDate(self):
        [[count]] = self.dataService.query('SELECT COUNT(id) FROM event WHERE date_time IS NULL')
        if count != 0:
            raise Exception('validation error, all events should have dates')