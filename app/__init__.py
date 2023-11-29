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
from app.utils import (
    config_2d,
    config_3d,
    game_over,
    load_texture,
    resize_viewport,
    tela_for_mundo_3d,
    toca_musica,
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


def scenario(width, height):
    glEnable(GL_TEXTURE_2D)
    # Desenhando galaxy
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_galaxy)
    glTranslatef(0, height, 0)
    glScalef(width, height + height * 0.85, 1)
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0), glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 0), glVertex3f(1, -1, 1)
    glTexCoord2f(1, 1), glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1), glVertex3f(-1, 1, 1)

    glEnd()
    glPopMatrix()

    # Desenhando Base
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_planet)
    glTranslatef(0, -height + (height * 0.15), 0)
    glScalef(width, height * 0.15, 1)
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0), glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 0), glVertex3f(1, -1, 1)
    glTexCoord2f(1, 1), glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1), glVertex3f(-1, 1, 1)

    glEnd()
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)


def draw():
    global asteroids_killed, life
    pg.display.flip()  # atualiza toda a tela
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # limpa a tela
    config_2d()
    scenario(WIDTH_WORLD / 2, HEIGHT_WORLD / 2)

    for asteroid in list_asteroids:  # Atualiza o Status dos Asteroides
        if asteroid.update():
            impact.play()  # toca o som do impacto do asteroide na terra
            life -= 20

    for explosion in list_explosion:
        explosion.update()

    draw_scoreboard(asteroids_killed, -WIDTH_WORLD / 2 * 0.95, HEIGHT_WORLD / 2 * 0.95)
    draw_hp(life, WIDTH_WORLD / 2 * 0.8, HEIGHT_WORLD / 2 * 0.95)

    for asteroid in list_asteroids:  # Checa se uma explosão atingiu um asteroide
        for explosion in list_explosion:
            if asteroid.Colide(explosion.x, explosion.y, explosion.ray):
                # expmis.play()  # toca o som da explosao acertando um asteroide
                asteroids_killed += 1
                break

    config_3d()
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
    global game_over_flag
    global asteroids_killed
    global life

    time_click = 1000
    last_click = 0
    # music_thread.start()
    while True:
        if (
            asteroids_killed == dif + 20
        ):  # A cada 20 asteroides destruidos o jogo aumenta sua dificuldade
            cond = cond - 2
            dif = dif + 20

        if len(list_asteroids) < 20 and randint(-cond, cond) == 0:
            Asteroids()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                click_atual = pg.time.get_ticks()
                # verifica se ja passou o intervalo do ultimo clique
                if click_atual - last_click >= time_click:
                    last_click = click_atual
                    x_tela, y_tela = event.pos
                    target = tela_for_mundo_3d(x_tela, y_tela)
                    if True:
                        # expmis.play()  # toca o som da explosao
                        config_3d()
                        start = list(glGetDoublev(GL_MODELVIEW_MATRIX))
                        start = [start[3][0], start[3][1], start[3][2]]
                        Missile(start, target)

            if event.type == pg.VIDEORESIZE:
                width, height = event.size
                resize_viewport(width, height)
        draw()
        if life == 0:
            game_over_flag = True
            game_over(WIDTH_WORLD, HEIGHT_WORLD, texture_game_over)
            # pg.mixer.music.load("audio/mgameover.mp3")
            # pg.mixer.music.play()
            sleep(2)
            quit()
        CLOCK.tick(60)
