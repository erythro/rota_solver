import argparse
import sqlite3
import Services.MigrationService

parser = argparse.ArgumentParser(description='initialises the database')
parser.parse_args()

connection = sqlite3.connect("var/data.db")

migrationService = Services.MigrationService.MigrationService(connection,'Migrations')
migrationService.migrate()

connection.close()

print('success')