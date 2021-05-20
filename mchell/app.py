import getopt
import sys

class App:
    def __init__(self, args):
        self.opts, self.args = getopt.getopt(args, "")
    
    def start(self):
        from camera import Camera
        from interpreter import Interpreter

        self.camera = Camera()
        self.interpreter = Interpreter()
        self.world = self.interpreter.world

main_app = App(sys.argv[1:])
main_app.start()