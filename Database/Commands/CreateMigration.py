import argparse
import sqlite3
import Services.MigrationService
import os
import time
from Database.Commands.AbstractCommand import AbstractCommand

class CreateMigration(AbstractCommand):
    def getName(self) -> str:
        return 'createMigration'
    def getDesc(self) -> str:
        return 'creates a migration'
    def configure(self, parser):
        parser.add_argument('name',metavar='name',type=str, help='the name of your migration')
    def execute(self, args):
        print('creating migration:' + args.name)

        name = str(int(time.time())) + '_' + args.name + '.py'

        f = open(os.path.join('Database','Migrations',name), "w")
        f.write("def run(cursor):\n")
        f.write('   cursor.execute("""\n')
        f.write("       #put your migration here\n")
        f.write('   """)\n')
        f.close()

        print('created Migration')