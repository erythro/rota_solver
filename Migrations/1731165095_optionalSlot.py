def run(cursor):
   cursor.execute("""
       ALTER TABLE "slot"
        ADD COLUMN "optional" TINYINT NOT NULL DEFAULT FALSE;
   """)
