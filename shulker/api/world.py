import uuid
from math import sqrt

from shulker.api.error import UnknownObjectiveException, NoTargetsException

class World:
    def __init__(self):
        self.blocks = {}
        self.entities = {}
        self.scoreboards = {}

    def set_block(self, coordinates, block):
        self.blocks[coordinates] = block
    
    def get_block(self, coordinates):
        if coordinates in self.blocks:
            return self.blocks[coordinates]
        return Block("air", 0 )

    def set_entity(self, entity):
        self.entities[entity] = entity
    
    def kill_entity(self, entity):
        if entity in self.entities:
            del self.entities[entity]

    def find_entities(self, target, execute_at, execute_by, need_target = True):
        entities = []
        for e in self.entities.values():
            if target.match(e, execute_at, execute_by):
                entities.append(e)

        if need_target and len(entities) == 0:
            raise NoTargetsException()

        return target.sort(entities, execute_at)

    def add_objective(self, objective):
        if objective not in self.scoreboards:
            self.scoreboards[objective] = Scoreboard(objective)

    def remove_objective(self, objective):
        if objective in self.scoreboards:
            del self.scoreboards[objective]

    def set_score(self, entity, objective, value):
        if objective in self.scoreboards:
            self.scoreboards[objective].set_score(entity, value)
        else:
            raise UnknownObjectiveException(objective)

    def reset_score(self, entity, objective = None):
        if objective:
            if objective in self.scoreboards:
                self.scoreboards[objective].reset_score(entity)
            else:
                raise UnknownObjectiveException(objective)
        else:
            for sb in self.scoreboards.values():
                sb.reset_score(entity)

    def get_score(self, entity, objective, default = None):
        if objective in self.scoreboards:
            score = self.scoreboards[objective].get_score(entity)
            if score is None:
                return default
            return score
        else:
            raise UnknownObjectiveException(objective)

class Scoreboard:
    def __init__(self, objective):
        self.objective = objective
        self.scores = {}
    
    def set_score(self, entity, value):
        self.scores[entity] = value
    
    def reset_score(self, entity):
        if entity in self.scores:
            del self.scores[entity]

    def get_score(self, entity):
        if entity in self.scores:
            return self.scores[entity]
        return None

    def __str__(self):
        s = "<Scoreboard {}>".format(self.objective)
        for k, v in self.scores.items():
            s += "\n"
            s += "<Value {}:{}>".format(k.display_name(), v)
        return s

class Block:
    def __init__(self, identifier, data):
        self.identifier = identifier
        self.data = data

    def __str__(self):
        return "<Block {}:{}>".format(self.identifier, self.data)

    def __eq__(self, other):
        return self.identifier == other.identifier and (self.data == -1 or other.data == -1 or self.data == other.data)

class Entity:
    def __init__(self, identifier, coordinates, name = None, euuid = None):
        if euuid is None:
            euuid = uuid.uuid4()
        
        self.uuid = euuid
        self.coordinates = coordinates
        self.identifier = identifier
        self.name = name
        self.tags = []

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag):
        if tag[0] == "!":
            return not tag[1:] in self.tags
        else:
            return tag in self.tags
    
    def teleport(self, coordinates):
        self.coordinates = coordinates

    def distance(self, coordinates):
        return self.coordinates.distance(coordinates)

    def __str__(self):
        return "<Entity {}:{}> @ {}".format(self.identifier, self.name, self.coordinates)

    def display_name(self):
        return self.identifier if self.name is None else self.name
    
    def __eq__(self, other):
        return self.uuid == other.uuid

    def __hash__(self):
        return hash(self.uuid) 