from cmu_graphics import *





def settings_redrawAll(app):
  drawLabel('settings', 100, 100)

def settings_onKeyPress(app, key):
  if key in ['escape', 'esc']:
    setActiveScreen('splash')
