from cmu_graphics import *

from graphics import *
from sudoku import *

from game3D import keyShiftPlane3D, keyMoveSelection3D

# Convert 3D index to 2D index
def getIndex2D(app, index3D: Vector3D):
  if app.planeDirection == 0:
    return Vector3D(index3D.z, index3D.y)
  elif app.planeDirection == 1:
    return Vector3D(index3D.z, index3D.x)
  elif app.planeDirection == 2:
    return Vector3D(index3D.x, index3D.y)

# Convert 2D index to 3D index
def getIndex3D(app, index2D: Vector3D):
  if app.planeDirection == 0:
    return Vector3D(app.selectedCell.x, index2D.y, index2D.x)
  elif app.planeDirection == 1:
    return Vector3D(index2D.y, app.selectedCell.y, index2D.x)
  elif app.planeDirection == 2:
    return Vector3D(index2D.x, index2D.y, app.selectedCell.z)


# Draw highlight on cell at index
def drawCellHighlight2D(app, index2D: Vector3D, color, opacity=100, borderColor=None, borderWidth=1):
  DISP_POS = app.DIMENSIONS['miniBoardPos']
  DISP_SIZE = app.DIMENSIONS['miniBoardSize']
  CELL_SIZE = DISP_SIZE / app.BOARD_SIZE

  drawRect(DISP_POS.x + CELL_SIZE.x * index2D.x, DISP_POS.y + CELL_SIZE.y * index2D.y, CELL_SIZE.x, CELL_SIZE.y, fill=color, opacity=opacity, border=borderColor, borderWidth=borderWidth)

# Called by drawMiniBoard()
# Draws legals pencil markings with proper style
def drawMiniBoardLegals(app, cx: float, cy: float, markings: set[int]) -> None:
  MARKING_SIZE = 10
  DY = 15

  color = 'black'
  markingStr = str(markings).replace(',','')[1:-1]

  drawLabel(markingStr[:5], cx, cy - DY, size=MARKING_SIZE, fill=color)
  drawLabel(markingStr[6:11], cx, cy, size=MARKING_SIZE, fill=color)
  drawLabel(markingStr[12:], cx, cy + DY, size=MARKING_SIZE, fill=color)

# Called by game2D_redrawAll()
def drawMiniBoard(app) -> None:
  DISP_POS = app.DIMENSIONS['miniBoardPos']
  DISP_SIZE = app.DIMENSIONS['miniBoardSize']

  CELL_SIZE = DISP_SIZE / app.BOARD_SIZE
  VALUE_SIZE = 20

  planeDirection = app.planeDirection
  miniBoard = app.board.getBoard2D(app.planeDirection, app.selectedCell.list(3)[app.planeDirection])
  blockSize = int(app.BOARD_SIZE**0.5)

  selectedIndex = getIndex2D(app, app.selectedCell)
  selectedCell = miniBoard[selectedIndex.x][selectedIndex.y]

  # draw single selection highlight if no multi selection
  if len(app.multiSelected) == 0:
    drawCellHighlight2D(app, selectedIndex, 'gold', opacity=50)

  # draw multi selection highlight
  else:
    for selection in app.multiSelected:
      selection2D = getIndex2D(app, selection)
      drawCellHighlight2D(app, selection2D, 'green', opacity=20)


  # draw bounding box
  drawRect(DISP_POS.x, DISP_POS.y, DISP_SIZE.x, DISP_SIZE.y, fill=None, border = 'red', borderWidth = 1)

  # draw '#' block cross
  drawLine(DISP_POS.x + 3*CELL_SIZE.x, DISP_POS.y, DISP_POS.x + 3*CELL_SIZE.x, DISP_POS.y + DISP_SIZE.y)
  drawLine(DISP_POS.x + 6*CELL_SIZE.x, DISP_POS.y, DISP_POS.x + 6*CELL_SIZE.x, DISP_POS.y + DISP_SIZE.y)
  drawLine(DISP_POS.x, DISP_POS.y + 3*CELL_SIZE.y, DISP_POS.x + DISP_SIZE.y, DISP_POS.y + 3*CELL_SIZE.y)
  drawLine(DISP_POS.x, DISP_POS.y + 6*CELL_SIZE.y, DISP_POS.x + DISP_SIZE.y, DISP_POS.y + 6*CELL_SIZE.y)


  # draw cells

  for x in range(app.BOARD_SIZE):
    for y in range(app.BOARD_SIZE):
      posX = DISP_POS.x + (x + 0.5) * CELL_SIZE.x
      posY = DISP_POS.y + (y + 0.5) * CELL_SIZE.y

      cell: Cell = miniBoard[x][y]
      cellValue: int = cell.get()

      # Draw gray background for locked cells
      if cell.isLocked:
        drawCellHighlight2D(app, Vector3D(x, y), 'gray', 10)

      # Draw red background for illegal cells
      if not cell.isLegal:
        drawCellHighlight2D(app, Vector3D(x, y), 'red', 10)

      # Highlight cell orange if in same row or col or block
      if ((x == selectedIndex.x or y == selectedIndex.y
          or (selectedIndex.x // blockSize == x // blockSize and selectedIndex.y // blockSize == y // blockSize))
          and not (x == selectedIndex.x and y == selectedIndex.y)):
        drawCellHighlight2D(app, Vector3D(x, y), 'orange', 10)

      # Set value text color
      valueColor = 'black'
      # Set same number as selected cell to red
      if cellValue == selectedCell.get() and cellValue != None:
        valueColor = 'red'
      
      # Draw value if value exists
      if cellValue != None:
        drawLabel(str(cellValue), posX, posY, size=VALUE_SIZE, fill=valueColor)

      # Draw pencil marks if no value and markings are enabled
      elif app.showMarkings:
        # Auto-legal mode, draw auto-legals
        if app.showLegals and len(cell.legals) != 0:
          drawMiniBoardLegals(app, posX, posY, cell.legals)
        # Manual-legal mode, draws user markings
        elif len(cell.markings) != 0:
          drawMiniBoardLegals(app, posX, posY, cell.markings)






# EVENT HANDLERS

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

  # Get 3D index
  selected3D = getIndex3D(app, Vector3D(selectedX, selectedY))

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
  
  # remove value if delete
  if key in ['delete', 'backspace']:
    app.board.set(selectionIndex, None)

  if not key.isdigit():
    return False
  if not 1 <= int(key) <= app.BOARD_SIZE:
    return False
  return app.board.set(selectionIndex, int(key))

# Enters input value to all multi-selected cells
def enterMultipleCellValue2D(app, key: str):
  multiSelected = app.multiSelected
  for selection in multiSelected:
    enterCellValue2D(app, key, selection)

# ================================================
# ==================== game2D ====================
# ================================================

def game2D_onScreenActivate(app):
  app.multiSelected.clear()
  app.multiSelect = False

def game2D_onMouseMove(app, mouseX, mouseY):
  app.mousePos = Vector3D(mouseX, mouseY)

def game2D_onKeyPress(app, key):

  # Shifts plane forward/backward
  # IMPORTED from game3D
  keyShiftPlane3D(app, key)

  # Moves selection within plane
  # IMPORTED from game3D
  if len(app.multiSelected) == 0:
    keyMoveSelection3D(app, key)
  
  # Enable multiSelect when 'z' is held
  if key in ['z']:
    app.multiSelect = True

  
  # TODO TESTING
  if key in ['v']:
    app.isFlatView = False
    setActiveScreen('game3D')
  if key in ['o']:
    app.board.clearRandomCells(100)
  
  # Input value into selected cell
  if len(app.multiSelected) == 0:
    enterCellValue2D(app, key)
    # Update legal states
    app.board.updateIllegalCells()

  # Input value into multi-selected cells
  else:
    enterMultipleCellValue2D(app, key)
    # Update legal states
    app.board.updateIllegalCells()

def game2D_onKeyRelease(app, key):

  # Disable multiSelect when 'z' is released
  if key in ['z']:
    app.multiSelect = False

def game2D_onMousePress(app, mouseX, mouseY):

  clickUpdateSelectedCell2D(app, Vector3D(mouseX, mouseY))

# DISPLAY HANDLERS

def game2D_redrawAll(app):
  drawMiniBoard(app)

