def run(cursor):
   cursor.execute('CREATE TABLE event_role(id INTEGER PRIMARY KEY AUTOINCREMENT, event_id INTEGER, role_id INTEGER)')