from shulker.api.command import Command
from shulker.app import main_app as app
import sys
from shulker.api.args import *

class TagCommand(Command):
    def schemes(self):
        return [
            [3, TargetArg("target"), ListArg("method", ["add", "remove"]), DefaultArg("tag")]
        ]
    
    def execute(self, execute_at, execute_by):
        entities = app.world.find_entities(self.pargs["target"], execute_at, execute_by)

        if self.pargs["method"] == "add":
            for e in entities:
                e.add_tag(self.pargs["tag"])
        elif self.pargs["method"] == "remove":
            for e in entities:
                e.remove_tag(self.pargs["tag"])

app.interpreter.add_command(TagCommand, "tag")