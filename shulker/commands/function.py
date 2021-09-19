from shulker.api.command import Command
from shulker.app import main_app as app
import sys
from shulker.api.args import *
import os

class FunctionCommand(Command):
    def schemes(self):
        return [
            [1, DefaultArg("function"), BooleanArg("is_relative")]
        ]
    
    def execute(self, execute_at = None, execute_by = None, execute_in = None):
        fname = self.pargs["function"].replace('/', os.sep)

        if "is_relative" in self.pargs and self.pargs["is_relative"]:
            app.interpreter.add_function_to_stack(fname, execute_at, execute_by, execute_in)
        else:
            app.interpreter.add_function_to_stack(fname, execute_at, execute_by)

app.interpreter.add_command(FunctionCommand, "function")