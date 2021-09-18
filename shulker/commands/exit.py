from command import Command
from app import main_app as app
from args import *
import sys

class ExitCommand(Command):
    def schemes(self):
        return [[0]]
    
    def execute(self, execute_at, execute_by):
        app.exit()


app.interpreter.add_command(ExitCommand, "exit")
app.interpreter.add_command(ExitCommand, "quit")