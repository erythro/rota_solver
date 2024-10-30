def run(cursor):
   cursor.execute("""
      ALTER TABLE "person_role"
   	ADD COLUMN "expected_period" INTEGER NULL DEFAULT NULL;
   """)