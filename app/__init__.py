import threading
from random import randint
from time import sleep

import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from app.asteroids import Asteroids, list_asteroids
from app.colision import list_colision
from app.constants import HEIGHT, HEIGHT_WORLD, WIDTH, WIDTH_WORLD
from app.missile import Missile, list_missile
from app.status_panel import draw_hp, draw_scoreboard
from app.utils import load_texture, tela_for_mundo

# configurações iniciais
pg.init()
pg.display.set_caption("Missile Command")
pg.mouse.set_cursor(*pg.cursors.diamond)
CLOCK = pg.time.Clock()
display = (WIDTH, HEIGHT)
CANVAS = pg.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)


glOrtho(-WIDTH_WORLD / 2, WIDTH_WORLD / 2, -HEIGHT_WORLD / 2, HEIGHT_WORLD / 2, -1, 1)

glEnable(GL_TEXTURE_2D)  # habilitando o uso de texturas
glEnable(GL_BLEND)
# habilitando a funcionalidade de mistura (necessário para objetos transparentes)
glBlendFunc(
    GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
)  # definindo como a mistura entre objetos transparência deve ser realizada

texture_galaxy = load_texture("images/galaxia.png")
texture_planet = load_texture("images/planet.png")
texture_game_over = load_texture("images/game_over.png")


expmis = pg.mixer.Sound("audio/boom12.wav")  # sons das explosoes
expast = pg.mixer.Sound("audio/boom10.wav")
impact = pg.mixer.Sound("audio/boom15.wav")


def resize_viewport(width_tela, height_tela):
    global WIDTH, HEIGHT, WIDTH_WORLD, HEIGHT_WORLD
    glViewport(0, 0, int(WIDTH), int(HEIGHT))
    glLoadIdentity()
    glOrtho(
        -WIDTH_WORLD / 2, WIDTH_WORLD / 2, -HEIGHT_WORLD / 2, HEIGHT_WORLD / 2, -1, 1
    )


def scenario(width, height):
    # Desenhando galaxy
    glColor((0, 0, 0))
    glPushMatrix()
    glTranslatef(0, height, 0)
    glScalef(width, height + height * 0.85, 1)
    glBindTexture(GL_TEXTURE_2D, texture_galaxy)  # tornando a textura 1 ativa
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0), glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 0), glVertex3f(1, -1, 1)
    glTexCoord2f(1, 1), glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1), glVertex3f(-1, 1, 1)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)  # desativando todas as texturas
    glPopMatrix()

    # Desenhando Base
    glColor((1, 1, 0))
    glPushMatrix()
    glTranslatef(0, -height + (height * 0.15), 0)
    glScalef(width, height * 0.15, 1)
    glBindTexture(GL_TEXTURE_2D, texture_planet)  # tornando a textura 1 ativa
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0), glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 0), glVertex3f(1, -1, 1)
    glTexCoord2f(1, 1), glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1), glVertex3f(-1, 1, 1)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)  # desativando todas as texturas
    glPopMatrix()
    glFlush()


def game_over(width, height):
    # Desenhando game over
    glColor((1, 1, 0))
    glPushMatrix()
    glScalef(width / 4, height / 4, 1)
    glBindTexture(GL_TEXTURE_2D, texture_game_over)  # tornando a textura 1 ativa
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0), glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 0), glVertex3f(1, -1, 1)
    glTexCoord2f(1, 1), glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1), glVertex3f(-1, 1, 1)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)  # desativando todas as texturas
    glPopMatrix()
    glFlush()
    pg.display.flip()


def draw():
    global asteroids_killed, life
    pg.display.flip()  # atualiza toda a tela
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # limpa a tela
    scenario(WIDTH_WORLD / 2, HEIGHT_WORLD / 2)

    for missile in list_missile:  # Atualiza o Status das Explosoes
        missile.update()

    for asteroid in list_asteroids:  # Atualiza o Status dos Asteroides
        if asteroid.update():
            impact.play()  # toca o som do impacto do asteroide na terra
            life -= 20

    for colision in list_colision:  # Atualiza o Status das colisões
        colision.update()

    draw_scoreboard(asteroids_killed, -WIDTH_WORLD / 2 * 0.95, HEIGHT_WORLD / 2 * 0.95)
    draw_hp(life, WIDTH_WORLD / 2 * 0.8, HEIGHT_WORLD / 2 * 0.95)

    for asteroid in list_asteroids:  # Checa se uma explosão atingiu um asteroide
        for missile in list_missile:
            if asteroid.Colide(missile.x, missile.y, missile.ray):
                expmis.play()  # toca o som da explosao acertando um asteroide
                asteroids_killed += 1
                break


def toca_musica():
    global game_over_flag

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


music_thread = threading.Thread(
    target=toca_musica
)  # cria um thread exclusivo para tocar a musica sem afetar o jogo


asteroids_killed = 0
life = 100
game_over_flag = False


def main():
    x_tela = 0
    y_tela = 0
    x_mundo = 0
    y_mundo = 0
    cond = 40  # Dificuldade, quanto mais perto do 0, mais asteroids aparecem
    dif = 0  # Variável auxiliar, para aumentar a dificuldade

    global list_asteroids
    global list_missile
    global game_over_flag
    global asteroids_killed
    global life

    time_click = 1000
    last_click = 0
    music_thread.start()
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
                    x_tela, y_tela = pg.mouse.get_pos()
                    x_mundo, y_mundo = tela_for_mundo(x_tela, HEIGHT - y_tela)
                    if y_mundo > -HEIGHT_WORLD / 2.5:
                        expmis.play()  # toca o som da explosao
                        Missile(x=x_mundo, y=y_mundo)

            if event.type == pg.VIDEORESIZE:
                width, height = event.size
                resize_viewport(width, height)

        draw()
        CLOCK.tick(60)
        if life == 0:
            game_over_flag = True  # verificador para fazer a musica do jogo parar
            game_over(WIDTH_WORLD, HEIGHT_WORLD)
            pg.mixer.music.load("audio/mgameover.mp3")  # toca musica de gameover
            pg.mixer.music.play()
            sleep(5)  # deixar em 5 segundos, pois eh a duracao da musica de gameover
            quit()
