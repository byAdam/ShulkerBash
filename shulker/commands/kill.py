from shulker.api.command import Command
from shulker.app import main_app as app
import sys
from shulker.api.args import *

class KillCommand(Command):
    def schemes(self):
        return [[1, TargetArg("target")]]

    def execute(self, execute_at, execute_by):
        entities = app.world.find_entities(self.pargs["target"], execute_at, execute_by)
        for e in entities:
            if e.uuid != "main":
                app.world.kill_entity(e)

app.interpreter.add_command(KillCommand, "kill")