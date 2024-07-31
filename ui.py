from cmu_graphics import *

class Button:
  def __init__(self, x: float, y: float, width: float, height: float, border='black', fill='white', borderRadius=0, borderWidth=0, text=None, icon=None):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

    self.border = border
    self.fill = fill
    self.borderRadius = borderRadius
    self.borderWidth = borderWidth

    self.text = text
    self.textSize = 24
    self.icon = icon

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
  def drawBaseButton(x, y, w, h, fillColor, borderColor, borderRadius, borderWidth, text=None, textSize=24,icon=None):
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

    if text != None:
      drawLabel(text, x + 0.5*w, y + 0.5*h, size=textSize, bold=True)


  def drawActive(self):
    self.drawBaseButton(self.x, self.y, self.width, self.height, self.fill, self.border, self.borderRadius, self.borderWidth, text=self.text, textSize=self.textSize)

  def drawHover(self):
    self.drawBaseButton(self.x-5, self.y-5, self.width+10, self.height+10, self.fill, self.border, self.borderRadius, self.borderWidth, text=self.text, textSize=self.textSize+2)

  def drawDefault(self):
    self.drawBaseButton(self.x, self.y, self.width, self.height, self.fill, self.border, self.borderRadius, self.borderWidth, text=self.text, textSize=self.textSize)


  def draw(self):
    if self.isActive:
      self.drawActive()
    elif self.isHover:
      self.drawHover()
    else:
      self.drawDefault()





class Slider:
  def __init__(self, posX, posY, length, railWidth=5, handleRadius=5):
    self.x = posX
    self.y = posY
    self.w = length
    self.thickness = railWidth
    self.handleR = handleRadius

    self.slideX = self.x

    self.isHover = False
    self.isActive = False

  def updateSlideX(self, newSlideX):
    self.slideX = max(self.x, min(self.x + self.w, newSlideX))
  
  def addSlideDx(self, slideDx):
    self.updateSlideX(self, self.slideX + slideDx)

  def mouseDrag(self, mouseX, mouseY):
    if self.isActive:
      self.updateSlideX(mouseX)
  
  def mouseMove(self, mouseX, mouseY):
    if distance(self.slideX, self.y, mouseX, mouseY) <= self.handleR:
      self.isHover = True
    else:
      self.isHover = False
  
  def mousePress(self, mouseX, mouseY):
    if distance(self.slideX, self.y, mouseX, mouseY) <= self.handleR:
      self.isActive = True
    
  def mouseRelease(self):
    self.isActive = False

  def getSlideAmount(self):
    return (self.slideX - self.x) / (self.w)
  

  
  def draw(self):
    drawLine(self.x, self.y, self.x+self.w, self.y, fill='lightGray', lineWidth=self.thickness)
    if self.isHover:
      drawCircle(self.slideX, self.y, self.handleR+2, fill='black', border=None)
    else:
      drawCircle(self.slideX, self.y, self.handleR, fill='black', border=None)



# btn1 = Button(100, 100, 100, 100, borderRadius=20, borderWidth=5, fill='pink')

# def redrawAll(app):
#   btn1.draw()

# def onMousePress(app, mouseX, mouseY):
#   btn1.updateActive(mouseX, mouseY, True)

# def onMouseMove(app, mouseX, mouseY):
#   btn1.updateHover(mouseX, mouseY)

# def onMouseRelease(app, mouseX, mouseY):
#   btn1.updateActive(mouseX, mouseY, False)

# runApp(width=800, height=800)

# s1 = Slider(100, 100, 200, 5, 10)

# def redrawAll(app):
#   s1.draw()

# def onMousePress(app, mouseX, mouseY):
#   s1.mousePress(mouseX, mouseY)

# def onMouseDrag(app, mouseX, mouseY):
#   s1.mouseDrag(mouseX, mouseY)

# def onMouseMove(app, mouseX, mouseY):
#   s1.mouseMove(mouseX, mouseY)

# def onMouseRelease(app, mouseX, mouseY):
#   s1.mouseRelease()

# runApp(width=800, height=800)
