import getopt
import sys
import os

class App:
    def __init__(self, args):
        self.opts, self.args = getopt.getopt(args, "f:c")

    
        self.main_function = None
        self.directory = None
        self.has_camera = False
        self.proccess_arguments()

        self.is_shell = self.main_function is None

    def proccess_arguments(self):
        for o, v in self.opts:
            if o == "-f":
                self.main_function = v
            if o == "-d":
                self.directory = v
            if o == "-c":
                self.has_camera = True
        
        if len(self.args) == 1:
            self.main_function = self.args[0]

        if self.directory is None:
            if self.main_function is None:
                self.directory = os.getcwd()
            else:
                self.directory = os.path.dirname(self.main_function)
    
    def start(self):
        from camera import Camera
        from interpreter import Interpreter

        self.interpreter = Interpreter(self.is_shell)
        self.world = self.interpreter.world

        if self.has_camera:
            self.camera = Camera()

main_app = App(sys.argv[1:])
main_app.start()