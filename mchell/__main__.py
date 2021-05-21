# Hide pygame start message
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from app import main_app as app
from commands import *
import sys

app.interpreter.start()

if app.has_camera:
    app.camera.main_loop()