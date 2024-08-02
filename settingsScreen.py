from cmu_graphics import *
from ui import *
from sudoku import Sudoku3D


def settings_onAppStart(app):
  app.diffSlider = Slider(200, 200, 300, 7, 10)
  app.difficulty = 0
  app.newBoardBtn = Button(200, 250, 180, 60, border='black', borderWidth=2, borderRadius=10, fill='white', text='New Board')

def getNewBoard(app, difficulty: int) -> Sudoku3D:
  newBoard = Sudoku3D(size=app.BOARD_SIZE)
  newBoard.loadBoardJSON('./resources/boards_3D/solvedBoard.json')
  newBoard.clearRandomCells(min(app.BOARD_SIZE**3, 50+difficulty*100))
  return newBoard

def settings_redrawAll(app):
  drawLabel('Difficulty: ' + str(app.difficulty), 200, 100, size=24)
  app.newBoardBtn.draw()

  app.diffSlider.draw()
  app.splashBtn.draw()

def settings_onMousePress(app, mouseX, mouseY):
  app.diffSlider.mousePress(mouseX, mouseY)
  app.newBoardBtn.updateActive(mouseX, mouseY, True)

  app.splashBtn.updateActive(mouseX, mouseY, True)
  if app.splashBtn.checkClicked(mouseX, mouseY):
    setActiveScreen('splash')


  if app.newBoardBtn.checkClicked(mouseX, mouseY):
    app.board = getNewBoard(app, app.difficulty)
    setActiveScreen('splash')

def settings_onMouseRelease(app, mouseX, mouseY):
  app.diffSlider.mouseRelease()
  app.newBoardBtn.updateActive(mouseX, mouseY, False)
  app.splashBtn.updateActive(mouseX, mouseY, False)

def settings_onMouseMove(app, mouseX, mouseY):
  app.diffSlider.mouseMove(mouseX, mouseY)
  app.newBoardBtn.updateHover(mouseX, mouseY)
  app.splashBtn.updateHover(mouseX, mouseY)


def settings_onMouseDrag(app, mouseX, mouseY):
  app.diffSlider.mouseDrag(mouseX, mouseY)
  app.difficulty = int(rounded(app.diffSlider.getSlideAmount()*7))

def settings_onKeyPress(app, key):
  if key in ['escape', 'esc']:
    setActiveScreen('splash')

