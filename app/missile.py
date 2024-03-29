from OpenGL.GL import *
from OpenGL.GLU import *

list_missile = []

from math import degrees, sin

from OpenGL.GL import *
from OpenGL.GLU import *

from app.explosion import Explosion
from app.texture import Texture
from app.utils import load_obj


class Missile:
    def __init__(self, missile_id, start, target, scale=0.12, rotation=0):
        self.id = missile_id
        self.target = target
        self.start = start
        self.pos = start
        self.scale = scale
        self.rotation = rotation
        self.rotation_x = degrees(sin(target[1]))
        self.texture = Texture("images/missile.png")
        list_missile.append(self)

    def draw(self):
        glPushMatrix()
        self.texture.bind()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glRotatef(self.rotation, 0, 0, 1)
        glRotatef(-90 + self.rotation_x, 1, 0, 0)
        glScalef(self.scale, self.scale, self.scale)
        glCallList(self.id)
        self.texture.unbind()
        glPopMatrix()

    def update(self):
        # Verifica se o missile chegou ao alvo com uma margem de erro
        margin_of_error = 0.009
        distance_to_target = (
            sum((self.pos[i] - self.target[i]) ** 2 for i in range(3)) ** 0.5
        )
        if distance_to_target < margin_of_error:
            Explosion(self.pos[0], self.pos[1], self.pos[2])
            list_missile.remove(self)
            del self
        else:
            self.rotation += 1
            for i in range(3):
                self.pos[i] += (self.target[i] - self.start[i]) * 0.05
            self.draw()


def carrega_missile(missile_id):
    glNewList(missile_id, GL_COMPILE)
    vertices, faces = load_obj("assets/missile.obj")
    for face in faces:
        if len(face) == 4:
            glBegin(GL_QUADS)
        else:
            glBegin(GL_POLYGON)
        for vertex_index in face:
            vertex = vertices[vertex_index - 1]
            glTexCoord3f(vertex[0], vertex[1], vertex[2])
            glVertex3fv(vertex)
        glEnd()
    glEndList()
