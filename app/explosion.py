import random

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from app.texture import Texture

list_explosion = []

# ponto reset


class Explosion:
    def __init__(
        self, x=0, y=0, z=0, ray=0.5, stacks=8, sectors=8
    ):  # adicionar n stacks e sectors
        self.x = x
        self.y = y
        self.z = z
        self.ray = ray
        list_explosion.append(self)
        self.n_stacks = stacks  # fatiamento vertical da esfera sugerido 30
        self.n_sectors = sectors  # fatiamento horizontal da esfera sugerido 30
        self.texture = Texture("images/sun.jpg", True)

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

        # colors_list = [(1, 0, 0), (0.4, 0, 0), (0.2, 0, 0), (1, 0.5, 0)]

        glPushMatrix()
        glEnable(GL_DEPTH_TEST)
        self.texture.bind()
        glTranslatef(pos_x, pos_y, pos_z)
        glScale(self.ray / 2, self.ray / 2, self.ray / 2)
        glColor3fv((1, 1, 1))
        glEnable(GL_CULL_FACE)
        glFrontFace(GL_CCW)
        glCullFace(GL_BACK)

        # Cor das partículas (vermelho)

        for i in range(int(self.n_stacks)):
            glBegin(GL_TRIANGLE_STRIP)

            for j in range(self.n_sectors):
                index = indices[i][j]
                x, y, z = pontos[index]
                u = j / self.n_sectors
                v = i / self.n_stacks
                glTexCoord2f(u, v)
                glVertex3f(pos_x + x, pos_y + y, pos_z + z)

                index = indices[i + 1][j]
                x, y, z = pontos[index]
                u = j / self.n_sectors
                v = (i + 1) / self.n_stacks
                glTexCoord2f(u, v)
                glVertex3f(pos_x + x, pos_y + y, pos_z + z)

                if j == self.n_sectors - 1:
                    index = indices[i][0]
                    x, y, z = pontos[index]
                    u = 0
                    v = i / self.n_stacks
                    glTexCoord2f(u, v)
                    glVertex3f(pos_x + x, pos_y + y, pos_z + z)

                    index = indices[i + 1][0]
                    x, y, z = pontos[index]
                    u = 0
                    v = (i + 1) / self.n_stacks
                    glTexCoord2f(u, v)
                    glVertex3f(pos_x + x, pos_y + y, pos_z + z)

            glEnd()
        glPopMatrix()
        glDisable(GL_CULL_FACE)
        self.texture.unbind()

    def update(self):  # Animação da explosão
        if self.ray < 1:
            self.ray += 0.005
            self.draw()
        else:
            list_explosion.remove(self)
            del self
