import os
import csv
from Commands.AbstractCommand import AbstractCommand

class ImportChurchSuite(AbstractCommand):
    expectedHeaders = ['Name', '', 'Details', 'Roles']
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
                    self.importRow(row, currentTeam)
                    pass


            if state == 'Team':
                currentTeam = row[0]
                state = 'Headers'
                continue
            
            if state == 'Headers':
                if row != self.expectedHeaders:
                    raise Exception(f"headers invalid, {row} - expected {self.expectedHeaders}")
                state = 'Data'
                continue

    def getFile(self, path):
        if not os.path.isfile(path):
            raise Exception(f"file {path} not found") 
        return open(path, "r")
    
    def importRow(self, row, team: str):
        role = self.resolveRoles(row[3].split(', '), team)

    def resolveRoles(self, roles: list, team: str):
        print(roles, team)