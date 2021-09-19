import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from shulker.app import main_app as app
from shulker.commands import *

import sys

import signal

def signal_handler(signal, frame):
    app.exit()

def main():
    signal.signal(signal.SIGINT, signal_handler)
    app.interpreter.start()
    app.camera.main_loop()



if __name__ == "__main__":
    main()