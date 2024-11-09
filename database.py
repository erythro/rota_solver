import argparse
from Database.Commands.CreateMigration import CreateMigration
from Database.Commands.Migrate import Migrate

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers(title="command",dest='command')

commands = [
    CreateMigration(),
    Migrate()
]

for command in commands:
    subparser = subparsers.add_parser(command.getName(), description=command.getDesc())
    command.configure(subparser)
    subparser.set_defaults(func=lambda args: command.execute(args))


args = main_parser.parse_args()
args.func(args)