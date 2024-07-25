from graphics import *




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


