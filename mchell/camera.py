import pygame
from pack import Pack
from app import main_app as app
import threading
from enum import Enum
from coordinates import Coordinates

class CameraState(Enum):
    INACTIVE = 0
    STARTING = 1
    RUNNING = 2
    STOPPING = 3
    ENDING = 4

class Camera():
    ## Block Pixels
    BP = 64

    def __init__(self):
        pygame.init()
        
        self.coordinates = Coordinates(0, 0, 0)
        self.dimensions = Coordinates(2, 2, 0)

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

    def start(self, coordinates, dimensions):
        self.coordinates = coordinates
        self.dimensions = dimensions
        self.state = CameraState.STARTING

    def stop(self):
        self.state = CameraState.STOPPING

    def end(self):
        self.state = CameraState.ENDING

    def main_loop(self):
        ## Until end
        while self.state != CameraState.ENDING:
            if self.state == CameraState.STARTING:
                size = [self.dimensions.x * self.BP, self.dimensions.y * self.BP]
                self.screen = pygame.display.set_mode(size)
                self.state = CameraState.RUNNING

            if self.state == CameraState.STOPPING:
                self.state = CameraState.INACTIVE
                pygame.display.quit()

            if self.state == CameraState.RUNNING:
                # Did the user click the window close button?
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.stop()

                self.draw_blocks()
                pygame.display.flip()
        
        pygame.display.quit()
        pygame.quit()