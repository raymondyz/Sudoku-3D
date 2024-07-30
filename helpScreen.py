from cmu_graphics import *





def help_redrawAll(app):
  drawLabel('help screen', 100, 100)

def help_onKeyPress(app, key):
  if key in ['escape', 'esc']:
    setActiveScreen('splash')
