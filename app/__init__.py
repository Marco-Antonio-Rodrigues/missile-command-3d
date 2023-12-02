import threading
from random import randint
from time import sleep

import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from app.asteroids import Asteroids, list_asteroids
from app.explosion import list_explosion
from app.constants import HEIGHT, HEIGHT_WORLD, WIDTH, WIDTH_WORLD
from app.missile import Missile, list_missile
from app.status_panel import draw_hp, draw_scoreboard
# from app.camera import Camera,Vec3,mouse_callback
from app.utils import (
    config_3d,
    game_over,
    load_texture,
    resize_viewport,
    tela_for_mundo_3d,
    toca_musica,
    desenhaTerreno
)

# configurações iniciais pygames
pg.init()
pg.display.set_caption("Missile Command")
pg.mouse.set_cursor(*pg.cursors.diamond)
CLOCK = pg.time.Clock()
display = (WIDTH, HEIGHT)
CANVAS = pg.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)

texture_galaxy = load_texture("images/galaxia.png")
texture_planet = load_texture("images/planet.png")
texture_game_over = load_texture("images/game_over.png")

expmis = pg.mixer.Sound("audio/boom12.wav")  # sons das explosoes
expast = pg.mixer.Sound("audio/boom10.wav")
impact = pg.mixer.Sound("audio/boom15.wav")

asteroids_killed = 0
life = 100
game_over_flag = False

# camera = Camera(Vec3( 0, 0, 0))

def scenario(width, height):
    # Desenhando Base
    glPushMatrix()
    desenhaTerreno()
    glPopMatrix()
    
def draw():
    global asteroids_killed, life
    pg.display.flip()  # atualiza toda a tela
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # limpa a tela
    # camera.ativar()
    config_3d()
    for asteroid in list_asteroids:  # Atualiza o Status dos Asteroides
        if asteroid.update():
            # impact.play()  # toca o som do impacto do asteroide na terra
            life -= 20

    for explosion in list_explosion:
        explosion.update()
        
    for asteroid in list_asteroids:  # Checa se uma explosão atingiu um asteroide
        for explosion in list_explosion:
            if asteroid.colide(explosion.x, explosion.y, explosion.ray):
                # expmis.play()  # toca o som da explosao acertando um asteroide
                asteroids_killed += 1
                break

    scenario(WIDTH_WORLD / 2, HEIGHT_WORLD / 2)
    for missile in list_missile:
        missile.update()


# music_thread = threading.Thread(
#     target=toca_musica, args=(game_over_flag,)
# )  # cria um thread exclusivo para tocar a musica sem afetar o jogo

def main():
    cond = 40  # Dificuldade, quanto mais perto do 0, mais asteroids aparecem
    dif = 0  # Variável auxiliar, para aumentar a dificuldade

    global list_asteroids
    global list_missile
    # global game_over_flag
    # global asteroids_killed
    # global life
        
    # time_click = 1000
    # last_click = 0
    # music_thread.start()
    while True:
        # if (
        #     asteroids_killed == dif + 20
        # ):  # A cada 20 asteroides destruidos o jogo aumenta sua dificuldade
        #     cond = cond - 2
        #     dif = dif + 20

        if len(list_asteroids) < 20 and randint(-cond, cond) == 0:
            Asteroids()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                # click_atual = pg.time.get_ticks()
                # verifica se ja passou o intervalo do ultimo clique
                # if click_atual - last_click >= time_click:
                    # last_click = click_atual
                    x_tela, y_tela = event.pos
                    target = tela_for_mundo_3d(x_tela, y_tela)
                    if True:
                        # expmis.play()  # toca o som da explosao
                        start = list(glGetDoublev(GL_MODELVIEW_MATRIX))
                        start = [start[3][0], start[3][1], start[3][2]]
                        Missile(start, target)

            if event.type == pg.VIDEORESIZE:
                width, height = event.size
                resize_viewport(width, height)
        # mouse_x, mouse_y = pg.mouse.get_pos()
        # mouse_callback(mouse_x,display[1]-mouse_y,camera)
        draw()
        # if life == 0:
            # game_over_flag = True
            # game_over(WIDTH_WORLD, HEIGHT_WORLD, texture_game_over)
            # pg.mixer.music.load("audio/mgameover.mp3")
            # pg.mixer.music.play()
            # sleep(2)
            # quit()
        CLOCK.tick(60)
