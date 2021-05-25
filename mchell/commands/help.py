from command import Command
from app import main_app as app
from args import *
from error import *

class HelpCommand(Command):
    def schemes(self):
        return [[1, StringArg("command")]]
    
    def execute(self, execute_at, execute_by):
        command = self.pargs["command"]

        if command in app.interpreter.commands:
            h = app.interpreter.commands[command].get_help(command)
            print(h)
        else:
            raise UnknownCommandException(command)

app.interpreter.add_command(HelpCommand, "help")