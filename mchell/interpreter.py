from threading import Thread
from app import main_app as app
import os

from world.world import World
from command import CommandInfo
from function import Function

class Interpreter(Thread):
    def __init__(self, is_shell=True):
        super().__init__()

        self.world = World()

        self.is_shell = is_shell
        self.commands = {}

        
        if not self.is_shell:
            self.main_function = os.path.relpath(app.main_function, app.directory)

        self.command_stack = []

    def proccess_stack(self):
        while self.command_stack:
            self.command_stack.pop().execute()

    def read_functions(self, base, current = ""):
        dpath = os.path.join(base, current)
        for f in os.listdir(dpath):
            ## Total path
            fpath = os.path.join(dpath, f)
            ## Relative path
            cpath = os.path.join(current, f)

            if os.path.isdir(fpath):
                self.read_functions(base, cpath)
            else:
                fname, extension = os.path.splitext(cpath)
                if extension == ".mcfunction":
                    self.functions[fname] = Function(fpath, cpath)

    def add_function_to_stack(self, fname, execute_at = None, execute_by = None, execute_in = None):
        ## If passed the function its executed in, then find the function relative
        if execute_in is not None:
            fname = os.path.join(os.path.dirname(execute_in), fname)

        if fname in self.functions:
            self.command_stack += self.functions[fname].get_commands_for_stack(execute_at, execute_by)

    def run(self):
        self.functions = {}
        self.read_functions(app.directory)

        if self.is_shell:
            while True:
                inp = input("> ")
                CommandInfo(inp).execute()
                self.proccess_stack()
        else:
            self.add_function_to_stack(self.main_function)
            self.proccess_stack()

    def add_command(self, obj, name):
        self.commands[name] = obj