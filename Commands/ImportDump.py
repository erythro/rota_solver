import sqlite3
import csv
import os
import re
from Commands.AbstractCommand import AbstractCommand

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
            (columns, rows) = self.getFormattedDataFromFile(table)
            placeholder = ('?,' * len(columns))[:-1]
            self.cursor.execute(f"DELETE FROM {table}")
            self.cursor.executemany(f"INSERT INTO {table} VALUES({placeholder})", rows)
            print(f"read {table}")
        self.connection.commit()
        self.connection.close()
        print('success')

    def tableToPath(self,table:str) -> str:
        return os.path.join('var','dump',f"{table}.csv")

    def convertDateTime(self, date: str):
        matches = re.findall('(\d\d)/(\d\d)/(\d\d\d\d) (\d\d):(\d\d)',date)
        if not len(matches):
           return date
        for (day, month, year, hour, minute) in matches:
            return f"{year}-{month}-{day} {hour}:{minute}:00"
    
    def getFile(sef, path):
        if not os.path.isfile(path):
            self.connection.rollback()
            raise Exception(f"file {path} not found") 
        return open(path, "r")

    def getDataFromFile(self, file):
        body = csv.reader(file, delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
        body = list(body)
        header = body[0]
        return (header, body[1:])

    def getColumnDataFromDb(self,table: str):
        columns = []
        typeLookup = dict()
        for (_, name, sqlType, _, _, _) in self.cursor.execute(f"PRAGMA table_info({table})").fetchall():
            columns.append(name)
            typeLookup[name] = sqlType
        return (columns, typeLookup)

    def getFormattedDataFromFile(self, table: str):
        (columns, typeLookup) = self.getColumnDataFromDb(table)

        (header, body)  = self.getDataFromFile(self.getFile(self.tableToPath(table)))

        if( header != columns):
            print('header')
            print(header)
            print('columns')
            print(columns)
            self.connection.rollback()
            raise Exception("header and columns do not match") 

        rows = []
        for row in body:
            for columnNumber in range(0, len(columns)):
                colType = typeLookup[columns[columnNumber]]
                if(colType == 'DATETIME'):
                    row[columnNumber] = self.convertDateTime(row[columnNumber])
            rows.append(tuple(row))
        return (columns, rows)

        