import uuid
from math import sqrt

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
        self.entities[entity.uuid] = entity
    
    def kill_entity(self, entity):
        if entity.uuid in self.entities:
            del self.entities[entity.uuid]

    def find_entities(self, target, execute_at, execute_by):
        entities = []
        for e in self.entities.values():
            if target.match(e, execute_at, execute_by):
                entities.append(e)
        return target.sort(entities, execute_at)

class Block:
    def __init__(self, identifier, data):
        self.identifier = identifier
        self.data = data

    def __str__(self):
        return "<Block {}:{}>".format(self.identifier, self.data)

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
    
    def teleport(self, coordinates):
        pass

    def distance(self, coordinates):
        return self.coordinates.distance(coordinates)

    def __str__(self):
        return "<Entity {}:{}> @ {}".format(self.identifier, self.name, self.coordinates)

    def display_name(self):
        return self.identifier if self.name is None else self.name