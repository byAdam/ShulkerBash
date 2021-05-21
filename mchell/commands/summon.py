from command import Command
from app import main_app as app
import sys
from args import *

class SummonCommand(Command):
    def schemes(self):
        return [[1, EntityArg("entity"), CoordinateArg("coords"), CommandArg("name")]]
        return [[1, EntityArg("entity"), CoordinateArg("name"), CommandArg("coords")]]
    
    def execute(self, execute_at, execute_by):

        coords = execute_at
        if "coords" in self.pargs:
            coords = self.merge_coordinates(self.pargs["coords"], execute_at)

        name = None
        if "name" in self.pargs:
            name = self.pargs["name"]

        entity = Entity(self.pargs["entity"], coords, name)
        app.world.set_entity(entity)

app.interpreter.add_command(SummonCommand, "summon")