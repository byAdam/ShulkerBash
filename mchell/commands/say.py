from command import Command
from app import main_app as app
from args import *

class SayCommand(Command):
    def schemes(self):
        return [[1, StringArg("text")]]
    
    def execute(self, execute_at, execute_by):
        import sys

        text = []
        for word in self.pargs["text"].split(" "):
            if word[0] == "@":
                for e in app.world.find_entities(Target(word), execute_at, execute_by):
                    text.append(e.display_name())
            else:
                text.append(word)

        sys.stdout.write(" ".join(text))
        sys.stdout.write("\n")

app.interpreter.add_command(SayCommand, "say")