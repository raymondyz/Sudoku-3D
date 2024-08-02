from cmu_graphics import *



def drawHelpText(app):
  x = 70
  y = 100
  dy = 30
  size = 24
  drawLabel('3D Sudoku Rules:', x, y, align='top-left', size=size, bold=True)
  y += dy
  drawLabel('For a 9x9x9 3D board, each slice in every orientation must satisfy normal 2D Sudoku rules.', x, y, align='top-left', size=size)
  y += dy
  drawLabel('Each "group" must contain the numbers from 1 - 9 and cannot have any duplicates.', x, y, align='top-left', size=size)
  y += dy
  drawLabel('Every column of 9x1x1 stack of numbers, in any orientation, is considered a group.', x, y, align='top-left', size=size)
  y += dy
  drawLabel('So every straight line must contain the numbers 1 - 9.', x, y, align='top-left', size=size)
  y += dy
  drawLabel('Every 3x3x1 "block" in any orientation is also considered a group, and so must have the numbers 1-9', x, y, align='top-left', size=size)
  y += dy
  drawLabel('These blocks are shown both on the 3D view and the 2D view, separated by dividers', x, y, align='top-left', size=size)

  y += 2*dy
  drawLabel('Controls:', x, y, align='top-left', size=size, bold=True)
  y += dy
  drawLabel('V: Change view from 3D <-> 2D', x, y, align='top-left', size=size)
  y += dy
  drawLabel('P: Return to splash screen', x, y, align='top-left', size=size)
  y += dy
  drawLabel('W, A, S, D: move selection within current slice', x, y, align='top-left', size=size)
  y += dy
  drawLabel('Q, E: move selected slice forward/backward', x, y, align='top-left', size=size)
  y += dy
  drawLabel('Hold Z: Activate multi-select mode', x, y, align='top-left', size=size)
  y += dy
  drawLabel('Number Keys: Toggle pencil mark for that number', x, y, align='top-left', size=size)
  y += dy
  drawLabel('Shift + Number: set number at selected location', x, y, align='top-left', size=size)
  y += dy
  drawLabel('Delete: remove number', x, y, align='top-left', size=size)








def help_onMousePress(app, mouseX, mouseY):
  app.splashBtn.updateActive(mouseX, mouseY, True)
  if app.splashBtn.checkClicked(mouseX, mouseY):
    setActiveScreen('splash')

def help_onMouseRelease(app, mouseX, mouseY):
  app.splashBtn.updateActive(mouseX, mouseY, False)

def help_onMouseHover(app, mouseX, mouseY):
  app.splashBtn.updateHover(mouseX, mouseY)
  

def help_redrawAll(app):
  drawHelpText(app)
  app.splashBtn.draw()



def help_onKeyPress(app, key):
  if key in ['escape', 'esc']:
    setActiveScreen('splash')
