import argparse
import sqlite3
from Commands.CreateMigration import CreateMigration
from Commands.Migrate import Migrate
from Commands.Dump import Dump
from Commands.ImportDump import ImportDump
from Commands.GenerateRota import GenerateRota
from functools import partial

connection = sqlite3.connect("var/data.db")

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers(title="command",dest='command')

commands = [
    CreateMigration(),
    Migrate(),
    Dump(connection),
    ImportDump(connection),
    GenerateRota()
]

for command in commands:
    subparser = subparsers.add_parser(command.getName(), description=command.getDesc())
    command.configure(subparser)
    subparser.set_defaults(func=partial(command.execute))


args = main_parser.parse_args()
args.func(args)
