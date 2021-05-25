from app import main_app as app
from coordinates import Coordinates
from error import *

class CommandInfo:
    def __init__(self, raw, execute_at = None, execute_by = None, execute_in = None):
        self.raw = raw

        if execute_at is None:
            execute_at = Coordinates(0, 0, 0)

        self.execute_at = execute_at
        self.execute_by = execute_by
        self.execute_in = execute_in

        self.command = None
        try:
            self.command = self.get_command()
        except Exception as e:
            ## Issues with parsing command
            print(e)

    def execute(self):
        if self.command:
            try:
                self.command.execute_valid(self.execute_at, self.execute_by, self.execute_in)
            except Exception as e:
                ## Issues with executing command
                print(e)

    def get_command(self):
        if not self.raw or self.raw[0] == "#":
            return None 

        args = self.raw.split(" ")
        command = args[0]
        args = args[1:]

        if command in app.interpreter.commands:
            return app.interpreter.commands[command](self.raw, args)
        else:
            raise UnknownCommandException(command)

class Command:
    def __init__(self, raw, args):
        self.raw = raw
        self.args = args
        self.valid = False
        self.process_args()

    def schemes(self):
        pass

    @classmethod
    def get_help(cls, command):
        from args import ListArg

        pschemes = []

        for scheme in cls.schemes(cls):
            pscheme = [command]

            min_index = scheme[0]
            for i, arg in enumerate(scheme[1:]):
                no_brackets = False

                if arg.display is not None:
                    name = "{}: {}".format(arg.display, arg.type_name)
                else:
                    if type(arg) is ListArg:
                        # No brackets if one option
                        no_brackets = (len(arg.options) == 1)
                        name = "|".join(arg.options)
                    else:
                        name = "{}: {}".format(arg.name, arg.type_name)

                # Add brackets
                if no_brackets:
                    text = name
                elif i < min_index:
                    text = "<{}>".format(name)
                else:
                    text = "[{}]".format(name)
                    
                pscheme.append(text)

            pschemes.append(" ".join(pscheme))
        
        return "\n".join(pschemes)

    def execute_valid(self, execute_at, execute_by, execute_in):
        if self.valid:
            from commands.function import FunctionCommand
            if type(self) is FunctionCommand:
                self.execute(execute_at, execute_by, execute_in)
            else:
                self.execute(execute_at, execute_by)


    def process_args(self):
        ## Try find valid arguments for each scheme
        for scheme in self.schemes():
            self.pargs = self.process_args_with_scheme(scheme)

            if self.pargs is not None:
                break
        
        self.valid = self.pargs is not None

    def process_args_with_scheme(self, scheme):
        pargs = {}

        index = 0
        min_scheme = scheme[0]

        for arg in scheme[1:]:
            # Reached end of args
            if index >= len(self.args):
                break

            min_scheme -= 1
            name, value, index = arg.get_data(self.args, index)

            if value is not None:
                pargs[name] = value
            else:
                return None

        # If min scheme
        if min_scheme <= 0:
            return pargs

        return None