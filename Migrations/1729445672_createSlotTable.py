def run(cursor):
   cursor.execute('CREATE TABLE slot(id INTEGER PRIMARY KEY AUTOINCREMENT, event_id INTEGER, role_id INTEGER)')