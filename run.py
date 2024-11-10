import argparse
import sqlite3
from Commands.CreateMigration import CreateMigration
from Commands.Migrate import Migrate
from Commands.Dump import Dump
from Commands.ImportDump import ImportDump
from Commands.GenerateRota import GenerateRota
from Commands.ImportChurchSuite import ImportChurchSuite
from Services.DataService import DataService
from Services.DataService import DataService
from Services.ValidationService import ValidationService
from functools import partial

connection = sqlite3.connect("var/data.db")
dataService = DataService(connection)
validator = ValidationService(dataService)

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers(title="command")

commands = [
    CreateMigration(),
    Migrate(),
    Dump(connection),
    ImportDump(connection,validator),
    GenerateRota(validator, dataService, connection),
    ImportChurchSuite(dataService)
]

for command in commands:
    subparser = subparsers.add_parser(command.getName(), description=command.getDesc())
    command.configure(subparser)
    subparser.set_defaults(func=partial(command.execute))


args = main_parser.parse_args()
args.func(args)
