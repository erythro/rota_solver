import argparse
import sqlite3
import Services.MigrationService
import os
import time

parser = argparse.ArgumentParser(description='creates a migration')
parser.add_argument('name',metavar='name',type=str, help='the name of your migration')
args = parser.parse_args()

print('creating migration:' + args.name)

name = str(int(time.time())) + '_' + args.name + '.py'

f = open(os.path.join('Migrations',name), "w")
f.write("def run(cursor):\n")
f.write("   #put your migration here")
f.close()

print('created Migration')