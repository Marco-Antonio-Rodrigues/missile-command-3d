import random

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from app.texture import Texture


class Score:
    def __init__(self):
        self.hp = Texture("images/hp.png")
        self.score = Texture("images/points.png")

    def draw(self) -> None:
        glPushMatrix()
        glScale(15, 15, 1)
        self.score.bind()
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex3f(-0.7, 0.2, -21)  # superior esquerdo
        glTexCoord2f(0, 0)
        glVertex3f(-0.7, 0, -21)  # inferior esquerdo
        glTexCoord2f(1, 0)
        glVertex3f(-0.3, 0, -21)  # inferior direito
        glTexCoord2f(1, 1)
        glVertex3f(-0.3, 0.2, -21)  # superior direito
        glEnd()
        self.score.unbind()

        self.hp.bind()
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex3f(0, 0.2, -21)  # superior esquerdo
        glTexCoord2f(0, 0)
        glVertex3f(0, 0, -21)  # inferior esquerdo
        glTexCoord2f(1, 0)
        glVertex3f(0.4, 0, -21)  # inferior direito
        glTexCoord2f(1, 1)
        glVertex3f(0.4, 0.2, -21)  # superior direito
        glEnd()
        self.hp.unbind()

        glPopMatrix()

    def update(self):
        self.draw()
