from shulker.api.command import Command
from shulker.app import main_app as app
import sys
from shulker.api.args import *
from shulker.api.error import InvalidCommandException

class CameraCommand(Command):
    def schemes(self):
        return [
            [2, ListArg("method", ["position"]), CoordinateArg("coordinates", "position")],
            [2, ListArg("method", ["dimensions"]), CoordinateArg("coordinates", "dimensions")],
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
                if dim.x >= 1 and dim.y >= 1 and dim.z >+ 0:
                    app.camera.set_dimensions(dim)
                else:
                    raise InvalidCommandException(self.raw, "The dimensions must all be greater than or equal to 0")
            else:
                raise InvalidCommandException(self.raw, "The dimensions must all be greater than or equal to 0")
        

app.interpreter.add_command(CameraCommand, "camera")