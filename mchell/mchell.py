import getopt
import pygame
from camera import Camera

class App:
    def __init__(self, args):
        self.opts, self.args = getopt.getopt(args, "h")
        self.camera = Camera(self)