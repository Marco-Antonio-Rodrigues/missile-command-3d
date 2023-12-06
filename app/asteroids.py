import random

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from app.explosion import Explosion
from app.texture import Texture
from app.utils import mod

list_asteroids = []


class Asteroids:
    def __init__(self, stacks=8, sectors=8, x=None, y=None, z=-5, ray=0.5):
        if x is None:
            x = random.randint(-9, 9)
        if y is None:
            y = random.randint(4, 6)
        self.x = x
        self.y = y
        self.z = z
        self.ray = ray
        list_asteroids.append(self)
        self.n_stacks = stacks  # fatiamento vertical da esfera
        self.n_sectors = sectors  # fatiamento horizontal da esfera
        self.texture = Texture("images/moon.jpg")
        
        self.ajusteY = mod(0.002 * self.y)  # Razão de ajuste no eixo Y

    def draw(self, pos_x=None, pos_y=None, pos_z=None):
        if pos_x:
            self.x = pos_x
        if pos_y:
            self.y = pos_y
        if pos_z:
            self.z = pos_z

        pos_x = self.x
        pos_y = self.y
        pos_z = self.z
        indices = []
        pontos = []
        PI = np.pi
        delta_Phi = PI / self.n_stacks
        delta_Theta = 2 * PI / self.n_sectors

        for i in range(int(self.n_stacks + 1)):
            Phi = -PI / 2.0 + i * delta_Phi
            temp = self.ray * np.cos(Phi)
            y = self.ray * np.sin(Phi)

            pt = []

            for j in range(self.n_sectors):
                Theta = j * delta_Theta
                x = temp * np.sin(Theta)
                z = temp * np.cos(Theta)

                pontos.append(np.array([x, y, z]))
                index = len(pontos) - 1
                pt.append(index)
            indices.append(pt)

        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        self.texture.bind()
        glTranslatef(self.x, self.y, self.z)
        glScale(self.ray, self.ray, self.ray)
        glColor3fv((1, 1, 1))
        glEnable(GL_CULL_FACE)
        glFrontFace(GL_CCW)
        glCullFace(GL_BACK)

        for i in range(int(self.n_stacks)):
            glBegin(GL_TRIANGLE_STRIP)

            for j in range(self.n_sectors):
                index = indices[i][j]
                x, y, z = pontos[index]
                u = j / self.n_sectors
                v = i / self.n_stacks
                glTexCoord2f(u, v)
                glVertex3f(x, y, z)

                index = indices[i + 1][j]
                x, y, z = pontos[index]
                u = j / self.n_sectors
                v = (i + 1) / self.n_stacks
                glTexCoord2f(u, v)
                glVertex3f(x, y, z)

                if j == self.n_sectors - 1:
                    index = indices[i][0]
                    x, y, z = pontos[index]
                    u = 0
                    v = i / self.n_stacks
                    glTexCoord2f(u, v)
                    glVertex3f(x, y, z)

                    index = indices[i + 1][0]
                    x, y, z = pontos[index]
                    u = 0
                    v = (i + 1) / self.n_stacks
                    glTexCoord2f(u, v)
                    glVertex3f(x, y, z)

            glEnd()
        glPopMatrix()
        glDisable(GL_CULL_FACE)
        glDisable(GL_TEXTURE_2D)
        self.texture.unbind()

    def colide(
        self, x=None, y=None, z=None, ray=None
    ):  # Checa se o asteroide colidiu e o remove
        if x and y and z and ray:
            distance = np.sqrt(
                (self.x - x) ** 2 + (self.y - y) ** 2 + (self.z - z) ** 2
            )
            if distance < self.ray*0.85:
                Explosion(self.x, self.y, self.z,self.ray)
                if self in list_asteroids:
                    list_asteroids.remove(self)
                    del self
                return True
        return False

    def update(self):
        if self.y > -0.25:
            self.y -= self.ajusteY
            self.draw()
            return False
        else:  # Se colidiu com a terra
            list_asteroids.remove(self)
            Explosion(self.x, self.y, self.z,self.ray)
            del self
            return True
