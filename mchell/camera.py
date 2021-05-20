import pygame
from pack import Pack

class Camera():
    ## Block Pixels
    BP = 64

    def __init__(self, app, coords = (0, 0), dimensions = (10, 10, 5)):
        pygame.init()

        self.app = app
        self.coords = coords
        self.dimensions = dimensions
        self.pack = Pack("pack")
        
        self.running = False

    def draw_block(self, block, coords):
        texture = self.pack.blocks["unknown"]
        if block in self.pack.blocks:
            texture = self.pack.blocks[block]

        self.screen.blit(texture, coords)

    def draw_blocks(self, blocks):
        for x in range(0, self.dimensions[0]):
            for y in range(0, self.dimensions[1]):
                self.draw_block(get_block((x, y)), coords)

    def get_block(self, block):
        return ""

    def start(self):
        self.running = True
        self.screen = pygame.display.set_mode([self.dimensions[0] * self.BP, self.dimensions[0] * self.BP])
        self.main_loop()

    def stop(self):
        self.running = False
        pygame.quit()

    def main_loop(self):
        while self.running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

            pygame.display.flip()