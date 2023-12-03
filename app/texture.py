from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image


class Texture:
    def __init__(self, filePath, mipmap=False):
        self.m_id = 0
        self.m_largura = 0
        self.m_altura = 0
        self.m_canais = 0
        self.load(filePath, mipmap)

    def load(self, filePath,mipmap):
        img = Image.open(filePath).transpose(Image.FLIP_TOP_BOTTOM)
        imgData = img.convert("RGBA").tobytes()

        self.m_largura, self.m_altura = img.size
        self.m_canais = 4

        self.m_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.m_id)

        if mipmap:
            gluBuild2DMipmaps(
                GL_TEXTURE_2D,
                GL_RGBA8,
                self.m_largura,
                self.m_altura,
                GL_RGBA,
                GL_UNSIGNED_BYTE,
                imgData,
            )
            glTexParameteri(
                GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR
            )
        else:
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGBA8,
                self.m_largura,
                self.m_altura,
                0,
                GL_RGBA,
                GL_UNSIGNED_BYTE,
                imgData,
            )
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glBindTexture(GL_TEXTURE_2D, 0)

    def bind(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.m_id)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
