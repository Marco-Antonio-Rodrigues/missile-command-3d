from OpenGL.GL import *
from OpenGL.GLU import *

list_missile = []

from OpenGL.GL import *
from OpenGL.GLU import *

from app.colision import Colision
from app.utils import load_obj, load_texture


class Missile:
    def __init__(self, start, target, scale=0.15, rotation=0):
        self.target = target
        self.start = start
        self.pos = start
        self.scale = scale
        self.rotation = rotation
        self.vertices, self.faces = load_obj("assets/missile.obj")
        self.texture = load_texture("images/texture.png")
        list_missile.append(self)

    def draw(self):
        glPushMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        # glRotatef(self.rotation,0,1, 0)
        glRotatef(-90, 1, 0, 0)
        glScalef(self.scale, self.scale, self.scale)
        for face in self.faces:
            if len(face) == 4:
                glBegin(GL_QUADS)
            else:
                glBegin(GL_POLYGON)
            for vertex_index in face:
                vertex = self.vertices[vertex_index - 1]
                glTexCoord3f(vertex[0], vertex[1], vertex[2])
                glVertex3fv(vertex)
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)
        glPopMatrix()

    def update(self):
        # Verifica se o missile chegou ao alvo com uma margem de erro
        margin_of_error = 0.1
        distance_to_target = (
            sum((self.pos[i] - self.target[i]) ** 2 for i in range(3)) ** 0.5
        )

        if distance_to_target < margin_of_error:
            Colision(self.pos[0], self.pos[1])
            list_missile.remove(self)
            del self
        else:
            self.rotation += 1
            for i in range(3):
                self.pos[i] += (self.target[i] - self.start[i]) * 0.02
            self.draw()
