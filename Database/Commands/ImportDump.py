import sqlite3
import csv
import os
import re
from Database.Commands.AbstractCommand import AbstractCommand

class ImportDump(AbstractCommand):
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
        return 'importDump'
    def getDesc(self) -> str:
        return 'Re-Import dumped csv files'
    def configure(self, parser):
        pass
    def execute(self, argparse):
        for table in self.tables:
            path = os.path.join('var','dump',f"{table}.csv")
            file = open(path, "r")
            columns = []
            typeLookup = dict()
            for (_, name, sqlType, _, _, _) in self.cursor.execute(f"PRAGMA table_info({table})").fetchall():
                columns.append(name)
                typeLookup[name] = sqlType
            data = self.cursor.execute(f"SELECT * FROM {table}").fetchall()
            data = [columns] + data
            reader = csv.reader(file, delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
            reader = list(reader)
            header = reader[0]
            reader = reader[1:]
            if( header != columns):
                print('header')
                print(header)
                print('columns')
                print(columns)
                self.connection.rollback()
                raise Exception("header and columns do not match") 

            rows = []
            for row in reader:
                for columnNumber in range(0, len(columns)):
                    colType = typeLookup[columns[columnNumber]]
                    if(colType == 'DATETIME'):
                        row[columnNumber] = self.convertDateTime(row[columnNumber])
                rows.append(tuple(row))
            placeholder = ('?,' * len(columns))[:-1]
            self.cursor.execute(f"DELETE FROM {table}")
            self.cursor.executemany(f"INSERT INTO {table} VALUES({placeholder})", rows)
            print(f"read {path}")
        self.connection.commit()
        print('success')

    def convertDateTime(self, date: str):
        matches = re.findall('(\d\d)/(\d\d)/(\d\d\d\d) (\d\d):(\d\d)',date)
        if not len(matches):
           return date
        for (day, month, year, hour, minute) in matches:
            return f"{year}-{month}-{day} {hour}:{minute}:00"

        