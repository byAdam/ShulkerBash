import os
import pygame
import json
import sys
from shulker.api.error import *

class Pack:
    def __init__(self, path):
        self.path = path

        try:
            self.block_textures = self.read_blocks()
            self.terrain = self.read_terrain()
            self.blocks = self.create_block_map()
        except:
            raise(InvalidResourcePackException(path))

    def read_blocks(self):
        blocks = {}

        with open(os.path.join(self.path, "blocks.json")) as f:
            data = json.load(f)
            for x in data:
                if "textures" in data[x]:
                    textures = data[x]["textures"]

                    if type(textures) is str:
                        blocks[x] = textures
                    else:
                        if "side" in textures:
                            blocks[x] = textures["side"]
                        elif "north" in textures:
                            blocks[x] = textures["north"]
        return blocks

    def read_terrain(self):
        terrain = {}

        with open(os.path.join(self.path, "textures/terrain_texture.json")) as f:
            data = json.load(f)
            
            tdata = data["texture_data"]

            for k, v in self.block_textures.items():
                texture = tdata[v]["textures"]

                if type(texture) is str:
                    terrain[k] = texture
                else:
                    if type(texture[0]) is str:
                        terrain[k] = texture[0]
                    else:
                        terrain[k] = texture[0]["path"]
        return terrain
    
    def create_block_map(self):
        blocks = {}

        for block_name in self.terrain:
            block_path = self.terrain[block_name]
            png_path = os.path.join(self.path, block_path) + ".png"

            try:
                block_image = pygame.image.load(png_path)
            except:
                continue

            block_image = pygame.transform.scale(block_image, (64, 64))
            blocks[block_name] = block_image
        return blocks


if __name__ == "__main__":
    Pack("resources")