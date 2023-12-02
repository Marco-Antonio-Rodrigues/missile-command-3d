import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

from app.constants import HEIGHT, HEIGHT_WORLD, WIDTH, WIDTH_WORLD


def load_texture(filename):
    # carregamento da textura feita pelo módulo PIL
    img = Image.open(filename)  # abrindo o arquivo da textura
    img = img.transpose(
        Image.FLIP_TOP_BOTTOM
    )  # espelhando verticalmente a textura (normalmente, a coordenada y das imagens cresce de cima para baixo)
    imgData = img.convert(
        "RGBA"
    ).tobytes()  # convertendo a imagem carregada em bytes que serão lidos pelo OpenGL

    # criando o objeto textura dentro da máquina OpenGL
    texId = glGenTextures(1)  # criando um objeto textura
    glBindTexture(GL_TEXTURE_2D, texId)  # tornando o objeto textura recém criado ativo
    glTexParameteri(
        GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR
    )  # definindo que textura será suavizada ao ser aplicada no objeto
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(
        GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE
    )  # definindo que a cor da textura substituirá a cor do polígono
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        img.width,
        img.height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        imgData,
    )  # enviando os dados lidos pelo módulo PIL para a OpenGL
    glBindTexture(GL_TEXTURE_2D, 0)  # tornando o objeto textura inativo por enquanto

    # retornando o identificador da textura recém-criada
    return texId


def game_over(width, height, texture):
    config_2d()
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

def tela_for_mundo_2d(x_tela, y_tela):
    x_tela_centro = x_tela - WIDTH / 2
    y_tela_centro = y_tela - HEIGHT / 2
    x_mundo = x_tela_centro * (WIDTH_WORLD / WIDTH)
    y_mundo = y_tela_centro * (HEIGHT_WORLD / HEIGHT)
    return x_mundo, y_mundo


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


def config_2d():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(
        -WIDTH_WORLD / 2, WIDTH_WORLD / 2, -HEIGHT_WORLD / 2, HEIGHT_WORLD / 2, -1, 1
    )


def config_3d():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50)
    glMatrixMode(GL_MODELVIEW)


def resize_viewport(width_tela, height_tela):
    global WIDTH, HEIGHT, WIDTH_WORLD, HEIGHT_WORLD
    aspect = float(width_tela/height_tela )
    WIDTH = width_tela
    HEIGHT = height_tela
    glViewport(0, 0, int(WIDTH), int(HEIGHT))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if width_tela >= height_tela:
        glOrtho(-WIDTH_WORLD / 2*aspect, WIDTH_WORLD / 2*aspect, -HEIGHT_WORLD / 2, HEIGHT_WORLD / 2, -1, 1)
    else:
        glOrtho(-WIDTH_WORLD / 2, WIDTH_WORLD / 2, (-HEIGHT_WORLD / 2)/aspect, (HEIGHT_WORLD / 2)/aspect, -1, 1)

def desenhaTerreno():
    
    L = 500
    incr = 1
    y = -1
    # y = -0.5
    glColor3f(0,0,1)
    glBegin(GL_LINES)
    for i in range(-L, L+1, incr):
		# // Verticais
        glVertex3f(i,y,-L)
        glVertex3f(i,y,L)

		# // Horizontais
        glVertex3f(-L,y,i)
        glVertex3f(L,y,i)
    glEnd()
