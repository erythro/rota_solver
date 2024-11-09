import argparse
import sqlite3
from Database.Commands.CreateMigration import CreateMigration
from Database.Commands.Migrate import Migrate
from Database.Commands.Dump import Dump
from Database.Commands.ImportDump import ImportDump
from functools import partial

connection = sqlite3.connect("var/data.db")

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers(title="command",dest='command')

commands = [
    CreateMigration(),
    Migrate(),
    Dump(connection),
    ImportDump(connection)
]

for command in commands:
    subparser = subparsers.add_parser(command.getName(), description=command.getDesc())
    command.configure(subparser)
    subparser.set_defaults(func=partial(command.execute))


args = main_parser.parse_args()
args.func(args)
