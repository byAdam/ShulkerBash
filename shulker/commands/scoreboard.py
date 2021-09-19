from shulker.api.command import Command
from shulker.app import main_app as app
import sys
from shulker.api.args import *
from random import randint
from shulker.api.world import ScoreEntity
from shulker.api.error import NoTargetsException

class ScoreboardCommand(Command):
    def schemes(self):
        operators = ListArg("operator", ["%=", "*=", "+=", "-=", "/=", "<", "=", ">", "><"], "operator")

        return [
            [3, ListArg("type", ["objectives"]), ListArg("method", ["add"]), DefaultArg("objective"), DefaultArg("criterion")],
            [3, ListArg("type", ["objectives"]), ListArg("method", ["remove"]), DefaultArg("objective")],
            [3, ListArg("type", ["players"]), ListArg("method", ["reset"]), TargetArg("target"), DefaultArg("objective")],
            [6, ListArg("type", ["players"]), ListArg("method", ["random"]), TargetArg("target"), DefaultArg("objective"), IntegerArg("min"), IntegerArg("max")],
            [5, ListArg("type", ["players"]), ListArg("method", ["set", "add", "remove"]), TargetArg("target"), DefaultArg("objective"), IntegerArg("value")],
            [7, ListArg("type", ["players"]), ListArg("method", ["operation"]), TargetArg("target", "targetSelector"), DefaultArg("objective", "targetObjective"), operators, TargetArg("target_b", "selector"), DefaultArg("objective_b", "objective")],
            [2, ListArg("type", ["input"]), ListArg("method", ["ask"]), StringArg("message")],
            [4, ListArg("type", ["input"]), ListArg("method", ["read"]), TargetArg("target"), DefaultArg("objective"), IntegerArg("default")]
        ]
    
    def execute(self, execute_at, execute_by):
        if self.pargs["type"] == "objectives":
            self.execute_objectives(execute_at, execute_by)
        elif self.pargs["type"] == "players":
            self.execute_players(execute_at, execute_by)
        elif self.pargs["type"] == "input":
            self.execute_input(execute_at, execute_by)

    def execute_objectives(self, execute_at, execute_by):
        if self.pargs["method"] == "add":
            app.world.add_objective(self.pargs["objective"])
        elif self.pargs["method"] == "remove":
            app.world.remove_objective(self.pargs["objective"])

    def find_or_create_entities(self, target, execute_at, execute_by):
        try:
            entities = app.world.find_entities(target, execute_at, execute_by)
        except Exception as e:
            if target.is_name:
                entities = [ScoreEntity(target.args["name"])]
                app.world.set_entity(entities[0])

            else:
                raise NoTargetsException()
        
        return entities
        

    def execute_players(self, execute_at, execute_by):
        entities = self.find_or_create_entities(self.pargs["target"], execute_at, execute_by)

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
                current = app.world.get_score(e, self.pargs["objective"], 0)

                value = current + self.pargs["value"]
                app.world.set_score(e, self.pargs["objective"], value)
            elif method == "remove":
                current = app.world.get_score(e, self.pargs["objective"], 0)

                value = current - self.pargs["value"]
                app.world.set_score(e, self.pargs["objective"], value)
            elif method == "operation":
                score_a = app.world.get_score(e, self.pargs["objective"], 0)

                for other in self.find_or_create_entities(self.pargs["target_b"], execute_at, execute_by):
                    score_b = app.world.get_score(other, self.pargs["objective_b"], 0)

                    score_new = self.evaluate_operator(score_a, score_b, self.pargs["operator"])

                    if type(score_new) is tuple:
                        app.world.set_score(e, self.pargs["objective"], score_new[0])
                        app.world.set_score(other, self.pargs["objective"], score_new[1])
                    else:
                        app.world.set_score(e, self.pargs["objective"], score_new)

    def execute_input(self, execute_at, execute_by):
        method = self.pargs["method"]

        if method == "ask":
            message = self.pargs.get("message", "")
            app.interpreter.set_input(input(message))
        elif method == "read":
            entities = app.world.find_entities(self.pargs["target"], execute_at, execute_by)
            score, newv = app.interpreter.read_input()

            if score is None:
                if "default" in self.pargs:
                    score = self.pargs["default"]
                else:
                    score = 0

            for e in entities:
                app.world.set_score(e, self.pargs["objective"], score)
            
            app.interpreter.set_input(newv)

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