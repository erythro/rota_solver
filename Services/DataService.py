from dataclasses import dataclass

@dataclass
class Rota:
    events = dict()

@dataclass
class Event:
    id: int
    name: str
    slots: dict

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
            rota.events[id] = Event(id, name, dict())

        #Load all slots for timeSlots
        result = self.cursor.execute('SELECT * FROM slot LEFT JOIN role ON slot.role_id = role.id')
        for [id, event_id, role_id, _, role_name] in result.fetchall():
            rota.events[event_id].slots[id] = Slot(id, event_id, role_id, role_name)
        return rota

    def getRoles(self) -> dict:
        roles = dict()
        result = self.cursor.execute('SELECT * FROM person_role LEFT JOIN role ON person_role.role_id = role.id')
        for [person_id, role_id, _, _, role_name] in result.fetchall():
            if role_id not in roles:
                roles[role_id] = Role(role_id, role_name, [])
            roles[role_id].person_ids.append(person_id)
        return roles
        
    def rolesPerPersonCounts(self) -> dict:
        roleCounts = dict()
        result = self.cursor.execute('SELECT person.id, COUNT(person_role.role_id) FROM person LEFT JOIN person_role ON person_role.person_id = person.id GROUP BY person.id')
        for [person_id, role_count] in result.fetchall():
            roleCounts[person_id] = role_count
        return roleCounts

    def slotsPerRoleCounts(self) -> dict:
        slotCounts = dict()
        result = self.cursor.execute('SELECT role.id, COUNT(slot.id) FROM role LEFT JOIN slot ON slot.role_id = role.id GROUP BY role.id')
        for [role_id, slot_count] in result.fetchall():
            slotCounts[role_id] = slot_count
        return slotCounts

    def expectedPeriods(self) -> dict:
        expectedPeriods = dict()
        result = self.cursor.execute('SELECT * FROM person_role')
        for [person_id, role_id, expected_period] in result.fetchall():
            if expected_period != None:
                expectedPeriods[(person_id, role_id)] = expected_period
        return expectedPeriods
    
    def averageRoleCountsPerEvent(self) -> dict:
        averageRoleCountsPerEvent = dict()
        result = self.cursor.execute('SELECT role_id, 1.0 * COUNT(id)/ COUNT(DISTINCT event_id) FROM slot GROUP BY role_id')
        for [role_id, averageRoleCountPerEvent] in result.fetchall():
            averageRoleCountsPerEvent[role_id] = averageRoleCountPerEvent
        return averageRoleCountsPerEvent