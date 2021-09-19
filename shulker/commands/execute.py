from shulker.api.command import Command
from shulker.app import main_app as app
from shulker.api.world import Block
import sys
from shulker.api.args import *

class ExecuteCommand(Command):
    def schemes(self):
        return [
            [6, TargetArg("target"), CoordinateArg("coordinates", "position"), ListArg("detect", ["detect"]), CoordinateArg("dcoordinates", "detectPos"), BlockArg("block") , ExecuteArg("command")],
            [3, TargetArg("target"), CoordinateArg("coordinates", "position"), ExecuteArg("command")]
        ]
    
    def execute(self, execute_at, execute_by):
        coordinates = execute_at.merge(self.pargs.get("coordinates"))
        entities = app.world.find_entities(self.pargs["target"], execute_at, execute_by)

        command = self.pargs["command"]

        for e in entities:
            ## If blocks don't match, skip command execution
            if "detect" in self.pargs:
                dcoords = e.coordinates.merge(self.pargs.get("dcoordinates"))
                dblock = self.pargs["block"]
                rblock = app.world.get_block(dcoords)

                if dblock != rblock:
                    continue
            
            CommandInfo(command, coordinates, e).execute()

app.interpreter.add_command(ExecuteCommand, "execute")