from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import camera
import time

class Display(object):
  # Inheritrance convinience functions
  def init(self): pass
  def close(self): pass
  def mouse(self, mouseButton, buttonState, x, y): pass
  def mouseMotion(self, x, y, dx, dy): pass
  def passiveMouseMotion(self, x, y, dx, dy): pass
  def keyboard(self, key, x, y): pass
  def specialKeys(self, key, x, y): pass
  def timerFired(self, value): pass
  def draw(self): pass
 
  # Initialization function
  def __init__(self, width = 1280, height = 720, frameName = "OpenGL"):
    self.frameSize = (self.width, self.height) = (width, height)
    self.frameName = frameName
    self.timerDelay = 20
 
    self.clearColor = (135.0/255, 206.0/255, 250.0/255, 1)
    self.defaultColor = (1, 1, 1)
    
    # Camera positioning
    self.pos = (0, 0, 0)
    self.ypr = (0, 0, 0)
    self.init()
    
    # Set up graphics
    self.initGL()
    self.initGLUT()
    self.camera = camera.Camera(self.width, self.height) 

    # For mouse motion
    self._mouseX = 0
    self._mouseY = 0

  # One-time GL commands
  def initGL(self):
    glClearColor(*self.clearColor)

  # Initialize the window manager (GLUT)
  def initGLUT(self):
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(*self.frameSize)
    glutCreateWindow(self.frameName)
  
    # Register all the convenience functions
    glutDisplayFunc(self.drawWrapper)
    glutIdleFunc(self.drawWrapper)
    glutTimerFunc(self.timerDelay, self.timerFired, 0)
    glutMouseFunc(self.mouse)
    glutMotionFunc(self.mouseMotionWrapper)
    glutPassiveMotionFunc(self.passiveMouseMotionWrapper)
    glutKeyboardFunc(self.keyboard)
    glutSpecialFunc(self.specialKeys)
    glutReshapeFunc(self.reshape)

    # Try to register a close function (fall back to a different one)
    try:
      glutCloseFunc(self.close)
    except:
      glutWMCloseFunc(self.close)

  # GL commands executed before drawing
  def preGL(self):
    glShadeModel(GL_FLAT)
    glEnable(GL_DEPTH_TEST)

    # Set up colors and clear buffers
    glClearColor(*self.clearColor)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(*self.defaultColor)
    glLoadIdentity()
    
  # Commands after GL is done
  def postGL(self):
    glutSwapBuffers()
    time.sleep(1/60.0)
  
  # Wrapper to re-register timer event
  def timerFiredWrapper(self, value):
    self.timerFired(value)
    glutTimerFunc(self.timerDelay, self.timerFired, value + 1)

  # Wrapper to handle as much GL as possible
  def drawWrapper(self):
    self.preGL()
    
    # Let the camera draw the view
    self.camera.draw(self.draw, self.pos, self.ypr)
    self.postGL()

  # Wrapper to pass change in position as well as position
  # Only called when mouse motion and button pressed
  def mouseMotionWrapper(self, x, y):
    if(self._mouseX == None or self._mouseY == None):
      (self._mouseX, self._mouseY) = (x, y)

    (dx, dy) = (x - self._mouseX, y - self._mouseY)
    self.mouseMotion(x, y, dx, dy)
    (self._mouseX, self._mouseY) = (x, y)

  # Wrapper to pass change in position as well as position
  # Called when mouse motion and not button pressed
  def passiveMouseMotionWrapper(self, x, y):
    if(self._mouseX == None or self._mouseY == None):
      (self._mouseX, self._mouseY) = (x, y)

    (dx, dy) = (x - self._mouseX, y - self._mouseY)
    self.passiveMouseMotion(x, y, dx, dy)
    (self._mouseX, self._mouseY) = (x, y)

  # Update when resizing the window
  def reshape(self, width, height):
    if(self.width != width or self.height != height):
      glutReshapeWindow(width, height)
      self.camera.width = width
      self.camera.height = height

  # Run the GL
  def run(self):
    glutMainLoop()
