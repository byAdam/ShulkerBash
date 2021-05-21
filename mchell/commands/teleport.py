from command import Command
from app import main_app as app
import sys
from args import *

class TeleportCommand(Command):
    def schemes(self):
        return [
            [1, TargetArg("target"), CoordinateArg("coordinates")],
            [1, TargetArg("target"), TargetArg("destination")],
        ]
    
    def execute(self, execute_at, execute_by):
        if "coordinates" in self.pargs:
            coordinates = execute_at.merge(self.pargs.get("coordinates"))
        else:
            d = app.world.find_entities(self.pargs["destination"], execute_at, execute_by)
            if len(d) != 1:
                print("Error finding destination")
                return
            else:
                coordinates = d[0].coordinates


        for e in app.world.find_entities(self.pargs["target"], execute_at, execute_by):
            e.teleport(coordinates)

app.interpreter.add_command(TeleportCommand, "teleport")