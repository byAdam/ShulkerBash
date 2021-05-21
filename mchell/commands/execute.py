from command import Command
from app import main_app as app
import sys
from args import *

class ExecuteCommand(Command):
    def schemes(self):
        return [
            [3, TargetArg("target"), CoordinateArg("coordinates"), ExecuteArg("command")]
        ]
    
    def execute(self, execute_at, execute_by):
        coordinates = execute_at.merge(self.pargs.get("coordinates"))
        entities = app.world.find_entities(self.pargs["target"], execute_at, execute_by)
        command = self.pargs["command"]

        for e in entities:
            CommandInfo(command, coordinates, e).execute()

app.interpreter.add_command(ExecuteCommand, "execute")