from shulker.api.command import CommandInfo
import re
import os
from shulker.app import main_app as app
from shulker.api.error import InvalidSubfunctionException

class Function:
    def __init__(self, base_path, relative_path):
        self.base_path = base_path
        self.relative_path = relative_path

        self.load()
        self.proccess_lines()

    def load(self):
        with open(self.base_path) as f:
            self.lines = f.readlines()

    def proccess_subfunction(self, i, name):
        j = i + 1

        if j < len(self.lines):
            white_space = re.findall(r"^\s+", self.lines[j])[0]

            if white_space == "\n":
                raise InvalidSubfunctionException(name)
        else:
            raise InvalidSubfunctionException(name)

        subfunction = []

        ## Loop through function
        ## TODO: Make this more dynamic, so we dont have two parsing functions
        while j < len(self.lines):
            line = self.lines[j]
            if re.match(r"^\s*$", line) or line.strip().startswith("#"):
                pass
            elif line.startswith(white_space):
                subfunction.append(line.strip())
            else:
                break
            
            j += 1


        fname = os.path.dirname(self.relative_path) + name
        app.interpreter.functions[fname] = Subfunction(subfunction, fname)

        return j - 1

    def proccess_lines(self):
        self.plines = []

        i = 0
        while i < len(self.lines):
            line = self.lines[i]

            ## If blank line or comment
            if re.match(r"^\s*$", line) or line.strip().startswith("#"):
                pass
            ## If start of subfunction
            elif line.startswith("def"):
                name = line.split("def ")[1].strip()
                i = self.proccess_subfunction(i, name)
            ## If normal line
            else:
                self.plines.append(line)

            i += 1
        
        ## Trim whitespace
        self.lines = [x.strip() for x in self.plines]

    def get_commands_for_stack(self, execute_at, execute_by):
        return [CommandInfo(line, execute_at, execute_by, self.relative_path) for line in reversed(self.lines)]


class Subfunction(Function):
    def __init__(self, lines, relative_path):
        self.relative_path = relative_path
        self.lines = lines