from command import Command
from app import main_app as app
import sys
from args import *

class SetblockCommand(Command):
    def __init__(self, args):
        super().__init__(args)

        self.schemes.append([2, CoordinateArg("coords"), BlockArg("block")])
        self.process_args()
    
    def execute(self, execute_at, execute_by):
        app.world.set_block((0, 0, 0), "stone", 0)

app.interpreter.add_command(SetblockCommand, "setblock")