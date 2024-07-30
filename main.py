'''

TODO MVP REQ:
Part 1
  [ ] Help screen
    [ ] Game rules
    [ ] Settings
      [ ] Disable context based highlights
      [ ] Keybinds
  
  [ ] Load board
    [x] Load from 3D list
    [-] Load from txt file
    [x] Load from json file
    [ ] Create preset boards

  [ ] Game over

  [ ] Game difficulty

  [ ] Auto/Manual legals
    [x] Auto legals
    [ ] Auto update legals when cell change
    [ ] Manual legal input
    [x] Proper legals display
    [ ] Switch between manual/auto


Part 2
  [ ] Backtracking solver
    [ ] More efficient 2D solver
    [ ] Generalize to 3D
    [ ] Speed up

Part 3
  [ ] Obvious singles hint
  [ ] Apply hint

TODO ROADMAP:
 - Check Solved

 - Select with mouse (3D)

FUTURE:
 - Add mini cube to game2D that displays current plane pos and orientation
 - Make small cube clickable
 - choose between 9x9x9 or 4x4x4


 
CHANGES:
 - Create general utils class including functions such as:
    - get 2D index from 3D index and vice versa
    - get distance
 - Improve splashScreen code

 - Functions that game2D & game3D share:
    - keyShiftPlane3D
    - keyMoveSelection3D
    - enterCellValue2D
    - getIndex3D
    - getIndex2D

    
USEFUL RESOURCES:


'''



from cmu_graphics import *

from graphics import *
from sudoku import *

from splashScreen import *
from helpScreen import *
from game2D import *
from game3D import *





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
  app.board.loadBoardJSON('./resources/boards_3D/blankBoard.json')

  app.selectedCell = Vector3D(5, 5, 5)
  app.multiSelect = False   # Select multiple cells, active when 'shift' is held TODO currently set to 'z'
  app.multiSelected = set()    # Multi-selected cells: list[Vector3D]
  app.planeDirection = 2    # Normal of selected plane, 0: x, 1: y, 2: z

  app.showPlaneOnly = True  # only displays numbers in selected plane
  app.showMarkings = True   # shows potential value markings

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
