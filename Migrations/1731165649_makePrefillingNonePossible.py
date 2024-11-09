def run(cursor):
   cursor.execute("""
    ALTER TABLE "prefilled_rota"
	    DROP COLUMN "person_id";
   """)
   cursor.execute("""
    ALTER TABLE "prefilled_rota"
	    ADD COLUMN "person_id" INTEGER NULL;
    """)