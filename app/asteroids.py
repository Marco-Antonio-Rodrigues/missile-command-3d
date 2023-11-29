import math
import random

from OpenGL.GL import *
from OpenGL.GLU import *

from app.explosion import Explosion
from app.constants import HEIGHT_WORLD, WIDTH_WORLD

list_asteroids = []


class Asteroids:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.xaux = random.randint(-((WIDTH_WORLD / 2) - 1), WIDTH_WORLD / 2 - 1)
        self.yaux = 10
        self.ray = 0.4 * random.randint(1, 2)
        self.edges = 36
        list_asteroids.append(self)

    def draw(self, pos_x=None, pos_y=None, ray=None, edges=None):
        if pos_x:
            self.x = pos_x
        if pos_y:
            self.y = pos_y
        if ray:
            self.ray = ray
        if edges:
            self.edges = edges

        pos_x = self.xaux
        pos_y = self.yaux

        glColor((1, 1, 1))

        glPushMatrix()
        glTranslatef(pos_x, pos_y, 0)
        glScalef(self.ray / 2, self.ray / 2, 1)  # matriz de escala uniforme
        glBegin(GL_POLYGON)
        for i in range(0, self.edges):
            ang = i * (2.0 * math.pi / self.edges)
            x = math.cos(ang)
            y = math.sin(ang)
            glVertex2f(x, y)

        glEnd()
        glPopMatrix()
        glFlush()

    def Colide(
        self, x=None, y=None, ray=None
    ):  # Checa se o asteroide colidiu e o remove
        if x and y and ray:
            distance = math.sqrt((self.xaux - x) ** 2 + (self.yaux - y) ** 2)
            if distance < self.ray or distance < ray:
                Explosion(self.xaux, self.yaux - self.ray / 2)
                list_asteroids.remove(self)
                del self
                return True
        return False

    def update(self):
        if self.yaux > -HEIGHT_WORLD / 2 * 0.8:
            self.yaux -= 0.02
            self.draw()
            return False
        else:  # Se colidiu com a terra
            Explosion(self.xaux, self.yaux - self.ray)
            list_asteroids.remove(self)
            del self
            return True
