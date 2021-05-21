from command import Command
from app import main_app as app
import sys
from args import *

class SetblockCommand(Command):
    def schemes(self):
        return [[2, CoordinateArg("coords"), BlockArg("block"), ListArg("place_type", ["replace", "destroy", "keep"])]]
    
    def execute(self, execute_at, execute_by):
        coords = self.merge_coordinates(self.pargs["coords"], execute_at)

        app.world.set_block(coords, self.pargs["block"])

app.interpreter.add_command(SetblockCommand, "setblock")