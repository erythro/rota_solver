def run(cursor):
   cursor.execute("""
       CREATE TABLE person_date_preference(person_id INTEGER NOT NULL, date DATE NOT NULL, preference_type VARCHAR(50) NOT NULL)
   """)
