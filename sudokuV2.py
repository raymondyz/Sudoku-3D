'''
TODO ROADMAP:

 - Move selection with keyboard
 - Check legal
 - Check Solved

 - Change plane direction with cube button

 - Select with mouse

FUTURE:
 - Make small cube clickable
 - 2D backsolver
 - choose between 9x9x9 or 4x4x4



'''



from cmu_graphics import *
import math

from graphics import Vector3D

from splashScreen import *


class Cell:
  def __init__(self, value: int = None) -> None:
    self.value: int = value
    self.isLocked: bool = False
    self.isLegal: bool = True
    self.markings: set[int] = set() # 'possible values' displayed, may be changed by player
    self.legals: set[int] = set()   # correct possible values
  
  def __repr__(self) -> str:
    return str(self.value)

  def set(self, value: int) -> bool:
    if self.isLocked:
      return False
    
    self.value = value
    return True
  
  def get(self) -> int:
    return self.value

class Sudoku3D:
  def __init__(self, size: int = 9) -> None:
    self.BOARD_SIZE: int = size
    self.board: list[list[list[Cell]]] = self.newBoard(self.BOARD_SIZE)

  def newBoard(self, size: int) -> list[list[list[Cell]]]:
    list3D = []
    for i in range(size):
      list2D = []
      for j in range(size):
        list1D = []
        for k in range(size):
          # cell = Cell(100*i + 10*j + k)
          cell = Cell()
          if (i+j+k) % 3 == 0:
            cell = Cell((i+j+k) % 10)
          cell.markings = {i, j, k}
          list1D.append(cell)
        list2D.append(list1D)
      list3D.append(list2D)
    return list3D
  
  def set(self, index: Vector3D, value: int) -> bool:
    cell = self.board[index.x][index.y][index.z]
    return cell.set(value)
  
  def get(self, index: Vector3D) -> int:
    cell = self.board[index.x][index.y][index.z]
    return cell.get()
  
  def getCell(self, index: Vector3D) -> int:
    cell = self.board[index.x][index.y][index.z]
    return cell
  
  def getBoard2D(self, plane: int, planeIndex: int) -> list[list[Cell]]:
    list2D = []
    for i in range(self.BOARD_SIZE):
      list1D = []
      for j in range(self.BOARD_SIZE):
        if plane == 0:
          list1D.append(self.board[planeIndex][i][j])
        elif plane == 1:
          list1D.append(self.board[i][planeIndex][j])
        elif plane == 2:
          list1D.append(self.board[j][i][planeIndex])
      list2D.append(list1D)
    return list2D

  
  def getIllegalCells(self) -> list[Cell]:
    # TODO FUTURE IMPLEMENTATION
    pass






def rotate(pos3D: Vector3D, angX: float, angY: float, axisPos3D: Vector3D = Vector3D(0, 0, 0)) -> Vector3D:
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
  pos3D = rotate(pos3D, math.radians(app.angleY), math.radians(app.angleX), axis3D)
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

  x1, y1 = getCellDispVertexPos(app, Vector3D(0, app.BOARD_SIZE, app.BOARD_SIZE)).list(2)
  x2, y2 = getCellDispVertexPos(app, Vector3D(0, 0, app.BOARD_SIZE)).list(2)
  drawLine(x1+DISP_CENTER.x, y1+DISP_CENTER.y,
           x2+DISP_CENTER.x, y2+DISP_CENTER.y)
  x3, y3 = getCellDispVertexPos(app, Vector3D(0, app.BOARD_SIZE, 0)).list(2)
  drawLine(x1+DISP_CENTER.x, y1+DISP_CENTER.y,
           x3+DISP_CENTER.x, y3+DISP_CENTER.y)
  x4, y4 = getCellDispVertexPos(app, Vector3D(app.BOARD_SIZE, app.BOARD_SIZE, app.BOARD_SIZE)).list(2)
  drawLine(x1+DISP_CENTER.x, y1+DISP_CENTER.y,
           x4+DISP_CENTER.x, y4+DISP_CENTER.y)

# Called by drawMainBoard()
# Action: draws '#' cross on selected plane
def drawMainBoardCross(app) -> None:
  direction = app.planeDirection
  x, y, z = (app.selectedCell + (0.5, 0.5, 0.5)).list(3)
  color = 'black'

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
  drawRect(DISP_CENTER.x-0.5*DISP_SIZE.x, DISP_CENTER.y-0.5*DISP_SIZE.y, DISP_SIZE.x, DISP_SIZE.y, fill=None, border = 'red', borderWidth = 3)

  # draw dot indicating (0,0,0) on board
  x, y = getCellDispVertexPos(app, Vector3D(0, 0, 0)).list(2)
  drawCircle(x+DISP_CENTER.x, y+DISP_CENTER.y, 5, fill='blue')

  # draw board cube outline
  drawMainBoardCubeOutline(app)

  # draw plane
  drawMainBoardCross(app)

  # draw cells
  for x in range(app.BOARD_SIZE):
    for y in range(app.BOARD_SIZE):
      for z in range(app.BOARD_SIZE):

        # Only draw cell if in plane
        if (x, y, z)[app.planeDirection] == app.selectedCell.list(3)[app.planeDirection]:
          drawCell(app, Vector3D(x, y, z), DISP_CENTER)

# Called by game3D_redrawAll()
def drawCubeButton(app) -> None:
  DISP_CENTER = app.DIMENSIONS['cubeButtonCenter']
  DISP_SIZE = app.DIMENSIONS['cubeButtonSize']
  sideLen = DISP_SIZE.x * 0.5

  # draw bounding box
  drawRect(DISP_CENTER.x-0.5*DISP_SIZE.x, DISP_CENTER.y-0.5*DISP_SIZE.y, DISP_SIZE.x, DISP_SIZE.y, fill=None, border = 'red', borderWidth = 1)

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


# Draw highlight on cell at index
def drawCellHighlight2D(app, index2D: Vector3D, color, opacity=100, borderColor=None, borderWidth=1):
  DISP_POS = app.DIMENSIONS['miniBoardPos']
  DISP_SIZE = app.DIMENSIONS['miniBoardSize']
  CELL_SIZE = DISP_SIZE / app.BOARD_SIZE

  drawRect(DISP_POS.x + CELL_SIZE.x * index2D.x, DISP_POS.y + CELL_SIZE.y * index2D.y, CELL_SIZE.x, CELL_SIZE.y, fill=color, opacity=opacity, border=borderColor, borderWidth=borderWidth)


# Called by game2D_redrawAll()
def drawMiniBoard(app) -> None:
  DISP_POS = app.DIMENSIONS['miniBoardPos']
  DISP_SIZE = app.DIMENSIONS['miniBoardSize']

  CELL_SIZE = DISP_SIZE / app.BOARD_SIZE
  VALUE_SIZE = 20
  MARKING_SIZE = 10

  planeDirection = app.planeDirection

  # TODO UGLY CODE, REWRITE
  # draw single selection highlight if no multi selection
  if len(app.multiSelected) == 0:
    selectedIndex3D: list[int] = app.selectedCell.list(3)
    selectedIndex: list[int] = selectedIndex3D[:planeDirection] + selectedIndex3D[planeDirection+1:]
    drawCellHighlight2D(app, Vector3D(*selectedIndex), 'gold', opacity=50)

  # draw multi selection highlight
  else:
    for selection in app.multiSelected:
      selection3D: list[int] = selection.list(3)
      selection2D: list[int] = selection3D[:planeDirection] + selection3D[planeDirection+1:]
      drawCellHighlight2D(app, Vector3D(*selection2D), 'green', opacity=20)


  # draw bounding box
  drawRect(DISP_POS.x, DISP_POS.y, DISP_SIZE.x, DISP_SIZE.y, fill=None, border = 'red', borderWidth = 1)

  # draw '#' block cross
  drawLine(DISP_POS.x + 3*CELL_SIZE.x, DISP_POS.y, DISP_POS.x + 3*CELL_SIZE.x, DISP_POS.y + DISP_SIZE.y)
  drawLine(DISP_POS.x + 6*CELL_SIZE.x, DISP_POS.y, DISP_POS.x + 6*CELL_SIZE.x, DISP_POS.y + DISP_SIZE.y)
  drawLine(DISP_POS.x, DISP_POS.y + 3*CELL_SIZE.y, DISP_POS.x + DISP_SIZE.y, DISP_POS.y + 3*CELL_SIZE.y)
  drawLine(DISP_POS.x, DISP_POS.y + 6*CELL_SIZE.y, DISP_POS.x + DISP_SIZE.y, DISP_POS.y + 6*CELL_SIZE.y)


  # draw cells

  miniBoard = app.board.getBoard2D(app.planeDirection, app.selectedCell.list(3)[app.planeDirection])

  for i in range(app.BOARD_SIZE):
    for j in range(app.BOARD_SIZE):
      posX = DISP_POS.x + (i + 0.5) * CELL_SIZE.x
      posY = DISP_POS.y + (j + 0.5) * CELL_SIZE.y

      cell: Cell = miniBoard[j][i]
      cellValue: int = cell.get()
      cellMarkings: set[int] = cell.markings

      if cellValue != None and cellValue != 0:
        drawLabel(str(cellValue), posX, posY, size=VALUE_SIZE)
      elif app.showMarkings and len(cell.markings) != 0:
        drawLabel(str(cellMarkings).replace(',','')[1:-1], posX, posY, size=MARKING_SIZE)


# Called by game3D_redrawAll()
def drawDebugTooltip(app) -> None:
  DISP_POS = app.DIMENSIONS['debugTooltipPos']
  DISP_SIZE = app.DIMENSIONS['debugTooltipSize']

  # draw bounding box
  drawRect(DISP_POS.x, DISP_POS.y, DISP_SIZE.x, DISP_SIZE.y, fill=None, border = 'red', borderWidth = 1)

  drawLabel(f'AngleX: {int(app.angleX)}', DISP_POS.x+10, DISP_POS.y+10, align = 'top-left')
  drawLabel(f'AngleY: {int(app.angleY)}', DISP_POS.x+10, DISP_POS.y+30, align = 'top-left')










def initializeConstants(app):
  # App contants
  app.CELL_SIZE = 50
  app.BOARD_SIZE = 9

  # Dimension constants
  app.DIMENSIONS = {
    'mainBoardCenter': Vector3D(400, 400),
    'mainBoardSize': Vector3D(800, 800),

    'cubeButtonCenter': Vector3D(1000, 500),
    'cubeButtonSize': Vector3D(200, 200),
    
    'miniBoardPos': Vector3D(175, 175),
    'miniBoardSize': Vector3D(450, 450),

    'debugTooltipPos': Vector3D(800 + 50, 0 + 50),
    'debugTooltipSize': Vector3D(200, 300),
  }


def initializeApp(app):
  # CMU Graphics
  app.width = 1200
  app.height = 800

  # Constants
  initializeConstants(app)

  # Page Organization
  app.page = 'game'  # start, game, settings
  
  # Sudoku Game
  app.board = Sudoku3D(size=app.BOARD_SIZE)

  app.selectedCell = Vector3D(5, 5, 5)
  app.multiSelect = False   # Select multiple cells, active when 'shift' is held TODO currently set to 'z'
  app.multiSelected = set()    # Multi-selected cells: list[Vector3D]
  app.planeDirection = 2    # Normal of selected plane, 0: x, 1: y, 2: z

  app.showPlaneOnly = True  # only displays numbers in selected plane
  app.showMarkings = True   # shows potential value markings

  # app.isFlatView = False    # currently in flat mode, or rotateable 3D mode
  
  # Visual
  app.angleX = 0 # degrees about the y-axis
  app.angleY = 0 # degrees about the x-axis

  # Mouse
  app.mouseSensitivity = 0.15
  app.mousePos = Vector3D(0, 0)


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

# Called by game2D_onMouseClick()
# Changes app.selectedCell to clicked cell index
def clickUpdateSelectedCell2D(app, mousePos: Vector3D) -> None:
  DISP_POS = app.DIMENSIONS['miniBoardPos']
  DISP_SIZE = app.DIMENSIONS['miniBoardSize']
  CELL_SIZE = DISP_SIZE / app.BOARD_SIZE

  # No action if click was outside board
  if not (DISP_POS.x < mousePos.x < DISP_POS.x + DISP_SIZE.x):
    return
  if not (DISP_POS.y < mousePos.y < DISP_POS.y + DISP_SIZE.y):
    return
  
  # Empty multiSelected list if multiSelect is off
  if not app.multiSelect:
    app.multiSelected.clear()
  
  # Get index in 2D board index coords
  selectedX = int((mousePos.x - DISP_POS.x) // CELL_SIZE.x)
  selectedY = int((mousePos.y - DISP_POS.y) // CELL_SIZE.y)

  # Convert 2D board index into 3D index, depending on planeDirection
  # TODO UGLY CODE, REWRITE BETTER
  selected3D = Vector3D(*app.selectedCell.list(3))
  if app.planeDirection == 0:
    selected3D = Vector3D(app.selectedCell.x, selectedX, selectedY)
  elif app.planeDirection == 1:
    selected3D = Vector3D(selectedX, app.selectedCell.y, selectedY)
  elif app.planeDirection == 2:
    selected3D = Vector3D(selectedX, selectedY, app.selectedCell.z)

  # If multi selection, add/remove selected to/from selection list
  if app.multiSelect:
    # Add original single selection when first multi-selecting
    if len(app.multiSelected) == 0:
      app.multiSelected.add(app.selectedCell)

    # Remove cell from multiSelected if already selected
    if selected3D in app.multiSelected:
      app.multiSelected.remove(selected3D)
    
    # Add cell to multiSelected
    else:
      app.multiSelected.add(selected3D)
  
  # Update selectedCell
  app.selectedCell = selected3D

  
# Enters digit into cell value if valid
def enterCellValue2D(app, key: str, selectionIndex = None) -> bool:
  if selectionIndex == None:
    selectionIndex: Vector3D = app.selectedCell

  if not key.isdigit():
    return False
  if not 1 <= int(key) <= app.BOARD_SIZE:
    return False
  return app.board.set(selectionIndex, int(key))


def enterMultipleCellValue2D(app, key: str):
  multiSelected = app.multiSelected
  for selection in multiSelected:
    enterCellValue2D(app, key, selection)
    


# ================================================
# ==================== game3D ====================
# ================================================

def game3D_onMouseMove(app, mouseX, mouseY):
  app.mousePos = Vector3D(mouseX, mouseY)

def game3D_onMouseDrag(app, mouseX, mouseY):
  mouseRotateMainBoard(app, Vector3D(mouseX, mouseY))

  app.mousePos = Vector3D(mouseX, mouseY)

def game3D_onKeyPress(app, key):
  if key in ['v']:
    app.isFlatView = True
    setActiveScreen('game2D')


# DISPLAY HANDLERS

def game3D_redrawAll(app):
  drawMainBoard(app)
  drawCubeButton(app)
  drawDebugTooltip(app)

# ================================================
# ==================== game2D ====================
# ================================================

def game2D_onMouseMove(app, mouseX, mouseY):
  app.mousePos = Vector3D(mouseX, mouseY)

def game2D_onKeyPress(app, key):
  if key in ['v']:
    app.isFlatView = False
    setActiveScreen('game3D')
  
  # Enable multiSelect when 'z' is held
  if key in ['z']:
    app.multiSelect = True
  
  if len(app.multiSelected) == 0:
    enterCellValue2D(app, key)
  else:
    enterMultipleCellValue2D(app, key)

def game2D_onKeyRelease(app, key):

  # Disable multiSelect when 'z' is released
  if key in ['z']:
    app.multiSelect = False

def game2D_onMousePress(app, mouseX, mouseY):

  clickUpdateSelectedCell2D(app, Vector3D(mouseX, mouseY))

# DISPLAY HANDLERS

def game2D_redrawAll(app):
  drawMiniBoard(app)


# ==============================================
# ==================== main ====================
# ==============================================

def onAppStart(app):
  initializeApp(app)

def main():
  runAppWithScreens(initialScreen='splash')

main()
