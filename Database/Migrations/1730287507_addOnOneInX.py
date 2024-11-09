def run(cursor):
   cursor.execute("""
      ALTER TABLE "person_role"
   	ADD COLUMN "on_one_in_x_events" INTEGER NULL DEFAULT NULL;
   """)