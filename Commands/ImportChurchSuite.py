import os
import csv
from Commands.AbstractCommand import AbstractCommand
from Services.DataService import DataService, Role, Person

class ImportChurchSuite(AbstractCommand):
    expectedHeaders = ['Name', '', 'Details', 'Roles']
    dataService: DataService
    skipRoles: list
    roles: dict
    roleMap: dict
    def __init__(self,dataService: DataService):
        self.dataService = dataService
        self.skipPeople = []
        self.people = self.dataService.getPeople()
        self.skipRoles = []
        self.roles = dict()
        for (id, name) in self.dataService.query('SELECT * FROM role'):
            self.roles[id] = Role(id, name, [])
        self.roleMap = dict()
        for role in self.roles.values():
            self.roleMap[role.role_name] = role
            
    def getName(self) -> str:
        return 'importChurchSuite'

    def getDesc(self) -> str:
        return 'attempt to import people and (optionally) roles from the church suite csv export'

    def configure(self, parser):
        parser.add_argument('path', help='path to church suite export file')
        parser.add_argument('--roles', action='store_true', help='import roles as well')

    def execute(self, args):
        file = self.getFile(args.path)
        reader = csv.reader(file, delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
        state = 'Team'
        currentTeam = None
        for row in reader:
            if state == 'Data':
                if row[3] == '':
                    state = 'Team'
                else:
                    if importCurrentTeam:
                        self.importRow(row, currentTeam)
                    continue


            if state == 'Team':
                currentTeam = row[0]
                importCurrentTeam = self.askYNQuestion(f"Do you want to import {currentTeam}?")
                state = 'Headers'
                continue
            
            if state == 'Headers':
                if row != self.expectedHeaders:
                    raise Exception(f"headers invalid, {row} - expected {self.expectedHeaders}")
                state = 'Data'
                continue
        self.dataService.connection.commit()

    def getFile(self, path):
        if not os.path.isfile(path):
            raise Exception(f"file {path} not found") 
        return open(path, "r")
    
    def importRow(self, row, team: str):
        (name, contactType, contactDetails, roleString) = row
        person = self.resolvePerson(name, contactType, contactDetails)
        if person == None:
            return
        roles = self.resolveRoles(roleString.split(', '), team)
        self.createPersonRoles(person, roles)

    def askYNQuestion(self, question: str) -> bool:
        while True:
            response = input(question + ' [y/n] (default n)')
            if response in ['yes', 'y']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Invalid input")
    
    def askMultipleChoiceQuestion(self, question: str, choices: list):
        print(f"{question}\n")
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")
        
        while True:
            try:
                answer = int(input(f"Please choose a number (1-{len(choices)}): "))
                
                if 1 <= answer <= len(choices):
                    print(f"You selected: {choices[answer - 1]}")
                    return choices[answer - 1]
                else:
                    print(f"Invalid choice. Please choose a number between 1 and {len(choices)}.")
            
            except ValueError:
                print("Invalid input. Please enter a number.")

    def resolveRoles(self, roles: list, team: str) -> list:
        resolved = []
        for role in roles:
            name = team
            if role != 'No role':
                name += ' - ' + role

            if name in self.roleMap.keys():
                resolved.append(self.roleMap[name])
                continue

            if name in self.skipRoles:
                print(f"Skipping role {name}")
                continue

            id = self.dataService.getRoleIdByName(name)
            if id == None:
                print(f"Role {name} not found.")
                match self.askMultipleChoiceQuestion('How should we proceed?',['Map to existing role', 'Create from name', 'Skip this role in this import']):
                    case 'Map to existing role':
                        id = self.mapToExistingRole(name)
                    case 'Create from name':
                        id = self.createRoleFromName(name)
                    case 'Skip this role in this import':
                        self.skipRoles.append(name)
                        continue
            print(self.roles)
            resolved.append(self.roles[id])
        return resolved

    def createRoleFromName(self, name: str) -> int:
        self.dataService.query('INSERT INTO role VALUES (?, ?)',[None,name])
        id = self.dataService.cursor.lastrowid
        role = Role(id, name, [])
        self.roles[id] = role
        self.roleMap[name] = role
        return role.id
    
    def mapToExistingRole(self, name: str) -> int:
        choice = self.askMultipleChoiceQuestion('Which role?',list(map(lambda role: role.role_name,self.roles.values())))
        role = list(filter(lambda role: role.role_name == choice,self.roles.values()))[0]
        self.roleMap[name] = role
        return role.id
    
    def resolvePerson(self, name, contactType, contactDetails) -> Person|None:
        [firstName, lastName] = name.split(' ',maxsplit=1)
        email = contactDetails.split('\n')[0]
        person = self.findPerson(firstName, lastName, email)
        if person != None:
            return person
        if (firstName,lastName,email) in self.skipPeople:
            return None

        print(f"person {firstName}, {lastName}, {email} not found")
        match self.askMultipleChoiceQuestion('How should we proceed?',['Update another person', 'Create', 'Skip this person in this import']):
            case 'Update another person':
                people = self.findSimilarPeople(firstName, lastName, email, 10)
                options = list(map(lambda person: f"{person.id} {person.firstName} {person.lastName} {person.email}", people))
                choice = self.askMultipleChoiceQuestion('Which person?',options)
                [id,_] = choice.split(' ',maxsplit=1)
                id = int(id)
                self.updatePerson(id, firstName, lastName, email)
                return self.people[id]
            case 'Create':
                return self.createPerson(firstName, lastName, email)
            case 'Skip this person in this import':
                self.skipPeople.append((firstName,lastName,email))
                return None

    def findPerson(self, firstName, lastName, email) -> None|Person:
        result = self.dataService.query('SELECT id, preferred_serving_mode FROM person WHERE firstName = ? AND lastName = ? and email = ?',[firstName, lastName, email])
        if len(result) == 0:
            return None
        [[id,preferredServingMode]] = result
        return Person(id, firstName, lastName, preferredServingMode, email)

    def findSimilarPeople(self, firstName:str, lastName:str, email:str, limit:int) -> list:
        query = """
            SELECT *
            FROM person
            ORDER BY
                (CASE WHEN email IS ? THEN 0 ELSE 1 END),
                (CASE WHEN lastName IS ? THEN 0 ELSE 1 END),
                (CASE WHEN firstName IS ? THEN 0 ELSE 1 END)
            LIMIT ?
        """
        people = []
        for [id, first_name, last_name, preferred_serving_mode, email] in self.dataService.query(query, [email, lastName, firstName, limit]):
            people.append(Person(id, first_name, last_name, preferred_serving_mode, email))
        return people

    def createPerson(self, firstName:str, lastName:str, email:str) -> Person:
        self.dataService.query('INSERT INTO person VALUES (?, ?, ?, ?, ?)',[None, firstName, lastName, 'only_mornings_or_evening', email])
        id = self.dataService.cursor.lastrowid
        person = Person(id, firstName, lastName, 'only_mornings_or_evening', email)
        self.people[id] = person
        return person

    def updatePerson(self, id:int, firstName:str, lastName:str, email:str):
        person = self.people[id]
        person.firstName = firstName
        person.lastName = lastName
        person.email = email
        self.dataService.query('UPDATE person SET firstName=?, lastName=?, email=? WHERE id = ?',[firstName, lastName, email, id])

    def createPersonRoles(self, person: Person, roles: list):
        for role in roles:
            [[count]] = self.dataService.query('SELECT COUNT(*) FROM person_role WHERE person_id = ? AND role_id = ?',[person.id, role.id])
            if count > 0:
                return
            self.dataService.query('INSERT INTO person_role VALUES (?, ?, ?)',[person.id, role.id, None])
