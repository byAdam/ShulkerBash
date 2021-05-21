import pygame
from pack import Pack
from app import main_app as app
import threading
from enum import Enum

class CameraState(Enum):
    INACTIVE = 0
    STARTING = 1
    RUNNING = 2
    STOPPING = 3
    ENDING = 4

class Camera():
    ## Block Pixels
    BP = 64

    def __init__(self, coordinates = (0, 0, 0), dimensions = (10, 10, 5)):
        pygame.init()

        self.coordinates = coordinates
        self.dimensions = dimensions
        self.pack = Pack("pack")
        self.state = CameraState.INACTIVE


    def draw_block(self, block, coordinates):
        texture = self.pack.blocks["unknown"]
        if block in self.pack.blocks:
            texture = self.pack.blocks[block]

        self.screen.blit(texture, coordinates)

    def draw_blocks(self, blocks):
        for x in range(0, self.dimensions[0]):
            for y in range(0, self.dimensions[1]):
                self.draw_block(get_block((x, y)), coordinates)

    def get_block(self, block):
        return ""

    def start(self):
        self.state = CameraState.STARTING

    def stop(self):
        self.state = CameraState.STOPPING

    def end(self):
        self.state = CameraState.ENDING

    def main_loop(self):
        ## Until end
        while self.state != CameraState.ENDING:
            if self.state == CameraState.STARTING:
                self.screen = pygame.display.set_mode([self.dimensions[0] * self.BP, self.dimensions[0] * self.BP])
                self.state = CameraState.RUNNING

            if self.state == CameraState.STOPPING:
                self.state = CameraState.INACTIVE
                pygame.display.quit()

            if self.state == CameraState.RUNNING:
                # Did the user click the window close button?
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.stop()

                pygame.display.flip()
        
        pygame.display.quit()
        pygame.quit()