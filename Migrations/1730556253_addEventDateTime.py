def run(cursor):
   cursor.execute("""
      ALTER TABLE "event"
      ADD COLUMN "date_time" DATETIME NULL;
   """)