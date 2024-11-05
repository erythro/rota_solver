from dataclasses import dataclass
import datetime

@dataclass
class Rota:
    events = dict()

@dataclass
class Event:
    id: int
    name: str
    date: datetime.datetime
    event_type: str
    slots: dict
    prev_id: int|None
    next_id: int|None

@dataclass
class Slot:
    id: int
    event_id: int
    role_id: int
    role_name: str

@dataclass
class Role:
    id: int
    role_name: str
    person_ids: list

@dataclass
class Person:
    id: int
    firstName: str
    lastName: str
    preferredServingMode: str

class DataService:
    connection = None
    cursor = None

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def query(self, query: str):
        return self.cursor.execute(query).fetchall()
        

    def getRota(self) -> Rota:
        rota = Rota()

        #Load all events (e.g. services)
        prev_id = None
        for [id, name, date, event_type] in self.query('SELECT * FROM event ORDER BY date_time ASC'):
            rota.events[id] = Event(id, name, datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S'), event_type, dict(), prev_id, None)
            if prev_id != None:
                rota.events[prev_id].next_id = id
            prev_id = id

        #Load all slots for timeSlots
        for [id, event_id, role_id, _, role_name] in self.query('SELECT * FROM slot LEFT JOIN role ON slot.role_id = role.id'):
            rota.events[event_id].slots[id] = Slot(id, event_id, role_id, role_name)
        return rota

    def getPeople(self) -> dict:
        people = dict()
        for [id, first_name, last_name, preferred_serving_mode] in self.query('SELECT * FROM person'):
            people[id] = Person(id, first_name, last_name, preferred_serving_mode)
        return people

    def getRoles(self) -> dict:
        roles = dict()
        for [person_id, role_id, _, _, role_name] in self.query('SELECT * FROM person_role LEFT JOIN role ON person_role.role_id = role.id'):
            if role_id not in roles:
                roles[role_id] = Role(role_id, role_name, [])
            roles[role_id].person_ids.append(person_id)
        return roles
        
    def rolesPerPersonCounts(self) -> dict:
        roleCounts = dict()
        for [person_id, role_count] in self.query('SELECT person.id, COUNT(person_role.role_id) FROM person LEFT JOIN person_role ON person_role.person_id = person.id GROUP BY person.id'):
            roleCounts[person_id] = role_count
        return roleCounts

    def slotsPerRoleCounts(self) -> dict:
        slotCounts = dict()
        for [role_id, slot_count] in self.query('SELECT role.id, COUNT(slot.id) FROM role LEFT JOIN slot ON slot.role_id = role.id GROUP BY role.id'):
            slotCounts[role_id] = slot_count
        return slotCounts

    def onOneInXEvents(self) -> dict:
        onOneInXEvents = dict()
        for [person_id, role_id, on_one_in_x_events] in self.query('SELECT * FROM person_role'):
            if on_one_in_x_events != None:
                onOneInXEvents[(person_id, role_id)] = on_one_in_x_events
        return onOneInXEvents
    
    def averageRoleCountsPerEvent(self) -> dict:
        averageRoleCountsPerEvent = dict()
        for [role_id, averageRoleCountPerEvent] in self.query('SELECT role_id, 1.0 * COUNT(id)/ COUNT(DISTINCT event_id) FROM slot GROUP BY role_id'):
            averageRoleCountsPerEvent[role_id] = averageRoleCountPerEvent
        return averageRoleCountsPerEvent

    def getRelationships(self) -> dict:
        return self.query('SELECT * FROM person_person')