from command import Command
from app import main_app as app

class DebugCommand(Command):
    def schemes(self):
        return [[0]]

    def execute(self, execute_at, execute_by):
        import sys

        sys.stdout.write("\n".join(str(x) for x in app.world.entities.values()))
        sys.stdout.write("\n")

app.interpreter.add_command(DebugCommand, "debug")