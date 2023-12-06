import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *


class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, vec):
        return Vec3(self.x + vec.x, self.y + vec.y, self.z + vec.z)

    def __mul__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def mag(self):
        return numpy.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normaliza(self):
        m = self.mag()
        self.x = self.x / m
        self.y = self.y / m
        self.z = self.z / m

    def prodVetorial(self, vec):
        return Vec3(
            self.y * vec.z - self.z * vec.y,
            self.z * vec.x - self.x * vec.z,
            self.x * vec.y - self.y * vec.x,
        )


class Camera:
    def __init__(self, pos=Vec3(0, 0, 0)):
        self.m_pos = pos
        self.m_dir = Vec3(0, 0, -1)
        self.m_left = Vec3(-1, 0, 0)
        self.m_up = Vec3(0, 1, 0)
        self.m_yaw = 0
        self.m_pitch = 0
        self.pos_mira = Vec3(0, 0, -1)
        self.m_scl = 0.25
        self.m_veloc = Vec3(0,0,0)

    def ativar(self):
        look = self.m_pos + self.m_dir
        glLoadIdentity()
        gluLookAt(
            self.m_pos.x,
            self.m_pos.y,
            self.m_pos.z,
            look.x,
            look.y,
            look.z,
            self.m_up.x,
            self.m_up.y,
            self.m_up.z,
        )
    def left(self):
        self.m_veloc = self.m_left *  self.m_scl
        self.m_pos =  self.m_pos +  self.m_veloc
     
    def right(self):
        self.m_veloc = self.m_left *  (-self.m_scl)
        self.m_pos =  self.m_pos +  self.m_veloc
        
    def down(self):
        self.m_veloc = self.m_dir *  (-self.m_scl)
        self.m_pos =  self.m_pos +  self.m_veloc
        
    def up(self):
        self.m_veloc = self.m_dir *  self.m_scl
        self.m_pos =  self.m_pos +  self.m_veloc
        
    def updateYaw(self, dYaw):
        self.m_yaw += dYaw / 5

    def updatePitch(self, dPitch):
        self.m_pitch += dPitch / 5

    def update(self):
        ang_x = float(numpy.radians(self.m_yaw))
        ang_y = float(numpy.radians(self.m_pitch))
        self.m_dir.x = numpy.sin(ang_x)
        self.m_dir.z = (-1) * (numpy.cos(ang_x))
        self.m_dir.y = numpy.tan(ang_y)
        self.m_dir.normaliza()
        self.m_left = self.m_up.prodVetorial(self.m_dir)
        self.pos_mira = self.m_pos + self.m_dir
        self.draw_mira()
        self.ativar()

    def draw_mira(self):
        vet1 = [self.pos_mira.x, self.pos_mira.y, self.pos_mira.z]
        glPushMatrix()
        glColor3f(1, 0, 0)
        glPointSize(10.0)
        glBegin(GL_POINTS)
        glVertex3fv(vet1)
        glEnd()
        glPopMatrix()


firstTimeMouse = True
lastMousePos_x = 0
lastMousePos_y = 0


def mouse_callback(xpos, ypos, camera):
    global firstTimeMouse, lastMousePos_x, lastMousePos_y
    if firstTimeMouse:
        dx = 0
        dy = 0
        lastMousePos_x = xpos
        lastMousePos_y = ypos
        firstTimeMouse = False

    dx = xpos - lastMousePos_x
    dy = ypos - lastMousePos_y
    lastMousePos_x = xpos
    lastMousePos_y = ypos
    camera.updateYaw(dx)
    camera.updatePitch(dy)
