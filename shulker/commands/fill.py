from shulker.api.command import Command
from shulker.app import main_app as app
import sys
from shulker.api.args import *
from shulker.api.coordinates import Coordinates

class FillCommand(Command):
    def schemes(self):
        return [[3, CoordinateArg("coordinates", "from"), CoordinateArg("delta_coordinates", "to"), BlockArg("block")]]
    
    def execute(self, execute_at, execute_by):
        coordinates = execute_at.merge(self.pargs["coordinates"])
        delta_coordinates = execute_at.merge(self.pargs["delta_coordinates"])

        for x in range(coordinates.x, delta_coordinates.x + 1):
            for y in range(coordinates.y, delta_coordinates.y + 1):
                for z in range(coordinates.z, delta_coordinates.z + 1):
                    app.world.set_block(Coordinates(x, y, z), self.pargs["block"])


app.interpreter.add_command(FillCommand, "fill")