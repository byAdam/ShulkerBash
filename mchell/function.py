from command import CommandInfo
import re
import os
from app import main_app as app

class Function:
    def __init__(self, base_path, relative_path):
        self.base_path = base_path
        self.relative_path = relative_path

        self.load()
        self.proccess_lines()

    def load(self):
        with open(self.base_path) as f:
            self.lines = f.readlines()

    def proccess_lines(self):
        self.plines = []
        in_function = False

        for line in self.lines:
            if not line:
                continue
            elif line.startswith("#"):
                continue
            elif line.startswith("def"):
                function = []
                fname = line.split("def ")[1].strip()
                in_function = True
                white_space = False
            elif in_function:
                if not white_space:
                    white_space = re.findall(r"^\s*", line)[0]

                if line.startswith(white_space):
                    function.append(line.strip())
                else:
                    fname = os.path.dirname(self.relative_path) + fname
                    app.interpreter.functions[fname] = Subfunction(function, fname)
                    in_function = False
            else:
                self.plines.append(line.strip())
    
        self.lines = self.plines

    def get_commands_for_stack(self, execute_at, execute_by):
        return [CommandInfo(line, execute_at, execute_by, self.relative_path) for line in reversed(self.lines)]


class Subfunction(Function):
    def __init__(self, lines, relative_path):
        self.relative_path = relative_path
        self.lines = lines