def run(cursor):
   cursor.execute("""
        ALTER TABLE "person"
        ADD COLUMN "preferred_serving_mode" VARCHAR(50) NOT NULL DEFAULT 'only_mornings_or_evening';
   """)
