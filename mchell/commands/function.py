from command import Command
from app import main_app as app
import sys
from args import *

class FunctionCommand(Command):
    def schemes(self):
        return [
            [1, DefaultArg("function")]
        ]
    
    def execute(self, execute_at = None, execute_by = None):
        app.interpreter.add_function_to_stack(self.pargs["function"], execute_at, execute_by)

app.interpreter.add_command(FunctionCommand, "function")