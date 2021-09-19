from threading import Thread
from shulker.app import main_app as app
import os
import time

from shulker.api.world import World, Entity
from shulker.api.command import CommandInfo
from shulker.api.function import Function
from shulker.api.coordinates import Coordinates
from shulker.api.error import UnknownFunctionException

class Interpreter(Thread):
    def __init__(self, is_shell=True, is_looping=False):
        super().__init__()

        self.world = World()

        self.is_shell = is_shell
        self.is_looping = is_looping
        self.commands = {}

        self.scoreboard_input = None

        self.main_entity = Entity("main", Coordinates(0, 0, 0), "main", "main")
        self.world.set_entity(self.main_entity)
        self.origin = Coordinates(0, 0, 0)

        if not self.is_shell:
            self.main_function = os.path.relpath(app.main_function, app.directory)

        self.command_stack = []

        self.functions = {}

    def set_input(self, text):
        try:
            text = int(text)
        except:
            pass

        self.scoreboard_input = text

    def read_input(self):
        if not self.scoreboard_input:
            return None, None

        if type(self.scoreboard_input) is int:
            return self.scoreboard_input, None
        else:
            char = self.scoreboard_input[0]
            return ord(char), self.scoreboard_input[1:]

    def proccess_stack(self):
        while self.command_stack:
            self.command_stack.pop().execute()
    
    def read_functions_in_directory(self, base, current=""):
        dpath = os.path.join(base, current)
        for f in os.listdir(dpath):
            ## Total path
            fpath = os.path.join(dpath, f)
            ## Relative path
            cpath = os.path.join(current, f)

            if os.path.isdir(fpath):
                pass
            else:
                fname, extension = os.path.splitext(cpath)
                if extension == ".mcfunction":
                    try:
                        self.functions[fname] = Function(fpath, cpath)
                    except Exception as e:
                        if app.show_errors:
                            print(e)

    def add_function_to_stack(self, fname, execute_at = None, execute_by = None, execute_in = None):
        ## If passed the function its executed in, then find the function relative
        if execute_in is not None:
            fname = os.path.join(os.path.dirname(execute_in), fname)

        # Read all functions in folder
        if fname not in self.functions:
            self.read_functions_in_directory(app.directory, os.path.dirname(fname))

        # If found function
        if fname in self.functions:
            self.command_stack += self.functions[fname].get_commands_for_stack(execute_at, execute_by)
        else:
            raise UnknownFunctionException(fname)

    def run(self):
        if self.is_shell:
            while True:
                inp = input("> ")
                CommandInfo(inp, self.origin, self.main_entity).execute()
                self.proccess_stack()
        else:
            if self.is_looping:
                while True:
                    start = time.time()
                    self.run_function_loop()
                    duration = time.time() - start
                    time.sleep(0.05 - duration)
            else:
                self.run_function_loop()
                app.exit()

    def run_function_loop(self):
        self.add_function_to_stack(self.main_function, self.origin, self.main_entity)
        self.proccess_stack()

    def add_command(self, obj, name):
        self.commands[name] = obj