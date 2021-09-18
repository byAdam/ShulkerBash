from command import Command
from app import main_app as app
from args import *

class SayCommand(Command):
    def schemes(self):
        return [[1, StringArg("text", "message")]]
    
    def execute(self, execute_at, execute_by):
        text = []
        for word in self.pargs["text"].split(" "):
            if word[0] == "@":
                for e in app.world.find_entities(Target(word), execute_at, execute_by, False):
                    text.append(e.display_name())
            else:
                text.append(word)

        name = "@"
        if execute_by is not None:
            name = execute_by.display_name()

        print("[{}] ".format(name) + " ".join(text))

app.interpreter.add_command(SayCommand, "say")