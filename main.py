from cmu_graphics import *

from graphics import *
from sudoku import *

from splashScreen import *
from helpScreen import *
from settingsScreen import *
from game2D import *
from game3D import *


def getNewBoard(app, difficulty: int) -> Sudoku3D:
  newBoard = Sudoku3D(size=app.BOARD_SIZE)
  newBoard.loadBoardJSON('./resources/boards_3D/solvedBoard.json')
  newBoard.clearRandomCells(min(app.BOARD_SIZE**3, 50+difficulty*100))
  return newBoard


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

  # Maps 'shift' + 'numkey' to 'numkey'
  app.SHIFT_KEY_MAP = {
    '!': '1',
    '@': '2',
    '#': '3',
    '$': '4',
    '%': '5',
    '^': '6',
    '&': '7',
    '*': '8',
    '(': '9'
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
  # app.board = Sudoku3D(size=app.BOARD_SIZE)
  app.board = getNewBoard(app, 5)

  app.isBoardSolved = app.board.checkSolved() # Whether the board has been correctly solved
  app.hasIllegalCell = app.board.checkHasIllegal() # Whether the board has an illegal cell

  app.selectedCell = Vector3D(5, 5, 5)
  app.multiSelect = False   # Select multiple cells, active when 'shift' is held TODO currently set to 'z'
  app.multiSelected = set() # Multi-selected cells: list[Vector3D]
  app.planeDirection = 2    # Normal of selected plane, 0: x, 1: y, 2: z

  app.showPlaneOnly = True  # only displays numbers in selected plane
  app.showMarkings = True   # shows potential value markings
  app.showLegals = False    # shows legals instead of markings

  # app.isFlatView = False    # currently in flat mode, or rotateable 3D mode
  
  # Visual
  app.angleX = 45 # degrees about the y-axis
  app.angleY = 30 # degrees about the x-axis

  # Mouse
  app.mouseSensitivity = 0.15
  app.mousePos = Vector3D(0, 0)


# ==============================================
# ==================== main ====================
# ==============================================

def onAppStart(app):
  initializeApp(app)

def main():
  runAppWithScreens(initialScreen='splash')

main()
