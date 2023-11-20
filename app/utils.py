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


def tela_for_mundo(x_tela, y_tela):
    x_tela_centro = x_tela - WIDTH / 2
    y_tela_centro = y_tela - HEIGHT / 2
    x_mundo = x_tela_centro * (WIDTH_WORLD / WIDTH)
    y_mundo = y_tela_centro * (HEIGHT_WORLD / HEIGHT)
    return x_mundo, y_mundo
