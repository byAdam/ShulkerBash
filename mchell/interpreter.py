from threading import Thread
from app import main_app as app

from world.world import World
from command import CommandInfo

class Interpreter(Thread):
    def __init__(self, is_shell=True):
        super().__init__()

        self.world = World()

        self.is_shell = True
        self.commands = {}

        self.command_stack = []

        self.start()

    def run(self):
        if self.is_shell:
            while True:
                inp = input("> ")
                CommandInfo(inp).execute()
        else:
            print("Not shell")
            self.execute_stack()

    def execute_stack(self):
        while self.command_stack:
            self.command_stack.pop().execute()

    def add_command(self, obj, name):
        self.commands[name] = obj