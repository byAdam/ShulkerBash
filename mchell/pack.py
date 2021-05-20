import os
import pygame

class Pack:
    def __init__(self, path):
        self.path = path
        self.blocks = {}
        self.read_blocks()

    def read_blocks(self):
        ## Todo: Read blocks.json folder instead
        for block in os.listdir(self.path):
            block_name = os.path.splitext(block)[0]
            
            block_image = pygame.image.load(os.path.join(self.path, block))
    
            ## Todo: Make sure this is nearest neighbor scaling
            block_image = pygame.transform.scale(block_image, (64, 64))

            self.blocks[block_name] = block_image