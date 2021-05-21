from command import Command
from app import main_app as app
import sys
from args import *

class FillCommand(Command):
    def schemes(self):
        return [[3, CoordinateArg("coords"), CoordinateArg("dcoords"), BlockArg("block")]]
    
    def execute(self, execute_at, execute_by):
        coords = self.merge_coordinates(self.pargs["coords"], execute_at)
        dcoords = self.merge_coordinates(self.pargs["dcoords"], execute_at)

        for x in range(coords[0], dcoords[0] + 1):
            for y in range(coords[1], dcoords[1] + 1):
                for z in range(coords[2], dcoords[2] + 1):
                    print(x, y, z)
                    app.world.set_block((x, y, z), self.pargs["block"])


app.interpreter.add_command(FillCommand, "fill")