import pyautogui
import pygame as pg
from numpy import sqrt as sqrt
from OpenGL.GL import *
from OpenGL.GLU import *
from time import sleep

from app.constants import ASPECT, HEIGHT, WIDTH


def game_over(width, height, texture):
    # Desenhando game over
    glPushMatrix()
    glTranslatef(-2, 6, -19)
    glScalef(width / 100, height / 110, 1)
    texture.bind()
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0), glVertex3f(-1, -1, 0)
    glTexCoord2f(1, 0), glVertex3f(1, -1, 0)
    glTexCoord2f(1, 1), glVertex3f(1, 1, 0)
    glTexCoord2f(0, 1), glVertex3f(-1, 1, 0)

    glEnd()
    texture.unbind()
    glPopMatrix()
    glFlush()
    pg.display.flip()


def tela_for_mundo_3d(x_tela, y_tela, display=(WIDTH, HEIGHT)):
    x_normalized = float(2 * x_tela / display[0] - 1)
    y_normalized = float(1 - 2 * y_tela / display[1])
    target = [x_normalized * 0.75, y_normalized * 0.40, -1]
    return target


def load_obj(filename):
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
                faces.append(list(map(int, [val.split("/")[0] for val in values[1:]])))
    return vertices, faces


def toca_musica(game_over_flag):
    # carrega a musica
    
    pg.mixer.music.load("audio/mcomeco.mp3")
    pg.mixer.music.play()
    sleep(1.47)
    # carrega o loop da musica
    pg.mixer.music.load("audio/mloop.mp3")
    pg.mixer.music.play(-1)
    while pg.mixer.music.get_busy():
        # verifica se deu gameover antes da musica acabar
        if game_over_flag == True:
            pg.mixer.music.stop()


def config_3d():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50)
    glMatrixMode(GL_MODELVIEW)


def resize_viewport(width, height):
    global WIDTH, HEIGHT, ASPECT
    WIDTH = width
    HEIGHT = height
    ASPECT = float(WIDTH / HEIGHT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, WIDTH, HEIGHT)
    force_mouse_center()


def force_mouse_center():
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = (
        screen_width // 2,
        screen_height // 2,
    )  # Calcula o centro da tela
    pyautogui.moveTo(center_x, center_y)