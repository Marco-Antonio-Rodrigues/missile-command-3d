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
    glPointSize(50* size)
    glBegin(GL_POINTS)
    for posicion, digito in enumerate(str(digitos)):
        for linha, pixel_linha in enumerate(pixel_digits[digito]):
            for coluna, pixel in enumerate(pixel_linha):
                if pixel == 1:
                    glVertex2f(coluna * size + posicion, -linha * size)
    glEnd()


# Função para desenhar os pontos
def draw_scoreboard(digitos, x, y,z):
    glPushMatrix()
    glColor3f(1, 1, 1)
    glTranslatef(x, y, z)
    draw_digitos(digitos)
    glPopMatrix()


# Função para desenhar o HP
def draw_hp(digitos, x, y,z):
    
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
