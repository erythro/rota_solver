import argparse
import sqlite3
import Services.MigrationService
import os
from Commands.AbstractCommand import AbstractCommand

class Migrate(AbstractCommand):
    def getName(self) -> str:
        return 'migrate'
    def getDesc(self) -> str:
        return 'initialises the database'
    def configure(self, parser):
        pass
    def execute(self, args):
        connection = sqlite3.connect("var/data.db")

        migrationService = Services.MigrationService.MigrationService(connection,os.path.join('Migrations'))
        migrationService.migrate()

        connection.close()

        print('success')

