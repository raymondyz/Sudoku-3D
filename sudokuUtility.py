from graphics import *


# Code taken from https://www.geeksforgeeks.org/check-whether-a-given-point-lies-inside-a-triangle-or-not/
def getTriangleArea2D(p1: Vector3D, p2: Vector3D, p3: Vector3D) -> float:
  return abs((p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y)) / 2.0)

# Code taken from https://www.geeksforgeeks.org/check-whether-a-given-point-lies-inside-a-triangle-or-not/
def isInsideTriangle2D(p1: Vector3D, p2: Vector3D, p3: Vector3D, point: Vector3D) -> bool:
  A = getTriangleArea2D(p1, p2, p3)

  # Calculate area of triangle PBC 
  A1 = getTriangleArea2D(point, p2, p3)
    
  # Calculate area of triangle PAC 
  A2 = getTriangleArea2D(p1, point, p3)
    
  # Calculate area of triangle PAB 
  A3 = getTriangleArea2D(p1, p2, point)
    
  return abs(A - (A1 + A2 + A3)) < 1e-3

def isInsideQuad2D(p1: Vector3D, p2: Vector3D, p3: Vector3D, p4: Vector3D, point: Vector3D) -> bool:
  return isInsideTriangle2D(p1, p2, p3, point) or isInsideTriangle2D(p1, p4, p3, point)


def isInsideQuad2D(p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y, pointx, pointy) -> bool:
  point = Vector3D(pointx, pointy)
  p1 = Vector3D(p1x, p1y)
  p2 = Vector3D(p2x, p2y)
  p3 = Vector3D(p3x, p3y)
  p4 = Vector3D(p4x, p4y)
  return isInsideTriangle2D(p1, p2, p3, point) or isInsideTriangle2D(p1, p4, p3, point)