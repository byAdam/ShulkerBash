from command import Command
from app import main_app as app
import sys
from args import *

class SummonCommand(Command):
    def schemes(self):
        return [
            [1, EntityArg("entity"), CoordinateArg("coordinates"), CommandArg("name")],
            [1, EntityArg("entity"), CommandArg("name"), CoordinateArg("coordinates")]
        ]
    
    def execute(self, execute_at, execute_by):

        coordinates = execute_at.merge(self.pargs.get("coordinates"))
        name = self.pargs.get("name")
        
        print(execute_at)
        print(self.pargs.get("coordinates"))
        print(coordinates)

        entity = Entity(self.pargs["entity"], coordinates, name)
        app.world.set_entity(entity)

app.interpreter.add_command(SummonCommand, "summon")