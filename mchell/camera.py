import pygame
from pack import Pack
from app import main_app as app
import threading
from enum import Enum
from coordinates import Coordinates
from world import Block

class CameraState(Enum):
    INACTIVE = 0
    RUNNING = 1
    STOPPING = 2
    ENDING = 3

class Camera():
    ## Block Pixels
    BP = 64

    def __init__(self):
        self.set_position(Coordinates(0, 0, 0))
        self.set_dimensions(Coordinates(2, 2, 1))
        self.screen = None

        self.pack = Pack("pack")
        self.state = CameraState.INACTIVE


    def draw_block(self, block, coordinates):
        texture = self.pack.blocks["unknown"]
        if block in self.pack.blocks:
            texture = self.pack.blocks[block]

        self.screen.blit(texture, coordinates)

    def draw_blocks(self):
        for x in range(0, self.dimensions.x):
            for y in range(0, self.dimensions.y):
                ## Todo: Add z coordinate
                bx = self.coordinates.x + x
                by = self.coordinates.y + y

                for z in range(0, self.dimensions.z):
                    bz = self.coordinates.z + z
                    block = self.get_block(Coordinates(bx, by, bz)).identifier

                    if block != "air":
                        break
                
                coordinates = (x * self.BP, (self.dimensions.y - y - 1) * self.BP)

                self.draw_block(block, coordinates)

    def get_block(self, coordinates):
        return app.world.get_block(coordinates)

    def set_position(self, coordinates):
        self.coordinates = coordinates
    
    def set_dimensions(self, dimensions):
        self.dimensions = dimensions
        self.size = (self.dimensions.x * self.BP, self.dimensions.y * self.BP)

    def start(self):
        pygame.init()
        self.state = CameraState.RUNNING

    def stop(self):
        self.state = CameraState.STOPPING
        self.screen = None

    def end(self):
        self.state = CameraState.ENDING

    def main_loop(self):
        ## Until end
        while self.state != CameraState.ENDING:

            if self.state == CameraState.STOPPING:
                self.state = CameraState.INACTIVE
                pygame.display.quit()

            if self.state == CameraState.RUNNING:
                self.proccess_events()

                # Make sure it wasn't stopped
                if self.state == CameraState.RUNNING:
                    self.display_loop()

        pygame.display.quit()
        pygame.quit()

    def proccess_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.on_break(pygame.mouse.get_pos())
    
    def on_break(self, pos):
        rel_pos = (pos[0] // self.BP, (self.size[1] - pos[1]) // self.BP)
        x = self.coordinates.x + rel_pos[0]
        y = self.coordinates.y + rel_pos[1]

        for z in range(0, self.dimensions.z):
            bz = self.coordinates.z + z
            block = self.get_block(Coordinates(x, y, bz)).identifier

            if block != "air":
                coords = Coordinates(x, y, bz)
                app.world.set_block(coords, Block("air", 0))
                break

    def display_loop(self):
        if self.screen is None or self.screen.get_size() != self.size:
            self.screen = pygame.display.set_mode(self.size)

        self.draw_blocks()
        pygame.display.flip()