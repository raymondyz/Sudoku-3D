from cmu_graphics import *

from ui import Button



# TODO TESTING CODE

def splash_onAppStart(app):
  pass

def splash_onScreenActivate(app):
  pass

def splash_onStep(app):
  pass

def splash_redrawAll(app):
  drawLabel('hello', 100, 100, size=50)

def splash_onKeyPress(app, key):
  if key == 'p':
    setActiveScreen('game')