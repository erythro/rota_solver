from dataclasses import dataclass

@dataclass
class Rota:
    events = dict()

@dataclass
class Event:
    id: int
    name: str
    slots = dict()

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
    person_ids = []

class DataService:
    connection = None
    cursor = None

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def getRota(self) -> Rota:
        rota = Rota()

        #Load all events (e.g. services)
        result = self.cursor.execute('SELECT * FROM event')
        for [id, name] in result.fetchall():
            rota.events[id] = Event(id, name)

        #Load all slots for timeSlots
        result = self.cursor.execute('SELECT * FROM slot LEFT JOIN role ON slot.role_id = role.id')
        for [id, event_id, role_id, _, role_name] in result.fetchall():
            rota.events[event_id].slots[id] = Slot(id, event_id, role_id, role_name)
        return rota

    def getRoles(self) -> dict:
        roles = dict()
        result = self.cursor.execute('SELECT * FROM person_role LEFT JOIN role ON person_role.role_id = role.id')
        for [person_id, role_id, _, role_name] in result.fetchall():
            if role_id not in roles:
                roles[role_id] = Role(role_id, role_name)
            roles[role_id].person_ids.append(person_id)
        return roles
        