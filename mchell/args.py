from world.world import *
from command import CommandInfo
from target import Target
from coordinates import Coordinates

class CommandArg:
    def __init__(self, name):
        self.name = name

    def get_data(self, args, index):
        return self.name, self.value(args, index), self.index(args, index)

    def value(self, args, index):
        return args[index]

    def index(self, args, index):
        return index + 1

class CoordinateArg(CommandArg):
    def value(self, args, i):
        try:
            return Coordinates(args[i], args[i+1], args[i+2])
        except:
            return None

    def index(self, args, index):
        return index + 3

class StringArg(CommandArg):
    def value(self, args, index):
        return " ".join(args)
    
    def index(self, args, index):
        return len(args)

class ListArg(CommandArg):
    def __init__(self, name, options):
        super().__init__(name)
        self.options = options

    def value(self, args, index):
        if args[index] in self.options:
            return args[index]
        return None

class BlockArg(CommandArg):
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

class EntityArg(CommandArg):
    pass

class ExecuteArg(CommandArg):
    def value(self, args, index):
        return CommandInfo(" ".join(args))
    
    def index(self, args, index):
        return len(args)

class IntegerArg(CommandArg):
    def value(self, args, index):
        try:
            return int(args[index])
        except:
            return None

class BooleanArg(CommandArg):
    def value(self, args, index):
        if args[index] == "true":
            return True
        elif args[index] == "false":
            return False
        return None

class TargetArg(CommandArg):
    def value(self, args, index):
        return Target(args[index])