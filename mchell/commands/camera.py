from command import Command
from app import main_app as app
import sys
from args import *

class CameraCommand(Command):
    def schemes(self):
        return [
            [2, ListArg("method", ["position"]), CoordinateArg("coordinates")],
            [2, ListArg("method", ["dimensions"]), CoordinateArg("coordinates")],
            [1, ListArg("method", ["start","stop"])],
        ]
    
    def execute(self, execute_at, execute_by):

        m = self.pargs["method"]
        if m == "start":
            app.camera.start()
        elif m == "stop":
            app.camera.stop()
        elif m == "position":
            coordinates = execute_at.merge(self.pargs.get("coordinates"))
            app.camera.set_position(coordinates)
        elif m == "dimensions":
            dim = self.pargs["coordinates"]
            if dim.is_absolute():
                app.camera.set_dimensions(dim)
        

app.interpreter.add_command(CameraCommand, "camera")