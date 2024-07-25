from cmu_graphics import *
import math

from graphics import *
from sudoku import *

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
  
  # remove value if delete
  if key in ['delete', 'backspace']:
    app.board.set(selectionIndex, None)

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

