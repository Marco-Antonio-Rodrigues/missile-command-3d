import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
import pyautogui

from app.constants import WIDTH,HEIGHT, ASPECT

def game_over(width, height, texture):
    glEnable(GL_TEXTURE_2D)
    # Desenhando game over
    glPushMatrix()
    glScalef(width / 4, height / 4, 1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0), glVertex3f(-1, -1, 0)
    glTexCoord2f(1, 0), glVertex3f(1, -1, 0)
    glTexCoord2f(1, 1), glVertex3f(1, 1, 0)
    glTexCoord2f(0, 1), glVertex3f(-1, 1, 0)

    glEnd()
    glDisable(GL_TEXTURE_2D)
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
    while pg.mixer.music.get_busy():
        # verifica se deu gameover antes da musica acabar
        if game_over_flag == True:
            pg.mixer.music.stop()

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
    ASPECT = float(WIDTH/HEIGHT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, WIDTH, HEIGHT)
    force_mouse_center()
  
def force_mouse_center(): 
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2# Calcula o centro da tela
    pyautogui.moveTo(center_x, center_y)