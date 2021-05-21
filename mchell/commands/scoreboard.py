from command import Command
from app import main_app as app
import sys
from args import *
from random import randint

class ScoreboardCommand(Command):
    def schemes(self):
        operators = ListArg("operator", ["%=", "*=", "+=", "-=", "/=", "<", "=", ">", "><"])

        return [
            [3, ListArg("type", ["objectives"]), ListArg("method", ["add"]), CommandArg("objective"), CommandArg("criterion")],
            [3, ListArg("type", ["objectives"]), ListArg("method", ["remove"]), CommandArg("objective")],
            [3, ListArg("type", ["players"]), ListArg("method", ["reset"]), TargetArg("target"), CommandArg("objective")],
            [6, ListArg("type", ["players"]), ListArg("method", ["random"]), TargetArg("target"), CommandArg("objective"), IntegerArg("min"), IntegerArg("max")],
            [5, ListArg("type", ["players"]), ListArg("method", ["set", "add", "remove"]), TargetArg("target"), CommandArg("objective"), IntegerArg("value")],
            [5, ListArg("type", ["players"]), ListArg("method", ["operation"]), TargetArg("target"), CommandArg("objective"), operators, TargetArg("target_b"), CommandArg("objective_b")]
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
            elif method == "operation":
                score_a = app.world.get_score(e, self.pargs["objective"])

                for other in app.world.find_entities(self.pargs["target_b"], execute_at, execute_by):
                    score_b = app.world.get_score(other, self.pargs["objective_b"])

                    score_new = self.evaluate_operator(score_a, score_b, self.pargs["operator"])

                    if type(score_new) is tuple:
                        app.world.set_score(e, self.pargs["objective"], score_new[0])
                        app.world.set_score(other, self.pargs["objective"], score_new[1])
                    else:
                        app.world.set_score(e, self.pargs["objective"], score_new)
                    

    def evaluate_operator(self, a, b, op):
        if op == "%=":
            return a % b
        if op == "*=":
            return a * b
        if op == "+=":
            return a + b
        if op == "-=":
            return a - b
        if op == "/=":
            return a // b
        if op == "<":
            return min(a, b)
        if op == "=":
            return b
        if op == ">":
            return max(a, b)
        if op == "><":
            return b, a

app.interpreter.add_command(ScoreboardCommand, "scoreboard")