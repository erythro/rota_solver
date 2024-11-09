import sqlite3
import csv
import os
from Database.Commands.AbstractCommand import AbstractCommand

class Dump(AbstractCommand):
    connection = None
    cursor = None
    tables = [
		'person',
		'role',
		'event',
		'person_role',
		'slot',
		'solution',
		'person_person',
		'person_date_preference',
		'prefilled_rota',
	]
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
    def getName(self) -> str:
        return 'dump'
    def getDesc(self) -> str:
        return 'Dumps the entire database to csv files in the var/dump path'
    def configure(self, parser):
        pass
    def execute(self, argparse):
        for table in self.tables:
            path = os.path.join('var','dump',f"{table}.csv")
            # if os.path.isfile(path):
            #     print(f"file exists {path}")
            #     os.remove(path)
            file = open(path, "w")
            columns = []
            for (_, name, _, _, _, _) in self.cursor.execute(f"PRAGMA table_info({table})").fetchall():
                columns.append(name)
            data = self.cursor.execute(f"SELECT * FROM {table}").fetchall()
            data = [columns] + data
            writer = csv.writer(file, delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
            for row in data:
                writer.writerow(row)
            print(f"dumped {path}")
        print('success')

        