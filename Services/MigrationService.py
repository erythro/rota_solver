import importlib.util
import sys
import os
import time
from dataclasses import dataclass

@dataclass
class Migration:
    path: str
    timestamp: int
    name: str

class MigrationService:
    connection = None
    cursor = None
    migrationDirectory: str

    def __init__(self, connection, migrationDirectory):
        self.connection = connection
        self.cursor = connection.cursor()
        self.migrationDirectory = migrationDirectory
    
    def migrate(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS migration (name STRING PRIMARY KEY, ran_at DATETIME)')
        migrations = self.loadMigrations()
        for migration in migrations:
            if not self.isExecuted(migration):
                self.executeMigration(migration)
        self.connection.commit()

    def isExecuted(self, migration: Migration) -> bool:
        result = self.cursor.execute('SELECT ran_at FROM migration WHERE name = ?', [migration.name])
        return result.fetchone() != None

    def loadMigrations(self):
        migrations = []
        for file in os.listdir(self.migrationDirectory):
            filename = os.fsdecode(file)
            if filename.endswith(".py"): 
                [timestamp,name] = filename.split('_',2)
                name = name[:-3]
                migrations.append(Migration(path=os.path.join(self.migrationDirectory, filename),timestamp=timestamp,name=name))
        migrations.sort(key=lambda x: x.timestamp)
        return migrations


    def executeMigration(self, migration: Migration):
        spec = importlib.util.spec_from_file_location(migration.name, migration.path)
        migrationModule = importlib.util.module_from_spec(spec)
        sys.modules[migration.name] = migration
        spec.loader.exec_module(migrationModule)
        migrationModule.run(self.connection)
        print('executing: '+migration.name)
        self.cursor.execute('INSERT INTO migration VALUES (?, ?)', (migration.name, time.time()))