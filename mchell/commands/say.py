from command import Command
from app import main_app as app

class SayCommand(Command):
    def schemes(self):
        return [1, Target("target")]
    
    def execute(self, execute_at, execute_by):
        import sys

        sys.stdout.write(" ".join(self.args))
        sys.stdout.write("\n")

app.interpreter.add_command(SayCommand, "say")