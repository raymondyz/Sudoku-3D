from graphics import *
import random
import json



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
    self.BLOCK_SIZE: int = int(self.BOARD_SIZE**0.5)
    self.board: list[list[list[Cell]]] = self.newBoard(self.BOARD_SIZE)

    self.updateIllegalCells()
    self.updateAllLegals()

  def newBoard(self, size: int) -> list[list[list[Cell]]]:
    list3D = []
    for i in range(size):
      list2D = []
      for j in range(size):
        list1D = []
        for k in range(size):
          # cell = Cell(100*i + 10*j + k)
          cell = Cell()
          if random.choice([0, 1, 1]) == 0:
            cell = Cell(((i+j+k) % 9) + 1)
            cell.isLocked = True
          cell.markings = {i, j, k}
          list1D.append(cell)
        list2D.append(list1D)
      list3D.append(list2D)
    return list3D
  
  def loadBoard(self, board: list[list[list[int]]]) -> bool:
    size = len(board)
    if len(board[0]) != size or len(board[0][0]) != size:
      raise Exception('Invalid board structure')
    
    for i in range(size):
      for j in range(size):
        for k in range(size):
          cell = Cell()
          value = board[i][j][k]
          
          if value != None and value > 0:
            cell.value = value
            cell.isLocked = True

          self.board[i][j][k] = cell
    
    self.updateIllegalCells()
    self.updateAllLegals()
  
  def loadBoardJSON(self, file: str) -> bool:
    board = json.loads(open(file, 'r').read())
    self.loadBoard(board)
  
  # TODO don't fall into infinite loop!
  def clearRandomCells(self, amount: int) -> bool:
    removed = 0
    while removed < amount:
      randomIndex = Vector3D(random.randrange(self.BOARD_SIZE), random.randrange(self.BOARD_SIZE), random.randrange(self.BOARD_SIZE))

      cell: Cell = self.getCell(randomIndex)

      if cell.value != None:
        cell.value = None
        cell.isLocked = False
        removed += 1

    self.updateAllLegals()

  # Tries to set index cell to value, then update legals
  def set(self, index: Vector3D, value) -> bool:
    cell = self.board[index.x][index.y][index.z]
    prevValue = cell.value

    # Tries to set value
    if cell.set(value):

      # If setting cell to None, re-evaluate legals
      # TODO can probably find more efficient method
      if value == None and prevValue != None:
        self.updateAllLegals()

      # If changing cell value, re-evalueate legals
      elif value != None and prevValue != None:
        self.updateAllLegals()
      
      # If adding cell value, update legals in same group
      elif value != None and prevValue == None:
        self.updateGroupLegals(index, value)
  
  def get(self, index: Vector3D) -> int:
    cell = self.board[index.x][index.y][index.z]
    return cell.get()
  
  def getCell(self, index: Vector3D) -> int:
    cell = self.board[index.x][index.y][index.z]
    return cell
  
  # Returns 2D list containing cells, access cells with getBoard2D()[xIndex][yIndex]
  def getBoard2D(self, plane: int, planeIndex: int) -> list[list[Cell]]:
    list2D = []
    for i in range(self.BOARD_SIZE):
      list1D = []
      for j in range(self.BOARD_SIZE):
        if plane == 0:
          list1D.append(self.board[planeIndex][j][i])
        elif plane == 1:
          list1D.append(self.board[j][planeIndex][i])
        elif plane == 2:
          list1D.append(self.board[i][j][planeIndex])
      list2D.append(list1D)
    return list2D

  # @staticmethod
  # def printBoard2D(board2D: list[list[Cell]]):
  #   for row in range(9):
  #     for col in range(9):
  #       value = board2D[row][col].get()
  #       print(' ' if value == None else value, end='  ')
  #     print()
  #   print()
  #   print()
  
  def setAllToLegal(self) -> None:
    for i in range(self.BOARD_SIZE):
      for j in range(self.BOARD_SIZE):
        for k in range(self.BOARD_SIZE):
          self.board[i][j][k].isLegal = True

  def updateIllegalCells(self) -> None:
    
    # Set all cells to legal
    self.setAllToLegal()

    # Block check (3x3x1 blocks)
    for i in range(0, self.BOARD_SIZE, self.BLOCK_SIZE):
      for j in range(0, self.BOARD_SIZE, self.BLOCK_SIZE):
        for layer in range(self.BOARD_SIZE):
          # Dict of the # of appearances for each value in block
          seenX = dict()
          seenY = dict()
          seenZ = dict()

          for dx in range(self.BLOCK_SIZE):
            for dy in range(self.BLOCK_SIZE):
              cellX = self.board[layer][i+dx][j+dy]
              cellY = self.board[i+dx][layer][j+dy]
              cellZ = self.board[i+dx][j+dy][layer]

              # Add cell values to seen dict
              if cellX.get() != None:
                seenX[cellX.get()] = seenX.get(cellX.get(), 0) + 1
              if cellY.get() != None:
                seenY[cellY.get()] = seenY.get(cellY.get(), 0) + 1
              if cellZ.get() != None:
                seenZ[cellZ.get()] = seenZ.get(cellZ.get(), 0) + 1
          
          for dx in range(self.BLOCK_SIZE):
            for dy in range(self.BLOCK_SIZE):
              cellX = self.board[layer][i+dx][j+dy]
              cellY = self.board[i+dx][layer][j+dy]
              cellZ = self.board[i+dx][j+dy][layer]

              # Set cell illegal if value appears multiple times
              if seenX.get(cellX.get(), 0) > 1:
                cellX.isLegal = False
              if seenY.get(cellY.get(), 0) > 1:
                cellY.isLegal = False
              if seenZ.get(cellZ.get(), 0) > 1:
                cellZ.isLegal = False
          
    
    # Row / column Check
    for i in range(self.BOARD_SIZE):
      for j in range(self.BOARD_SIZE):
        # Dictionary of the # of appearances for each value
        seenX = dict()
        seenY = dict()
        seenZ = dict()

        for layer in range(self.BOARD_SIZE):

          cellX = self.board[layer][i][j]
          cellY = self.board[i][layer][j]
          cellZ = self.board[i][j][layer]

          # Add cell values to seen dict
          if cellX.get() != None:
            seenX[cellX.get()] = seenX.get(cellX.get(), 0) + 1
          if cellY.get() != None:
            seenY[cellY.get()] = seenY.get(cellY.get(), 0) + 1
          if cellZ.get() != None:
            seenZ[cellZ.get()] = seenZ.get(cellZ.get(), 0) + 1
        
        for layer in range(self.BOARD_SIZE):
          cellX = self.board[layer][i][j]
          cellY = self.board[i][layer][j]
          cellZ = self.board[i][j][layer]

          # Set cell illegal if value appears multiple times
          if seenX.get(cellX.get(), 0) > 1:
            cellX.isLegal = False
          if seenY.get(cellY.get(), 0) > 1:
            cellY.isLegal = False
          if seenZ.get(cellZ.get(), 0) > 1:
            cellZ.isLegal = False


  # FOR INTERNAL USE
  # Resets all cells to full set of legals
  def resetAllLegals(self) -> None:

    for i in range(self.BOARD_SIZE):
      for j in range(self.BOARD_SIZE):
        for k in range(self.BOARD_SIZE):
          cell: Cell = self.board[i][j][k]

          # Set unlocked cell legals to all values
          if cell.isLocked:
            cell.legals = set()
          else:
            cell.legals = set(range(1, self.BOARD_SIZE + 1))

  # set the Cell.markings of every cell to its Cell.legals
  def setAllMarkingsToLegals(self):
    for i in range(self.BOARD_SIZE):
      for j in range(self.BOARD_SIZE):
        for k in range(self.BOARD_SIZE):
          cell = self.board[i][j][k]
          cell.markings = set(cell.legals)

  # Removes value from all cell legals in same group (row/col/block) as index
  def updateGroupLegals(self, index: Vector3D, value: int) -> None:

    # Removes value from all 9x1x1 columns
    for layer in range(self.BOARD_SIZE):
      cellX: Cell = self.board[layer][index.y][index.z]
      cellY: Cell = self.board[index.x][layer][index.z]
      cellZ: Cell = self.board[index.x][index.y][layer]

      # Removes value if value in legals
      if value in cellX.legals:
        cellX.legals.remove(value)
      if value in cellY.legals:
        cellY.legals.remove(value)
      if value in cellZ.legals:
        cellZ.legals.remove(value)
    
    # Removes value from all 3x3x1 blocks
    blockVertex = (index // self.BLOCK_SIZE) * self.BLOCK_SIZE  # Rounds to nearest 3rd
    for i in range(self.BLOCK_SIZE):
      for j in range(self.BLOCK_SIZE):
        cellX = self.board[index.x][blockVertex.y + i][blockVertex.z + j]
        cellY = self.board[blockVertex.x + i][index.y][blockVertex.z + j]
        cellZ = self.board[blockVertex.x + i][blockVertex.y + j][index.z]

        if value in cellX.legals:
          cellX.legals.remove(value)
        if value in cellY.legals:
          cellY.legals.remove(value)
        if value in cellZ.legals:
          cellZ.legals.remove(value)

  
  def updateAllLegals(self) -> None:

    # Reset all cells to full legals
    self.resetAllLegals()
    
    # Remove illegal values
    for i in range(self.BOARD_SIZE):
      for j in range(self.BOARD_SIZE):
        for k in range(self.BOARD_SIZE):
          cell = self.board[i][j][k]
          
          # If cell has a value, update all legals in same group (row/col/block)
          if cell.value != None:
            self.updateGroupLegals(Vector3D(i, j, k), cell.value)
