from OpenGL.GL import *
from OpenGL.GLU import *


class Obj:
    def __init__(self, filename, x=0, y=0, scale=0.5):
        vertices, faces = self.load_obj(filename)
        self.x = x
        self.y = y
        self.scale = scale
        self.vertices = vertices
        self.faces = faces

    def load_obj(self, filename):
        vertices = []
        faces = []
        with open(filename, "r") as file:
            for line in file:
                values = line.split()
                if not values:
                    continue
                if values[0] == "v":
                    vertices.append(list(map(float, values[1:4])))
                elif values[0] == "f":
                    faces.append(
                        list(map(int, [val.split("/")[0] for val in values[1:]]))
                    )
        return vertices, faces

    def draw_obj(self):
        self.scale += 1
        glPushMatrix()
        glRotatef(self.scale, 0, 1, 0)
        glTranslatef(0, 0, 0)
        # glScalef(10, 10, 10)
        glColor3f(1, 0, 0)
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex_index in face:
                vertex = self.vertices[vertex_index - 1]
                glVertex3fv(vertex)
        glEnd()
        glPopMatrix()

    def draw_textured_obj(self, texture):
        self.scale += 1
        glPushMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glTranslatef(self.x, self.y, -1)
        glRotatef(self.scale, 0, 1, 0)
        glScalef(0.15, 0.15, 0.15)
        for face in self.faces:
            glBindTexture(GL_TEXTURE_2D, texture)
            if len(face) == 4:
                glBegin(GL_QUADS)
            else:
                glBegin(GL_POLYGON)
            for vertex_index in face:
                vertex = self.vertices[vertex_index - 1]
                glTexCoord3f(
                    vertex[0], vertex[1], vertex[2]
                )  # Use as coordenadas de textura do modelo .obj (pode precisar de ajustes)
                glVertex3fv(vertex)
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)
        glPopMatrix()
