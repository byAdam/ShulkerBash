from command import Command
from app import main_app as app
import sys
from args import *

class SummonCommand(Command):
    def schemes(self):
        return [[2, EntityArg("entity"), CoordinateArg("coords")]]
    
    def execute(self, execute_at, execute_by):
        coords = self.merge_coordinates(self.pargs["coords"], execute_at)

        entity = Entity(self.pargs["entity"], coords)
        app.world.set_entity(entity)

app.interpreter.add_command(SummonCommand, "summon")