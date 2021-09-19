from shulker.api.command import Command
from shulker.app import main_app as app
from shulker.api.args import *
import sys

class DebugCommand(Command):
    def schemes(self):
        return [[1, ListArg("type", ["entities", "scoreboards"])]]

    def execute(self, execute_at, execute_by):
        if self.pargs["type"] == "entities":
            self.debug_entities()
        elif self.pargs["type"] == "scoreboards":
            self.debug_scoreboards()
        
    def debug_entities(self):
        sys.stdout.write("\n".join(str(x) for x in app.world.entities.values()))
        sys.stdout.write("\n")

    def debug_scoreboards(self):
        sys.stdout.write("\n".join(str(x) for x in app.world.scoreboards.values()))
        sys.stdout.write("\n")

app.interpreter.add_command(DebugCommand, "debug")