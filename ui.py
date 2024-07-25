from cmu_graphics import *

class Button:
  def __init__(self, x: float, y: float, width: float, height: float, border='black', fill='white', borderRadius=0, borderWidth=0):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

    self.border = border
    self.fill = fill
    self.borderRadius = borderRadius
    self.borderWidth = borderWidth

    self.isHover = False
    self.isActive = False
  
  def updateHover(self, mouseX, mouseY) -> bool:
    # Check if mouse is in button
    if self.x <= mouseX <= self.x + self.width and self.y <= mouseY <= self.y + self.height:
      self.isHover = True
      return True
    else:
      self.isHover = False
      return False
  
  def updateActive(self, mouseX, mouseY, isMouseDown) -> bool:
    # Check if mouse is in button
    if self.x <= mouseX <= self.x + self.width and self.y <= mouseY <= self.y + self.height and isMouseDown:
      self.isActive = True
    else:
      self.isActive = False
  
  def checkClicked(self, mouseX, mouseY) -> bool:
    # Check if mouse is in button
    if self.x <= mouseX <= self.x + self.width and self.y <= mouseY <= self.y + self.height:
      return True
    else:
      return False
  
  @staticmethod
  def drawBaseButton(x, y, w, h, fillColor, borderColor, borderRadius, borderWidth):
    oLeft    = x     + borderRadius
    oRight   = x + w - borderRadius
    oTop     = y     + borderRadius
    oBottom  = y + h - borderRadius

    iLeft = oLeft + borderWidth
    iRight = oRight - borderWidth
    iTop = oTop + borderWidth
    iBottom = oBottom - borderWidth

    # Draw border
    if borderWidth != 0:
      if borderRadius != 0:
        drawCircle(oLeft, oTop, borderRadius, fill=borderColor)
        drawCircle(oRight, oTop, borderRadius, fill=borderColor)
        drawCircle(oLeft, oBottom, borderRadius, fill=borderColor)
        drawCircle(oRight, oBottom, borderRadius, fill=borderColor)
      drawRect(x, oTop, w, oBottom - oTop, fill=borderColor)
      drawRect(oLeft, y, oRight - oLeft, h, fill=borderColor)
    
    if borderRadius - borderWidth > 0:
      drawCircle(oLeft, oTop, borderRadius - borderWidth, fill=fillColor)
      drawCircle(oRight, oTop, borderRadius - borderWidth, fill=fillColor)
      drawCircle(oLeft, oBottom, borderRadius - borderWidth, fill=fillColor)
      drawCircle(oRight, oBottom, borderRadius - borderWidth, fill=fillColor)
    drawRect(x + borderWidth, iTop - borderWidth, w - 2*borderWidth, iBottom - iTop + 2*borderWidth, fill=fillColor)
    drawRect(iLeft - borderWidth, y + borderWidth, iRight - iLeft + 2*borderWidth, h - 2*borderWidth, fill=fillColor)

  def drawActive(self):
    self.drawBaseButton(self.x, self.y, self.width, self.height, self.fill, self.border, self.borderRadius, self.borderWidth)

  def drawHover(self):
    self.drawBaseButton(self.x-5, self.y-5, self.width+10, self.height+10, self.fill, self.border, self.borderRadius, self.borderWidth)

  def drawDefault(self):
    self.drawBaseButton(self.x, self.y, self.width, self.height, self.fill, self.border, self.borderRadius, self.borderWidth)


  def draw(self):
    if self.isActive:
      self.drawActive()
    elif self.isHover:
      self.drawHover()
    else:
      self.drawDefault()

# btn1 = Button(100, 100, 40, 40, borderRadius=19, borderWidth=0, fill='pink')

# def redrawAll(app):
#   btn1.draw()

# def onMousePress(app, mouseX, mouseY):
#   btn1.updateActive(mouseX, mouseY, True)

# def onMouseMove(app, mouseX, mouseY):
#   btn1.updateHover(mouseX, mouseY)

# def onMouseRelease(app, mouseX, mouseY):
#   btn1.updateActive(mouseX, mouseY, False)

# runApp(width=800, height=800)