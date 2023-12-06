import threading
from random import randint
from time import sleep

import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from app.asteroids import Asteroids, list_asteroids
from app.camera import Camera, mouse_callback
from app.constants import HEIGHT, WIDTH
from app.explosion import list_explosion
from app.ground import Ground
from app.missile import Missile, list_missile
from app.status_panel import draw_hp, draw_scoreboard
from app.utils import (
    config_3d,
    force_mouse_center,
    game_over,
    resize_viewport,
    tela_for_mundo_3d,
    toca_musica,
)

# configurações iniciais pygames
pg.init()
pg.display.set_caption("Missile Command")
CLOCK = pg.time.Clock()
display = (WIDTH, HEIGHT)
CANVAS = pg.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)
force_mouse_center()

expmis = pg.mixer.Sound("audio/boom12.wav")  # sons das explosoes
expast = pg.mixer.Sound("audio/boom10.wav")
impact = pg.mixer.Sound("audio/boom15.wav")

camera = Camera()
ground = Ground()

asteroids_killed = 0
life = 100
game_over_flag = False


glEnable(GL_LIGHTING)           #Habilitando luz
#glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)
    
luz_ambiente = (0.8,0.8,0.8,0.8)
luz_difusa = (0.7, 0.7, 0.7, 1.0)
luz_especular = (1.0, 1.0, 1.0, 1.0)
especularidade = 60
    
glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luz_ambiente)
glMaterialfv(GL_FRONT, GL_SPECULAR, luz_especular)
glMateriali(GL_FRONT, GL_SHININESS, especularidade)
glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luz_ambiente)
    
glLightfv(GL_LIGHT0,GL_AMBIENT, luz_ambiente)
glLightfv(GL_LIGHT0,GL_DIFFUSE, luz_difusa)
glLightfv(GL_LIGHT0,GL_SPECULAR, luz_especular )






def scenario():
                        # Desenhando Base
    glPushMatrix()
    ground.draw()
    glPopMatrix()


def draw():
    global asteroids_killed, life
    pg.display.flip()  # atualiza toda a tela
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # limpa a tela
    camera.update()
    config_3d()
    scenario()
    
    
    for asteroid in list_asteroids:  # Checa se uma explosão atingiu um asteroide
        for explosion in list_explosion:
            if asteroid.colide(explosion.x, explosion.y, explosion.z, explosion.ray):
                #expmis.play()  # toca o som da explosao acertando um asteroide
                asteroids_killed += 1
                break 
        for missile in list_missile:
            if asteroid.colide(missile.pos[0], missile.pos[1], missile.pos[2], 0.001):
                #expmis.play()  # toca o som da explosao acertando um asteroide
                asteroids_killed += 1
                break
            
            
    for asteroid in list_asteroids:  # Atualiza o Status dos Asteroides
        if asteroid.update():
            #impact.play()  # toca o som do impacto do asteroide na terra
            life -= 10
     
    for explosion in list_explosion:
       explosion.update()
    
    
    for missile in list_missile:
        missile.update()


#music_thread = threading.Thread(
#     target=toca_musica, args=(game_over_flag,)
# )                                                  # cria um thread exclusivo para tocar a musica sem afetar o jogo


def main():
    
    global list_asteroids
    global list_missile
    global game_over_flag
    global asteroids_killed
    global life
    #music_thread.start()
    
    asteroids_qtd = 3                           #Quantidade de asteroides simultaneos no jogo
    dif = 0                                     #Variável auxiliar, para aumentar a dificuldade
    mouse_bloqueado = True
    while True:
        if (asteroids_killed == dif + 100):     # A cada 100 asteroides destruidos o jogo aumenta sua dificuldade
            dif = dif + 100
            asteroids_qtd = asteroids_qtd + 1 

        if len(list_asteroids) < asteroids_qtd: #Cria os Asteroides
            Asteroids()
            
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                x_tela, y_tela = event.pos
                target = tela_for_mundo_3d(x_tela, y_tela)
                if True:
                    #expmis.play()  # toca o som da explosao
                    start = list(glGetDoublev(GL_MODELVIEW_MATRIX))
                    start = [start[3][0], start[3][1]-1, start[3][2]]
                    target = [camera.pos_mira.x, camera.pos_mira.y, camera.pos_mira.z]
                    Missile(start, target)

            if event.type == pg.VIDEORESIZE:
                width, height = event.size
                resize_viewport(width, height)
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mouse_bloqueado = not mouse_bloqueado
                    

        pg.mouse.set_visible(not mouse_bloqueado)
        pg.event.set_grab(mouse_bloqueado)
        if mouse_bloqueado:
            mouse_x, mouse_y = pg.mouse.get_pos()
            mouse_callback(mouse_x, display[1] - mouse_y, camera)

        draw()
        # if life == 0:
        # game_over_flag = True
        # game_over(WIDTH_WORLD, HEIGHT_WORLD, texture_game_over)
        # pg.mixer.music.load("audio/mgameover.mp3")
        # pg.mixer.music.play()
        # sleep(2)
        # quit()
        CLOCK.tick(60)
