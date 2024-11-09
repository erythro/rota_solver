def run(cursor):
   cursor.execute('CREATE TABLE person(id INTEGER PRIMARY KEY AUTOINCREMENT, firstName STRING, lastName STRING)')