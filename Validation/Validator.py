from Services.DataService import DataService

class Validator:
    dataService: DataService
    validTypes = [
        'morning_1',
        'morning_2',
        'evening'
    ]
    validServingModes = [
        'only_one_of_mornings',
        'only_mornings',
        'only_mornings_prefer_1',
        'only_mornings_prefer_2',
        'only_mornings_prefer_both',
        'only_evening',
        'only_one_of_date',
        'only_mornings_or_evening',
        'any'
    ]
    validRelationships = [
        'serve_same_event',
        'serve_same_date',
        'serve_different_event',
        'serve_different_date'
    ]
    validDatePreferences = [
        'not_serve',
        'prefer_serve'
    ]
    def __init__(self, dataService: DataService):
        self.dataService = dataService
        return
    def validate(self):
        self.noNullEventDate()
        self.eventTypes()
        self.personServingModes()
        self.personPersonRelationships()
        self.personDatePreferences()
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
    def personServingModes(self):
        modes = "'" + "','".join(self.validServingModes) + "'"
        [[count]] = self.dataService.query(f"SELECT COUNT(id) FROM person WHERE preferred_serving_mode NOT IN ({modes})")
        if count != 0:
            raise Exception(f"validation error, person preferred_serving_mode must be in list: {modes}")
    def personPersonRelationships(self):
        relationships = "'" + "','".join(self.validRelationships) + "'"
        [[count]] = self.dataService.query(f"SELECT COUNT(*) FROM person_person WHERE relationship_type NOT IN ({relationships})")
        if count != 0:
            raise Exception(f"validation error, person relationship_type must be in list: {relationships}")
    def personDatePreferences(self):
        preferences = "'" + "','".join(self.validDatePreferences) + "'"
        [[count]] = self.dataService.query(f"SELECT COUNT(*) FROM person_date_preference WHERE preference_type NOT IN ({preferences})")
        if count != 0:
            raise Exception(f"validation error, person_date preference_type must be in list: {preferences}")