from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *

from app.texture import Texture


class Ground:
    def __init__(self,y=-1,L=500):
        self.y = y
        self.L = L
        self.texture = Texture("images/piso.jpg")

    def draw(self):
        glColor3f(1, 0.8, 0.6)
        self.texture.bind()
        glBegin(GL_QUADS)
        glTexCoord2f(-100, -100)
        glVertex3f(-self.L, self.y, self.L)

        glTexCoord2f(100, -100)
        glVertex3f(self.L, self.y, self.L)

        glTexCoord2f(100, 100)
        glVertex3f(self.L, self.y, -self.L)

        glTexCoord2f(-100, 100)
        glVertex3f(-self.L, self.y, -self.L)
        glEnd()
        self.texture.unbind()
