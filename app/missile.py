import math
import random

from OpenGL.GL import *
from OpenGL.GLU import *

list_missile = []


class Missile:
    def __init__(self, x=0, y=0, ray=0.5, edges=36):
        self.x = x
        self.y = y
        self.ray = ray
        self.edges = edges
        list_missile.append(self)

    def draw(self, pos_x=None, pos_y=None, ray=None, edges=None):
        if pos_x:
            self.x = pos_x
        if pos_y:
            self.y = pos_y
        if ray:
            self.ray = ray
        if edges:
            self.edges = edges

        pos_x = self.x
        pos_y = self.y

        colors_list = [
            (1, 0, 0),
            (1, 1, 0),
            (1, 1, 1),
            (1, 0.8, 0),
            (1, 0.6, 0),
            (1, 0.4, 0),
        ]
        number_random = random.randint(0, len(colors_list) - 1)
        glColor(colors_list[number_random])

        glPushMatrix()
        glTranslatef(pos_x, pos_y, 0)
        glScalef(self.ray / 2, self.ray / 2, 1)  # Matriz de escala uniforme

        glBegin(GL_POLYGON)
        for i in range(0, self.edges):
            ang = i * (2.0 * math.pi / self.edges)
            x = math.cos(ang)
            y = math.sin(ang)
            glVertex2f(x, y)

        glEnd()
        glPopMatrix()
        glFlush()

    def update(self):  # Aumenta o raio de efeito do missil
        if self.ray < 1:
            self.ray += 0.002
            self.draw()
        else:
            list_missile.remove(self)
            del self
