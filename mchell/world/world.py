class World:
    def __init__(self):
        self.blocks = {}
        self.entities = {}
        self.scoreboards = {}

    def set_block(self, coordinates, identifier, data):
        self.blocks[coordinates] = Block(identifier, data)
    
    def get_block(self, coordinates):
        if coordinates in self.blocks:
            return self.blocks[coordinates]
        return Block("air", 0 )

class Block:
    def __init__(self, identifier, data = 0):
        self.identifier = identifier
        self.data = data

    def __str__(self):
        return "{}:{}".format(self.identifier, self.data)