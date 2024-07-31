from cmu_graphics import *
import math

from graphics import *
from sudoku import *
from sudokuUtility import isInsideQuad2D

def rotate3D(pos3D: Vector3D, angX: float, angY: float, axisPos3D: Vector3D = Vector3D(0, 0, 0)) -> Vector3D:
  pos3D = pos3D.rotatedY(angY, axisPos3D)
  pos3D = pos3D.rotatedX(angX, axisPos3D)
  return pos3D




# Input: index pos of cell
# Output: unrotated pixel vertex (corner) position centered at (0,0,0)
def getPixelPos(app, index3D: Vector3D) -> Vector3D:
  translate = 0.5 * app.BOARD_SIZE * app.CELL_SIZE

  pos3D = (index3D * app.CELL_SIZE) - ((translate,) * 3)
  return pos3D

# Input: unrotated pixel pos centered at (0,0,0)
# Output: rotated pixel pos centered at (0,0,0)
def getRotatedPos(app, pos3D: Vector3D, axis3D: Vector3D = Vector3D(0, 0, 0)) -> Vector3D:
  pos3D = rotate3D(pos3D, math.radians(app.angleY), math.radians(app.angleX), axis3D)
  return pos3D

# Input: index pos of cell
# Output: rotated pixel pos of cell corner (untranslated)
def getCellDispVertexPos(app, index3D: Vector3D) -> Vector3D:
  unrotPos3D = getPixelPos(app, index3D)
  rotPos3D = getRotatedPos(app, unrotPos3D)
  
  return rotPos3D

# Input: index pos of cell
# Output: rotated pixel pos of cell center (untranslated)
def getCellDispCenterPos(app, index3D: Vector3D) -> Vector3D:

  unrotPos3D = getPixelPos(app, index3D)
  # translate to center
  unrotPos3D = unrotPos3D + ((0.5 * app.CELL_SIZE,) * 3)
  rotPos3D = getRotatedPos(app, unrotPos3D)

  return rotPos3D


# Input: unrotated pixel pos
# Output: x1, y1, x2, y2 needed to draw rotated line
def getLine3D(app, startPos: Vector3D, endPos: Vector3D, axisPos: Vector3D = Vector3D(0, 0, 0)) -> tuple[float]:
  startPos = getRotatedPos(app, startPos, axisPos)
  endPos = getRotatedPos(app, endPos, axisPos)
  return (startPos.x, startPos.y, endPos.x, endPos.y)

# Input: cell index start and end
# Output, x1, y1, x2, y2 needed to draw rotated line on main board
def getLineOnBoard(app, index1: Vector3D, index2: Vector3D):
  DISP_CENTER = app.DIMENSIONS['mainBoardCenter']

  return getLine3D(app, getPixelPos(app, index1) + DISP_CENTER, getPixelPos(app, index2) + DISP_CENTER, DISP_CENTER)







# TODO WORK IN PROGRESS
# TODO WORK IN PROGRESS
def drawCellValue(app, cellCenterDisp3D: Vector3D, value: str = '') -> None:
  drawLabel(value, cellCenterDisp3D.x, cellCenterDisp3D.y)

def drawCell(app, index3D: Vector3D, dispCenter3D: Vector3D) -> None:
  VALUE_SIZE = 20
  MARKING_SIZE = 10

  cell: Cell = app.board.getCell(index3D)
  value = cell.get()
  markings = cell.markings

  # return if nothing to draw
  if value == None and len(markings) == 0:
    return

  # get cell display position
  cellVertexPos3D = getCellDispVertexPos(app, index3D)
  cellCenterPos3D = getCellDispCenterPos(app, index3D)
  # translate to center of display
  cellVertexPos3D = cellVertexPos3D + dispCenter3D
  cellCenterPos3D = cellCenterPos3D + dispCenter3D

  # draw cell text
  color = 'black' if cell.isLegal else 'red'
  dispText = str(value) if value != None else ''

  drawLabel(dispText, cellCenterPos3D.x, cellCenterPos3D.y, fill=color, size=VALUE_SIZE)

# Called by redrawAll() -> drawMainBoard()
def drawMainBoardCubeOutline(app) -> None:
  DISP_CENTER = app.DIMENSIONS['mainBoardCenter']

  color = 'black'
  if app.isBoardSolved:
    color = 'green'
  elif app.hasIllegalCell:
    color = 'red'

  
  sideLen = 450
  p1 = Vector3D(sideLen/2, sideLen/2, sideLen/2) + DISP_CENTER
  p2 = Vector3D(sideLen/2, sideLen/2, -sideLen/2) + DISP_CENTER
  p3 = Vector3D(sideLen/2, -sideLen/2, sideLen/2) + DISP_CENTER
  p4 = Vector3D(sideLen/2, -sideLen/2, -sideLen/2) + DISP_CENTER
  p5 = Vector3D(-sideLen/2, sideLen/2, sideLen/2) + DISP_CENTER
  p6 = Vector3D(-sideLen/2, sideLen/2, -sideLen/2) + DISP_CENTER
  p7 = Vector3D(-sideLen/2, -sideLen/2, sideLen/2) + DISP_CENTER
  p8 = Vector3D(-sideLen/2, -sideLen/2, -sideLen/2) + DISP_CENTER

  drawLine(*getLine3D(app, p1, p2, DISP_CENTER), fill=color)
  drawLine(*getLine3D(app, p2, p4, DISP_CENTER), fill=color)
  drawLine(*getLine3D(app, p4, p3, DISP_CENTER), fill=color)
  drawLine(*getLine3D(app, p3, p1, DISP_CENTER), fill=color)
  drawLine(*getLine3D(app, p4, p8, DISP_CENTER), fill=color)
  drawLine(*getLine3D(app, p7, p8, DISP_CENTER), fill=color)
  drawLine(*getLine3D(app, p7, p3, DISP_CENTER), fill=color)
  drawLine(*getLine3D(app, p6, p8, DISP_CENTER), fill=color)
  drawLine(*getLine3D(app, p2, p6, DISP_CENTER), fill=color)

# Called by drawMainBoard()
# Action: draws '#' cross on selected plane
def drawMainBoardCross(app) -> None:
  direction = app.planeDirection
  x, y, z = (app.selectedCell + (0.5, 0.5, 0.5)).list(3)
  color = 'black'
  if app.isBoardSolved:
    color = 'green'
  elif app.hasIllegalCell:
    color = 'red'

  if direction == 0:
    drawLine(*getLineOnBoard(app, Vector3D(x, 0, 3), Vector3D(x, 9, 3)), fill=color)
    drawLine(*getLineOnBoard(app, Vector3D(x, 0, 6), Vector3D(x, 9, 6)), fill=color)
    drawLine(*getLineOnBoard(app, Vector3D(x, 3, 0), Vector3D(x, 3, 9)), fill=color)
    drawLine(*getLineOnBoard(app, Vector3D(x, 6, 0), Vector3D(x, 6, 9)), fill=color)

  if direction == 1:
    drawLine(*getLineOnBoard(app, Vector3D(3, y, 0), Vector3D(3, y, 9)), fill=color)
    drawLine(*getLineOnBoard(app, Vector3D(6, y, 0), Vector3D(6, y, 9)), fill=color)
    drawLine(*getLineOnBoard(app, Vector3D(0, y, 3), Vector3D(9, y, 3)), fill=color)
    drawLine(*getLineOnBoard(app, Vector3D(0, y, 6), Vector3D(9, y, 6)), fill=color)
  
  if direction == 2:
    drawLine(*getLineOnBoard(app, Vector3D(0, 3, z), Vector3D(9, 3, z)), fill=color)
    drawLine(*getLineOnBoard(app, Vector3D(0, 6, z), Vector3D(9, 6, z)), fill=color)
    drawLine(*getLineOnBoard(app, Vector3D(3, 0, z), Vector3D(3, 9, z)), fill=color)
    drawLine(*getLineOnBoard(app, Vector3D(6, 0, z), Vector3D(6, 9, z)), fill=color)



# Called by game3D_redrawAll()
def drawMainBoard(app) -> None:
  DISP_CENTER = app.DIMENSIONS['mainBoardCenter']
  DISP_SIZE = app.DIMENSIONS['mainBoardSize']

  # draw bounding box
  # drawRect(DISP_CENTER.x-0.5*DISP_SIZE.x, DISP_CENTER.y-0.5*DISP_SIZE.y, DISP_SIZE.x, DISP_SIZE.y, fill=None, border = 'red', borderWidth = 3)

  # TODO TESTING: draw dot indicating (0,0,0) on board
  x, y = getCellDispVertexPos(app, Vector3D(0, 0, 0)).list(2)
  drawCircle(x+DISP_CENTER.x, y+DISP_CENTER.y, 5, fill='blue')

  # TODO TESTING: draw dot at selected cell
  x, y = getCellDispCenterPos(app, app.selectedCell).list(2)
  drawCircle(x+DISP_CENTER.x, y+DISP_CENTER.y, 5, fill='green')

  # draw board cube outline
  drawMainBoardCubeOutline(app)

  # draw plane
  drawMainBoardCross(app)

  # draw cells
  for x in range(app.BOARD_SIZE):
    for y in range(app.BOARD_SIZE):
      for z in range(app.BOARD_SIZE):

        # Only draw cell if in plane, unless app.showPlaneOnly == False
        if (not app.showPlaneOnly) or (x, y, z)[app.planeDirection] == app.selectedCell.list(3)[app.planeDirection]:
          drawCell(app, Vector3D(x, y, z), DISP_CENTER)

# Called by game3D_redrawAll()
def drawCubeButton(app) -> None:
  DISP_CENTER = app.DIMENSIONS['cubeButtonCenter']
  DISP_SIZE = app.DIMENSIONS['cubeButtonSize']
  sideLen = DISP_SIZE.x * 0.5

  # draw bounding box
  # drawRect(DISP_CENTER.x-0.5*DISP_SIZE.x, DISP_CENTER.y-0.5*DISP_SIZE.y, DISP_SIZE.x, DISP_SIZE.y, fill=None, border = 'red', borderWidth = 1)

  p1 = Vector3D(sideLen/2, sideLen/2, sideLen/2) + DISP_CENTER
  p2 = Vector3D(sideLen/2, sideLen/2, -sideLen/2) + DISP_CENTER
  p3 = Vector3D(sideLen/2, -sideLen/2, sideLen/2) + DISP_CENTER
  p4 = Vector3D(sideLen/2, -sideLen/2, -sideLen/2) + DISP_CENTER
  p5 = Vector3D(-sideLen/2, sideLen/2, sideLen/2) + DISP_CENTER
  p6 = Vector3D(-sideLen/2, sideLen/2, -sideLen/2) + DISP_CENTER
  p7 = Vector3D(-sideLen/2, -sideLen/2, sideLen/2) + DISP_CENTER
  p8 = Vector3D(-sideLen/2, -sideLen/2, -sideLen/2) + DISP_CENTER

  drawPolygon(*getLine3D(app, p1, p2, DISP_CENTER), *getLine3D(app, p4, p3, DISP_CENTER), fill=None, border='black')
  drawPolygon(*getLine3D(app, p3, p4, DISP_CENTER), *getLine3D(app, p8, p7, DISP_CENTER), fill=None, border='black')
  drawPolygon(*getLine3D(app, p8, p6, DISP_CENTER), *getLine3D(app, p2, p4, DISP_CENTER), fill=None, border='black')

  # TODO REWRITE USING CLASS, BAD IMPLEMENTATION
  if isInsideQuad2D(*getLine3D(app, p1, p2, DISP_CENTER), *getLine3D(app, p4, p3, DISP_CENTER), *app.mousePos.list(2)):
    drawPolygon(*getLine3D(app, p1, p2, DISP_CENTER), *getLine3D(app, p4, p3, DISP_CENTER), fill='red', border='black')

  elif isInsideQuad2D(*getLine3D(app, p3, p4, DISP_CENTER), *getLine3D(app, p8, p7, DISP_CENTER), *app.mousePos.list(2)):
    drawPolygon(*getLine3D(app, p3, p4, DISP_CENTER), *getLine3D(app, p8, p7, DISP_CENTER), fill='green', border='black')

  elif isInsideQuad2D(*getLine3D(app, p8, p6, DISP_CENTER), *getLine3D(app, p2, p4, DISP_CENTER), *app.mousePos.list(2)):
    drawPolygon(*getLine3D(app, p8, p6, DISP_CENTER), *getLine3D(app, p2, p4, DISP_CENTER), fill='blue', border='black')

# TODO REWRITE, lots of repeated code from drawCubeButton(), add to own class
def mouseUpdateCubeButton(app, mousePos: Vector3D) -> None:
  DISP_CENTER = app.DIMENSIONS['cubeButtonCenter']
  DISP_SIZE = app.DIMENSIONS['cubeButtonSize']
  sideLen = DISP_SIZE.x * 0.5

  p1 = Vector3D(sideLen/2, sideLen/2, sideLen/2) + DISP_CENTER
  p2 = Vector3D(sideLen/2, sideLen/2, -sideLen/2) + DISP_CENTER
  p3 = Vector3D(sideLen/2, -sideLen/2, sideLen/2) + DISP_CENTER
  p4 = Vector3D(sideLen/2, -sideLen/2, -sideLen/2) + DISP_CENTER
  p5 = Vector3D(-sideLen/2, sideLen/2, sideLen/2) + DISP_CENTER
  p6 = Vector3D(-sideLen/2, sideLen/2, -sideLen/2) + DISP_CENTER
  p7 = Vector3D(-sideLen/2, -sideLen/2, sideLen/2) + DISP_CENTER
  p8 = Vector3D(-sideLen/2, -sideLen/2, -sideLen/2) + DISP_CENTER

  if isInsideQuad2D(*getLine3D(app, p1, p2, DISP_CENTER), *getLine3D(app, p4, p3, DISP_CENTER), *mousePos.list(2)):
    app.planeDirection = 0
  elif isInsideQuad2D(*getLine3D(app, p3, p4, DISP_CENTER), *getLine3D(app, p8, p7, DISP_CENTER), *mousePos.list(2)):
    app.planeDirection = 1
  elif isInsideQuad2D(*getLine3D(app, p8, p6, DISP_CENTER), *getLine3D(app, p2, p4, DISP_CENTER), *mousePos.list(2)):
    app.planeDirection = 2

# Called by game3D_redrawAll()
def drawDebugTooltip(app) -> None:
  DISP_POS = app.DIMENSIONS['debugTooltipPos']
  DISP_SIZE = app.DIMENSIONS['debugTooltipSize']

  # draw bounding box
  drawRect(DISP_POS.x, DISP_POS.y, DISP_SIZE.x, DISP_SIZE.y, fill=None, border = 'red', borderWidth = 1)

  drawLabel(f'AngleX: {int(app.angleX)}', DISP_POS.x+10, DISP_POS.y+10, align = 'top-left')
  drawLabel(f'AngleY: {int(app.angleY)}', DISP_POS.x+10, DISP_POS.y+30, align = 'top-left')




# EVENT HANDLERS

# Called by game3D_onMouseDrag()
def mouseRotateMainBoard(app, currMousePos2D: Vector3D) -> None:
  DISP_CENTER = app.DIMENSIONS['mainBoardCenter']
  DISP_SIZE = app.DIMENSIONS['mainBoardSize']

  # No action if mouse outside of drag area
  if not (-0.5*DISP_SIZE.x <= currMousePos2D.x-DISP_CENTER.x <= 0.5*DISP_SIZE.x):
    return
  if not (-0.5*DISP_SIZE.y <= currMousePos2D.y-DISP_CENTER.y <= 0.5*DISP_SIZE.y):
    return

  app.angleX -= app.mouseSensitivity*(currMousePos2D.x - app.mousePos.x)
  app.angleY += app.mouseSensitivity*(currMousePos2D.y - app.mousePos.y)

  # Prevents angle from exceeding 90 degrees
  app.angleX = min(90, max(0, app.angleX))
  app.angleY = min(90, max(0, app.angleY))


# Convert 3D index to 2D index
# TODO, STOLEN FROM game2D, GENERALIZE INTO UTILS CLASS
def getIndex2D(app, index3D: Vector3D):
  if app.planeDirection == 0:
    return Vector3D(index3D.z, index3D.y)
  elif app.planeDirection == 1:
    return Vector3D(index3D.z, index3D.x)
  elif app.planeDirection == 2:
    return Vector3D(index3D.x, index3D.y)

# Convert 2D index to 3D index
# TODO, STOLEN FROM game2D, GENERALIZE INTO UTILS CLASS
def getIndex3D(app, index2D: Vector3D):
  if app.planeDirection == 0:
    return Vector3D(app.selectedCell.x, index2D.y, index2D.x)
  elif app.planeDirection == 1:
    return Vector3D(index2D.y, app.selectedCell.y, index2D.x)
  elif app.planeDirection == 2:
    return Vector3D(index2D.x, index2D.y, app.selectedCell.z)

# Move selected plane
def keyShiftPlane3D(app, key: str) -> None:

  # Move plane forward
  if key in ['e']:
    dIndex = [0, 0, 0]
    dIndex[app.planeDirection] = 1
    app.selectedCell += dIndex

  # Move plane backward
  if key in ['q']:
    dIndex = [0, 0, 0]
    dIndex[app.planeDirection] = -1
    app.selectedCell += dIndex
  
  # Wrap plane around if outside board
  app.selectedCell %= app.BOARD_SIZE

# Move selection within selected plane
def keyMoveSelection3D(app, key: str) -> None:
  index2D = getIndex2D(app, app.selectedCell)

  # Move selection up
  if key in ['w']:
    app.selectedCell = getIndex3D(app, index2D + (0, -1, 0))

  # Move selection down
  if key in ['s']:
    app.selectedCell = getIndex3D(app, index2D + (0, 1, 0))

  # Move selection right
  if key in ['d']:
    app.selectedCell = getIndex3D(app, index2D + (1, 0, 0))
  
  # Move selection left
  if key in ['a']:
    app.selectedCell = getIndex3D(app, index2D + (-1, 0, 0))
  
  # Wrap selection around if outside board
  app.selectedCell %= app.BOARD_SIZE


# ================================================
# ==================== game3D ====================
# ================================================

def game3D_onScreenActivate(app):
  app.multiSelected.clear()
  app.multiSelect = False

def game3D_onMouseMove(app, mouseX, mouseY):
  app.mousePos = Vector3D(mouseX, mouseY)

def game3D_onMousePress(app, mouseX, mouseY):
  app.mousePos = Vector3D(mouseX, mouseY)

  mouseUpdateCubeButton(app, app.mousePos)

def game3D_onMouseDrag(app, mouseX, mouseY):
  mouseRotateMainBoard(app, Vector3D(mouseX, mouseY))

  app.mousePos = Vector3D(mouseX, mouseY)

def game3D_onKeyPress(app, key):

  # Shifts plane forward/backward
  keyShiftPlane3D(app, key)

  # Move selection within plane
  keyMoveSelection3D(app, key)


  if key in ['v']:
    setActiveScreen('game2D')
  if key in ['p']:
    setActiveScreen('splash')
  

  

  

# DISPLAY HANDLERS

def game3D_redrawAll(app):
  drawMainBoard(app)
  drawCubeButton(app)
  # drawDebugTooltip(app)