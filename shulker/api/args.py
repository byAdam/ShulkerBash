from shulker.api.world import *
from shulker.api.command import CommandInfo
from shulker.api.target import Target
from shulker.api.coordinates import Coordinates

class DefaultArg:
    type_name = "string"

    def __init__(self, name, display = None):
        self.name = name
        self.display = display

    def get_data(self, args, index):
        return self.name, self.value(args, index), self.index(args, index)

    def value(self, args, index):
        return args[index]

    def index(self, args, index):
        return index + 1

class CoordinateArg(DefaultArg):
    type_name = "x y z"
    
    def value(self, args, i):
        try:
            return Coordinates(args[i], args[i+1], args[i+2])
        except:
            return None

    def index(self, args, index):
        return index + 3

class StringArg(DefaultArg):
    type_name = "string"

    def value(self, args, index):
        return " ".join(args[index:])
    
    def index(self, args, index):
        return len(args)

class ListArg(DefaultArg):
    def __init__(self, name, options, display = None):
        super().__init__(name, display)
        self.options = options

    def value(self, args, index):
        if args[index] in self.options:
            return args[index]
        return None

class BlockArg(DefaultArg):
    type_name = "Block"

    def value(self, args, index):
        data = 0
        if index < len(args) - 1:
            try:
                data = int(args[index + 1])
            except:
                return None
        
        if 0 <= data <= 16:
            return Block(args[index], data)
        return None
    
    def index(self, args, index):
        return index + 2

class EntityArg(DefaultArg):
    type_name = "Entity"

class ExecuteArg(DefaultArg):
    type_name = "Command"

    def value(self, args, index):
        return " ".join(args[index:])
    
    def index(self, args, index):
        return len(args)

class IntegerArg(DefaultArg):
    type_name = "int"

    def value(self, args, index):
        try:
            return int(args[index])
        except:
            return None

class BooleanArg(DefaultArg):
    type_name = "bool"

    def value(self, args, index):
        if args[index] == "true":
            return True
        elif args[index] == "false":
            return False
        return None

class TargetArg(DefaultArg):
    type_name = "target"

    def value(self, args, index):
        return Target(args[index])