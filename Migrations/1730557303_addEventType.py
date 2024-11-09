def run(cursor):
   cursor.execute("""
      ALTER TABLE "event"
	   ADD COLUMN "type" VARCHAR(50) NOT NULL DEFAULT 'morning_1';
   """)