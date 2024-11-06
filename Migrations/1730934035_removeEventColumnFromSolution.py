def run(cursor):
   cursor.execute("""
        ALTER TABLE "solution"
	        DROP COLUMN "event_id";
   """)
