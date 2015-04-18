from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src import display

class Example(display.Display):
  # Keyboard function
  def keyboard(self, key, x, y):
    (x, y, z)  = self.pos
    (ya, p, r) = self.ypr
    dPos = 0.1
    dRot = 0.1

    # Change lateral position
    if(key == "w"):
      x -= dPos
    if(key == "a"):
      y -= dPos
    if(key == "s"):
      x += dPos
    if(key == "d"):
      y += dPos
    if(key == "q"):
      z -= dPos
    if(key == "e"):
      z += dPos

    # Change orientation
    if(key == "i"):
      p -= dRot
    if(key == "j"):
      ya -= dRot
    if(key == "k"):
      p += dRot
    if(key == "l"):
      ya += dRot
    if(key == "u"):
      r -= dRot
    if(key == "o"):
      r += dRot

    # Reset position and orientation
    if(key == "r"):
      (x, y, z)  = (0, 0, 0)
      (ya, p, r) = (0, 0, 0)

    self.pos = (x, y, z)
    self.ypr = (ya, p, r)

  # Smoothly change orientation if mouse if moved
  def mouseMotion(self, x, y, dx, dy):
    (y, p, r) = self.ypr
    self.ypr = (y + dx/500.0, p + dy/500.0, r)
 
  # Simple exmaple draw function
  def draw(self):
    glutWireCube(1.0)

# Run example
if(__name__ == "__main__"):
  Example().run()
