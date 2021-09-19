from shulker.api.command import Command
from shulker.app import main_app as app
import sys
from shulker.api.args import *
from shulker.api.error import *

class TeleportCommand(Command):
    def schemes(self):
        return [
            [2, TargetArg("target"), CoordinateArg("coordinates", "destination")],
            [2, TargetArg("target"), TargetArg("destination")],
        ]
    
    def execute(self, execute_at, execute_by):
        if "coordinates" in self.pargs:
            coordinates = execute_at.merge(self.pargs.get("coordinates"))
        else:
            d = app.world.find_entities(self.pargs["destination"], execute_at, execute_by)
            if len(d) > 1:
                raise TooManyTargetsException()
            else:
                coordinates = d[0].coordinates


        for e in app.world.find_entities(self.pargs["target"], execute_at, execute_by):
            e.teleport(coordinates)

app.interpreter.add_command(TeleportCommand, "teleport")
app.interpreter.add_command(TeleportCommand, "tp")