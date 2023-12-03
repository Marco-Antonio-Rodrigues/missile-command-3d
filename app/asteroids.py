import random

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from app.utils import mod as mod
from app.explosion import Explosion
from app.texture import Texture

list_asteroids = []


class Asteroids:
    def __init__(self, stacks=8, sectors=8, x=0, y=0, z=0, ray=0.5): 
        self.x = x
        self.y = y
        self.z = z
        self.ray = ray
        list_asteroids.append(self)
        self.n_stacks = stacks              # fatiamento vertical da esfera 
        self.n_sectors = sectors            # fatiamento horizontal da esfera
        self.texture = Texture("images/moon.jpg")

        self.xaux = random.randint(-9,9)
        self.yaux = 3.5
        self.zaux = -10
        self.ajusteX = mod(0.005*self.xaux) #Razão de ajuste no eixo X
        self.ajusteY = mod(0.005*self.yaux)   #Razão de ajuste no eixo Y
        

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
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        self.texture.bind()
        glTranslatef(self.xaux, self.yaux, self.zaux)
        glScale(self.ray / 2, self.ray / 2, self.ray / 2)
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

    def colide(self, x=None, y=None, z=None, ray=None):  # Checa se o asteroide colidiu e o remove
        if x and y and z and ray:
            distance = np.sqrt((self.xaux - x) ** 2 + (self.yaux - y) ** 2 +(self.zaux - z) ** 2)
            #print(distance)
            if distance <= self.ray or distance <= ray:
                Explosion(8, 8, self.xaux, self.yaux - self.ray, self.zaux)
                list_asteroids.remove(self)
                del self
                return True
        return False

    def update(self):
        if self.yaux > -2 and self.xaux >0:     #Se na direita
            self.xaux -= self.ajusteX
            self.yaux -= self.ajusteY
            self.zaux +=0.05
            self.draw()
            return False
        elif self.yaux > -2 and self.xaux < 0:  # Se Na esquerda
            self.xaux += self.ajusteX
            self.yaux -= self.ajusteY
            self.zaux +=0.05
            self.draw()
            return False
        else:                                   # Se colidiu com a terra
            list_asteroids.remove(self)
            del self
            return True
