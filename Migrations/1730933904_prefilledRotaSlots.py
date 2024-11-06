def run(cursor):
   cursor.execute("""
       CREATE TABLE prefilled_rota(person_id INTEGER NOT NULL, slot_id INTEGER NOT NULL)
   """)
