import getopt
import sys
import os
import threading

class App:
    def __init__(self, args):
        self.opts, self.args = getopt.getopt(args, "f:d:p:lehb")
    
        self.main_function = None
        self.directory = None
        self.is_looping = False
        self.show_errors = False
        self.camera = None
        self.debug = False
        self.pack = False
        self.is_exit = False

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
                self.show_errors = True
            if o == "-h":
                self.show_help()
            if o == "-b":
                self.debug = True
            if o == "-p":
                self.pack = v
        
        if len(self.args) == 1:
            self.main_function = self.args[0]

        if self.directory is None:
            if self.main_function is None:
                self.directory = os.getcwd()
            else:
                self.directory = os.path.dirname(self.main_function)

        if self.main_function is None:
            self.show_errors = True


    def show_help(self):
        with open(os.path.join(sys.path[0],"help.md")) as f:
            lines = f.readlines()
        print("".join(lines))

        self.exit()
    
    def start(self):
        from shulker.camera import Camera
        from shulker.interpreter import Interpreter
        
        self.interpreter = Interpreter(self.is_shell, self.is_looping)
        self.interpreter.read_functions_in_directory(self.directory)
        self.world = self.interpreter.world
        self.camera = Camera(self.pack)
    
    def exit(self):
        self.is_exit = True
        if self.camera is not None:
            self.camera.end()
        sys.exit(0)

main_app = App(sys.argv[1:])
main_app.start()