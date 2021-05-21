import re
import random
from command import Command
from coordinates import Coordinates

class Target:
    def __init__(self, selector):
        self.selector = selector
        self.args = {
            "coordinates": Coordinates(), 
            "delta": Coordinates(), 
            "radius": [None, None],
            "tags": [],
            "sort": "nearest",
            "count": None,
            "self": False
        }

        self.process_selector()

    def process_selector(self):
        if self.selector[0] != "@":
            self.args["name"] = self.selector[0]
        else:
            ## Todo: Rewrite this whole section

            variable = self.selector[:2]
            raw_args = self.selector[3:-1]

            if raw_args:
                scores = re.match("{.*}", raw_args)
                if scores:
                    raw_args = re.sub("{.*}", "", raw_args)
                
                
                for arg in raw_args.split(","):
                    k, v = arg.split("=")

                    if k == "x":
                        self.args["coordinates"].update(x=v)
                    elif k == "y":
                        self.args["coordinates"].update(y=v)
                    elif k == "z":
                        self.args["coordinates"].update(z=v)
                    elif k == "dx":
                        self.args["delta"].update(x=v)
                    elif k == "dy":
                        self.args["delta"].update(y=v)
                    elif k == "dz":
                        self.args["delta"].update(z=v)
                    elif k == "rm":
                        self.args["radius"][0] = float(v)
                    elif k == "r":
                        self.args["radius"][1] = float(v)
                    elif k == "name":
                        self.args["name"] = v
                    elif k == "type":
                        self.args["type"] = v
                    elif k == "c":
                        self.args["count"] = int(v)
                    elif k == "scores":
                        self.args["scores"] = scores
                    elif k == "tag":
                        self.args["tags"].append(v)

            self.process_variable(self.selector[:2])
    
    def process_variable(self, var):
        if var == "@a":
            self.args["type"] = "player"
                
        elif var == "@p":
            self.args["count"] = 1
            self.args["type"] = "player"

        elif var == "@r":
            self.args["sort"] = "random"
        
        elif var == "@s":
            self.args["self"] = True
    
    def match(self, entity, execute_at, execute_by):
        ## If not same entity as executed_by
        if self.args["self"]:
            if execute_by is not None:
                if execute_by != entity:
                    return False

        coordinates = execute_at.merge(self.args["coordinates"])

        if "type" in self.args:
            if self.args["type"] != entity.identifier:
                return False
        
        if "name" in self.args:
            if self.args["name"] != entity.name:
                return False
        
        if self.args["radius"][0] is not None:
            if entity.distance(coordinates) < self.args["radius"][0]:
                return False

        if self.args["radius"][1] is not None:
            if entity.distance(coordinates) > self.args["radius"][1]:
                return False

        if self.args["delta"].has_absolute():
            delta = self.args["delta"]
            dx = coordinates.x + coordinates.parse_value(delta.x)
            dy = coordinates.y + coordinates.parse_value(delta.y)
            dz = coordinates.z + coordinates.parse_value(delta.z)

            if not coordinates.between(coordinates.x, dx, entity.coordinates.x):
                return False
            if not coordinates.between(coordinates.y, dy, entity.coordinates.y):
                return False
            if not coordinates.between(coordinates.z, dz, entity.coordinates.z):
                return False

        for tag in self.args["tags"]:
            if not entity.has_tag(tag):
                return False
                
        return True

    def sort(self, entities, execute_at):
        ## Sort list
        if self.args["sort"] == "nearest":
            entities.sort(key = lambda x: x.distance(execute_at))
        elif self.args["sort"] == "random":
            random.shuffle(entities)

        c = self.args["count"]

        ## Filter list by count
        if c is None:
            return entities
        elif c < 0:
            return entities[-c:]
        else:
            return entities[:c]