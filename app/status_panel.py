from OpenGL.GL import *
from OpenGL.GLUT import *
from pygame.locals import *

# Dicionário que define a representação pixelizada dos dígitos
pixel_digits = {
    "0": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    "1": [
        [0, 0, 1],
        [0, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
    ],
    "2": [
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
    ],
    "3": [
        [1, 1, 1],
        [0, 0, 1],
        [0, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    "4": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
    ],
    "5": [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    "6": [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    "7": [
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
    ],
    "8": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    "9": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    "H": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
    ],
    "P": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 0],
        [1, 0, 0],
    ],
    ":": [
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 0],
    ],
}


# Função para desenhar números na tela
def draw_digitos(digitos):
    size = 0.20  # size
    glPointSize(50 * size)
    glBegin(GL_POINTS)
    for posicion, digito in enumerate(str(digitos)):
        for linha, pixel_linha in enumerate(pixel_digits[digito]):
            for coluna, pixel in enumerate(pixel_linha):
                if pixel == 1:
                    glVertex2f(coluna * size + posicion, -linha * size)
    glEnd()


# Função para desenhar os pontos
def draw_scoreboard(digitos, x, y, z):
    glPushMatrix()
    glColor3f(1, 1, 1)
    glTranslatef(x, y, z)
    draw_digitos(digitos)
    glPopMatrix()


# Função para desenhar o HP
def draw_hp(digitos, x, y, z):
    glPushMatrix()
    glColor3f(1, 1, 1)
    glTranslatef(x - 2.5, y, z)

    glPopMatrix()

    glPushMatrix()
    glTranslatef(x, y, z)
    if digitos >= 80:
        glColor3f(0, 1, 0)

    elif digitos >= 40:
        glColor(1, 1, 0)

    else:
        glColor(1, 0, 0)
    draw_digitos(digitos)
    glPopMatrix()


def mini_map(list_objects, x, y, z):
    size = 0.20
    display = [[0] * 18 for _ in range(8)]
    for object in list_objects:
        if object.x <= 0:
            display[7 - int(object.y)][abs(int(object.x))] = 1
        else:
            display[7 - int(object.y)][int(object.x) + 8] = 1
    glPushMatrix()
    glLineWidth(5)
    glTranslatef(x, y, z)
    glColor3f(1, 0, 0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(-0.5, -2)
    glVertex2f(-0.5, 0.5)
    glVertex2f(4, 0.5)
    glVertex2f(4, -2)
    glEnd()

    glColor3f(1, 1, 1)
    glBegin(GL_POINTS)

    for linha, pixel_linha in enumerate(display):
        for coluna, pixel in enumerate(pixel_linha):
            if pixel == 1:
                glVertex2f(coluna * size, -linha * size)
    glEnd()

    glPopMatrix()
