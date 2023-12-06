from OpenGL.GL import *
from OpenGL.GLU import *

class Iluminacao():
    def __init__(self):
            
        posicaoLuz0 = (0, 2, 4, 1)
        
        luz_ambiente = (0.5,0.5,0.5, 1.0)
        luz_difusa = (0.7, 0.7, 0.7, 1.0)
        luz_especular = (1.0, 1.0, 1.0, 1.0)
        
        especularidade = (1.0, 1.0, 1.0, 1.0)
        aspecto_material = 60                   #shininess
            
        
        glMaterialfv(GL_FRONT, GL_SPECULAR, especularidade)
        glMateriali(GL_FRONT, GL_SHININESS, aspecto_material)
        
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luz_ambiente)

        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2,0.2,0.2,1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
        glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
        
        glLightfv(GL_LIGHT0, GL_POSITION, posicaoLuz0)
        
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)           #Habilitando luz
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
    