'''
PROBLEMS:

 - Division by zero gives (0, 0, 0)
 - Reflected dunder funcs not implemented


FUTURE:



'''




import math

class Vector3D:
  def __init__(self, x: float = 0, y: float = 0, z: float = 0):
    self.x: float = x
    self.y: float = y
    self.z: float = z
  
  def __repr__(self):
    return f'Vector3D({self.x}, {self.y}, {self.z})'
  
  def __hash__(self):
    return hash(self.__repr__())
  
  def __eq__(self, other):
    if isinstance(other, Vector3D):
      return (self.x, self.y, self.z) == (other.x, other.y, other.z)
    return NotImplemented
  
  def __neg__(self):
    return Vector3D(-self.x, -self.y, -self.z)
  
  def __add__(self, other):
    if isinstance(other, Vector3D):
      return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    if isinstance(other, tuple) or isinstance(other, list):
      return Vector3D(self.x + other[0], self.y + other[1], self.z + other[2])
    
    return NotImplemented
  
  def __sub__(self, other):
    if isinstance(other, Vector3D):
      return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    if isinstance(other, tuple) or isinstance(other, list):
      return Vector3D(self.x - other[0], self.y - other[1], self.z - other[2])
    
    return NotImplemented
  
  def __mul__(self, other: float):
    if isinstance(other, int) or isinstance(other, float):
      return Vector3D(self.x * other, self.y * other, self.z * other)
    
    return NotImplemented
      
  def __truediv__(self, other: float):
    if isinstance(other, int) or isinstance(other, float):
      if other == 0:
        return Vector3D(0, 0, 0)
      return Vector3D(self.x / other, self.y / other, self.z / other)
    
    return NotImplemented
  
  def __floordiv__(self, other: float):
    if isinstance(other, int) or isinstance(other, float):
      if other == 0:
        return Vector3D(0, 0, 0)
      return Vector3D(self.x // other, self.y // other, self.z // other)
    
    return NotImplemented

  def __mod__(self, other: float):
    if isinstance(other, int) or isinstance(other, float):
      if other == 0:
        return Vector3D(0, 0, 0)
      return Vector3D(self.x % other, self.y % other, self.z % other)
    
    return NotImplemented

  
  def list(self, length: int = 3) -> list[float]:
    return [self.x, self.y, self.z, 1][0:min(4, max(0, length))]
  
  # def rowForm(self, cols: int = 3) -> np.ndarray:
  #   return np.array([self.x, self.y, self.z, 1])[0:min(4, max(0, cols))]

  # def colForm(self, rows: int = 3) -> np.ndarray:
  #   return np.array([self.x, self.y, self.z, 1])[0:min(4, max(0, rows))].T

  def getLength(self) -> float:
    return (self.x**2 + self.y**2 + self.z**2)**0.5
    
  def normalized(self):
    length = self.getLength()
    if length == 0:
      return Vector3D(0, 0, 0)
    return Vector3D(self.x / length, self.y / length, self.z / length)
  
  # def transformed(self, transformMatrix4x4: np.ndarray):
  #   return np.matmul(transformMatrix4x4, self.colForm(4))
  
  # def translated(self, dPos):
  #   if isinstance(dPos, Vector3D):
  #     dPos = dPos.rowForm()
  #   translateMatrix = np.array(
  #     [[1, 0, 0, dPos[0]],
  #      [0, 1, 0, dPos[1]],
  #      [0, 0, 1, dPos[2]],
  #      [0, 0, 0, 1     ]])
    
  #   return self.transformed(translateMatrix)

  def rotatedX(self, theta: float, axisPos3d):
    x = self.x
    y = self.y
    z = self.z
    cx = axisPos3d.x
    cy = axisPos3d.y
    cz = axisPos3d.z
    
    # Rotation matrix math taken from https://en.wikipedia.org/wiki/Rotation_matrix
    newx = cx + ((x-cx)*1) + ((y-cy)*0) + ((z-cz)*0)
    newy = cy + ((x-cx)*0) + ((y-cy)*math.cos(theta)) + ((z-cz)*-math.sin(theta))
    newz = cz + ((x-cx)*0) + ((y-cy)*math.sin(theta)) + ((z-cz)*math.cos(theta))

    return Vector3D(newx, newy, newz)
    
  def rotatedY(self, theta: float, axisPos3d):
    x = self.x
    y = self.y
    z = self.z
    cx = axisPos3d.x
    cy = axisPos3d.y
    cz = axisPos3d.z
    
    # Rotation matrix math taken from https://en.wikipedia.org/wiki/Rotation_matrix
    newx = cx + ((x-cx)*math.cos(theta)) + ((y-cy)*0) + ((z-cz)*math.sin(theta))
    newy = cy + ((x-cx)*0) + ((y-cy)*1) + ((z-cz)*0)
    newz = cz + ((x-cx)*-math.sin(theta)) + ((y-cy)*0) + ((z-cz)*math.cos(theta))

    return Vector3D(newx, newy, newz)
      
  def rotatedZ(self, theta: float, axisPos3d):
    x = self.x
    y = self.y
    z = self.z
    cx = axisPos3d.x
    cy = axisPos3d.y
    cz = axisPos3d.z
    
    # Rotation matrix math taken from https://en.wikipedia.org/wiki/Rotation_matrix
    newx = cx + ((x-cx)*math.cos(theta)) + ((y-cy)*-math.sin(theta)) + ((z-cz)*0)
    newy = cy + ((x-cx)*math.sin(theta)) + ((y-cy)*math.cos(theta)) + ((z-cz)*0)
    newz = cz + ((x-cx)*0) + ((y-cy)*0) + ((z-cz)*1)

    return Vector3D(newx, newy, newz)