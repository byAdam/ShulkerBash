from shulker.api.command import Command
from shulker.app import main_app as app
from shulker.api.args import *
from shulker.api.error import *

class HelpCommand(Command):
    def schemes(self):
        return [[0, StringArg("command")]]
    
    def execute(self, execute_at, execute_by):
        if "command" in self.pargs:
            command = self.pargs["command"]

            if command in app.interpreter.commands:
                h = app.interpreter.commands[command].get_help(command, True)
                print("Usage:")
                print(h)
            else:
                raise UnknownCommandException(command)
        else:
            commands = app.interpreter.commands
            print("Commands:")
            for command in commands:
                print("  "+command)

app.interpreter.add_command(HelpCommand, "help")