from command import Command
from app import main_app as app
import sys
from args import *

class CameraCommand(Command):
    def schemes(self):
        return [
            [3, ListArg("method", ["start"]), CoordinateArg("coordinates"), CoordinateArg("dimensions")],
            [1, ListArg("method", ["stop"])],
        ]
    
    def execute(self, execute_at, execute_by):
        if self.pargs["method"] == "start":
            self.start_camera(execute_at, execute_by)
        elif self.pargs["method"] == "stop":
            self.stop_camera()

    def stop_camera(self):
        app.camera.stop()

    def start_camera(self, execute_at, execute_by):
        coordinates = execute_at.merge(self.pargs.get("coordinates"))
        dimensions = self.pargs.get("dimensions")

        if not dimensions.is_absolute():
            print("Need absolute coordinates")
            return

        app.camera.start(coordinates, dimensions)

app.interpreter.add_command(CameraCommand, "camera")