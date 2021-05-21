from command import Command
from app import main_app as app
import sys
from args import *
from random import randint

class ScoreboardCommand(Command):
    def schemes(self):
        return [
            [3, ListArg("type", ["objectives"]), ListArg("method", ["add"]), CommandArg("objective"), CommandArg("criterion")],
            [3, ListArg("type", ["objectives"]), ListArg("method", ["remove"]), CommandArg("objective")],
            [3, ListArg("type", ["players"]), ListArg("method", ["reset"]), TargetArg("target"), CommandArg("objective")],
            [6, ListArg("type", ["players"]), ListArg("method", ["random"]), TargetArg("target"), CommandArg("objective"), IntegerArg("min"), IntegerArg("max")],
            [5, ListArg("type", ["players"]), ListArg("method", ["set", "add", "remove"]), TargetArg("target"), CommandArg("objective"), IntegerArg("value")]
        ]
    
    def execute(self, execute_at, execute_by):
        if self.pargs["type"] == "objectives":
            self.execute_objectives(execute_at, execute_by)
        elif self.pargs["type"] == "players":
            self.execute_players(execute_at, execute_by)

    def execute_objectives(self, execute_at, execute_by):
        if self.pargs["method"] == "add":
            app.world.add_objective(self.pargs["objective"])
        elif self.pargs["method"] == "remove":
            app.world.remove_objective(self.pargs["objective"])

    def execute_players(self, execute_at, execute_by):
        entities = app.world.find_entities(self.pargs["target"], execute_at, execute_by)

        method = self.pargs["method"]
        for e in entities:
            if method == "reset":
                if "objective" in self.pargs:
                    app.world.reset_score(e, self.pargs["objective"])
                else:
                    app.world.reset_score(e)
            elif method == "random":
                value = randint(self.pargs["min"], self.pargs["max"])
                app.world.set_score(e, self.pargs["objective"], value)
            elif method == "set":
                app.world.set_score(e, self.pargs["objective"], self.pargs["value"])
            elif method == "add":
                current = app.world.get_score(e, self.pargs["objective"])
                if current is None:
                    current = 0

                value = current + self.pargs["value"]
                app.world.set_score(e, self.pargs["objective"], value)
            elif method == "remove":
                current = app.world.get_score(e, self.pargs["objective"])
                if current is None:
                    current = 0

                value = current - self.pargs["value"]
                app.world.set_score(e, self.pargs["objective"], value)

app.interpreter.add_command(ScoreboardCommand, "scoreboard")