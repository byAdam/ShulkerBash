from shulker.api.command import Command
from shulker.app import main_app as app
import sys
from shulker.api.args import *

class SetblockCommand(Command):
    def schemes(self):
        return [[2, CoordinateArg("coordinates", "position"), BlockArg("block")]]
    
    def execute(self, execute_at, execute_by):
        coordinates = execute_at.merge(self.pargs["coordinates"])
        
        app.world.set_block(coordinates, self.pargs["block"])

app.interpreter.add_command(SetblockCommand, "setblock")