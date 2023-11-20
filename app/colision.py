import random

import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

list_colision = []


class Colision:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.rotate = 0
        list_colision.append(self)

    def draw(self, pos_x=None, pos_y=None):
        if pos_x:
            self.x = pos_x
        if pos_y:
            self.y = pos_y

        pos_x = self.x
        pos_y = self.y
        num_particles = 10
        explosion_radius = 0.3
        particle_size = 10

        colors_list = [(1, 0, 0), (0.4, 0, 0), (0.2, 0, 0), (1, 0.5, 0)]

        glPushMatrix()
        glTranslatef(pos_x, pos_y, 0)
        glRotatef(self.rotate, 1, 1, 1)

        glPointSize(particle_size)  # Define o tamanho das partículas
        glColor3fv((1, 0, 0))  # Cor das partículas (vermelho)

        glBegin(GL_POINTS)  # Sprite da explosão
        for _ in range(num_particles):
            number_random = random.randint(0, len(colors_list) - 1)
            glColor(colors_list[number_random])
            x, y, z = (
                random.uniform(-explosion_radius, explosion_radius),
                random.uniform(-explosion_radius, explosion_radius),
                random.uniform(-explosion_radius, explosion_radius),
            )
            glVertex3f(x, y, z)
        glEnd()

        glPopMatrix()
        glFlush()

    def update(self):  # Animação da explosão
        if self.rotate < 360:
            self.rotate += 5
            self.draw()
        else:
            list_colision.remove(self)
            del self
