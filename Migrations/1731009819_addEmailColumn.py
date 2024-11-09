def run(cursor):
   cursor.execute("""
       ALTER TABLE "person"
        ADD COLUMN "email" VARCHAR(255);
   """)
