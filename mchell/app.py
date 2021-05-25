import getopt
import sys
import os
import threading

class App:
    def __init__(self, args):
        self.opts, self.args = getopt.getopt(args, "f:d:leh")

    
        self.main_function = None
        self.directory = None
        self.is_looping = False
        self.hide_errors = False
        self.camera = None

        self.proccess_arguments()

        self.is_shell = self.main_function is None

    def proccess_arguments(self):
        for o, v in self.opts:
            if o == "-f":
                self.main_function = v
            if o == "-d":
                self.directory = v
            if o == "-l":
                self.is_looping = True
            if o == "-e":
                self.hide_errors = True
            if o == "-h":
                self.show_help()
        
        if len(self.args) == 1:
            self.main_function = self.args[0]

        if self.directory is None:
            if self.main_function is None:
                self.directory = os.getcwd()
            else:
                self.directory = os.path.dirname(self.main_function)

    def show_help(self):
        with open("help.md") as f:
            lines = f.readlines()
        print("".join(lines))

        self.exit()
    
    def start(self):
        from camera import Camera
        from interpreter import Interpreter

        self.interpreter = Interpreter(self.is_shell, self.is_looping)
        self.interpreter.read_functions(self.directory)
        self.world = self.interpreter.world
        self.camera = Camera()
    
    def exit(self):
        if self.camera is not None:
            self.camera.end()
        sys.exit(0)

main_app = App(sys.argv[1:])
main_app.start()