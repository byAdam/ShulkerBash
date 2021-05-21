import pygame
from pack import Pack
from app import main_app as app
import threading

class Camera():
    ## Block Pixels
    BP = 64

    def __init__(self, coordinates = (0, 0, 0), dimensions = (10, 10, 5)):
        pygame.init()

        self.coordinates = coordinates
        self.dimensions = dimensions
        self.pack = Pack("pack")
        self.starting = False
        self.stopping = False
        self.running = False

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
        self.starting = True

    def stop(self):
        self.stopping = True

    def main_loop(self):
        while True:
            if self.starting:
                self.starting = False
                self.screen = pygame.display.set_mode([self.dimensions[0] * self.BP, self.dimensions[0] * self.BP])
                self.running = True

            if self.stopping:
                self.stopping = False
                self.running = False
                pygame.display.quit()

            if self.running:
                # Did the user click the window close button?
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.stop()

                pygame.display.flip()