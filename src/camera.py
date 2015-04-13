from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

class Camera(object):
  # Initialization function
  def __init__(self, width, height):
    self.width = width
    self.height = height

  # GL to be used before drawing
  def preGL(self):
    # Clear perspective matrix, and update it (useful for resizing)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Degree of FOV, width / height ratio, min dist, max dist
    gluPerspective(60, (self.width * 1.0) / self.height, 0.2, 1000)

    # Clear the model view, and the depth bit
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_DEPTH_BUFFER_BIT)

  # Draw function
  def draw(self, drawFunc, pos, ypr):
    # Unpack position and orientation
    (x, y, z) = pos
    (yaw, pitch, roll) = ypr

    # Get set up
    self.preGL()
    
    # Do translations for correct viewing
    glRotatef(-(pitch * 360) / (2 * math.pi), 1, 0, 0)
    glRotatef(-(yaw * 360) / (2 * math.pi), 0, 1, 0)
    glRotatef((roll * 360) / (2 * math.pi), 0, 0, 1)
    glTranslatef(-y, z, -x)

    # Call user draw function
    drawFunc()
