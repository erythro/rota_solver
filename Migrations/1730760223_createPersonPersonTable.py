def run(cursor):
   cursor.execute("""
        CREATE TABLE person_person(from_id INTEGER NOT NULL, to_id INTEGER NOT NULL, relationship_type VARCHAR(50) NOT NULL)
   """)
