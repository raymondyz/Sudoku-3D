from cmu_graphics import *

from ui import Button
from game3D import *

import string

# TODO PROTOTYPE, FIX CODE LATER
# TODO PROTOTYPE, FIX CODE LATER
# TODO PROTOTYPE, FIX CODE LATER



def drawStartButton(app):
  DISP_CENTER = app.startButtonPos
  
  sideLen = app.startButtonSize
  p1 = Vector3D(sideLen/2, sideLen/2, sideLen/2) + DISP_CENTER
  p2 = Vector3D(sideLen/2, sideLen/2, -sideLen/2) + DISP_CENTER
  p3 = Vector3D(sideLen/2, -sideLen/2, sideLen/2) + DISP_CENTER
  p4 = Vector3D(sideLen/2, -sideLen/2, -sideLen/2) + DISP_CENTER
  p5 = Vector3D(-sideLen/2, sideLen/2, sideLen/2) + DISP_CENTER
  p6 = Vector3D(-sideLen/2, sideLen/2, -sideLen/2) + DISP_CENTER
  p7 = Vector3D(-sideLen/2, -sideLen/2, sideLen/2) + DISP_CENTER
  p8 = Vector3D(-sideLen/2, -sideLen/2, -sideLen/2) + DISP_CENTER

  drawLine(*getLine3D(app, p1, p2, DISP_CENTER))
  drawLine(*getLine3D(app, p2, p4, DISP_CENTER))
  drawLine(*getLine3D(app, p4, p3, DISP_CENTER))
  drawLine(*getLine3D(app, p3, p1, DISP_CENTER))
  drawLine(*getLine3D(app, p4, p8, DISP_CENTER))
  drawLine(*getLine3D(app, p7, p8, DISP_CENTER))
  drawLine(*getLine3D(app, p7, p3, DISP_CENTER))
  drawLine(*getLine3D(app, p6, p8, DISP_CENTER))
  drawLine(*getLine3D(app, p2, p6, DISP_CENTER))


def stepStartAnimation(app):
  if app.startButtonPos.x <= 400:
    setActiveScreen('game3D')
  app.angleX = (app.angleX - 10) % 90
  app.startButtonSize = min(450, app.startButtonSize + 17)
  app.startButtonPos -= (10, 0, 0)
  # pass


def splash_onAppStart(app):
  pass

def splash_onScreenActivate(app):
  app.startButtonSize = 100
  app.startButtonPos = Vector3D(600, 400)
  app.startText = 'S  T  A  R  T'
  app.runStartAni = False

  app.angleY = 30

def splash_onStep(app):

  if app.runStartAni:
    stepStartAnimation(app)
  else:
    app.angleX = (app.angleX - 1) % 90

def splash_onMouseMove(app, mouseX, mouseY):
  if not app.runStartAni:
    if distance(mouseX, mouseY, *app.startButtonPos.list(2)) < 100:
      app.startButtonSize = 120
      app.startText = '[            ]'
    else:
      app.startButtonSize = 100
      app.startText = 'S  T  A  R  T'

def splash_onMousePress(app, mouseX, mouseY):
  if (not app.runStartAni) and distance(mouseX, mouseY, *app.startButtonPos.list(2)) < 100:
    app.runStartAni = True
    app.startButtonSize = 120

def splash_redrawAll(app):
  drawStartButton(app)
  
  if not app.runStartAni:
    drawLabel(app.startText, 600, 400, size=64, bold=True, fill='black', border='white', borderWidth = 3)

def splash_onKeyPress(app, key):
  if key == 'p':
    setActiveScreen('game3D')