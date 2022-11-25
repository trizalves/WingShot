#INTEGRANTES: DAVI PENA(32140381), BEATRIZ ALVES(32118929), LETÍCIA SILVA (32157843)

import pygame
import os
import time
import random
from pygame import mixer

pygame.font.init()
pygame.mixer.init()

#MUSICA
pygame.mixer.music.set_volume(0.9)
pygame.mixer.music.load("audios/musica_background.mp3")
pygame.mixer.music.play(-1)

#SOM GAME OVER
pygame.mixer.music.set_volume(0.1)
game_over = pygame.mixer.Sound("audios/game_over.mp3")

#SOM TIRO
pygame.mixer.music.set_volume(0.1)
som_tiro = pygame.mixer.Sound("audios/som_tiro.mp3")

#SOM COLISAO
pygame.mixer.music.set_volume(0.1)
som_colisao = pygame.mixer.Sound("audios/som_colisao.mp3")

#SOM CLIQUE
pygame.mixer.music.set_volume(0.2)
som_click = pygame.mixer.Sound("audios/click.mp3")

#SOM NIVEL
pygame.mixer.music.set_volume(0.1)
som_nivel = pygame.mixer.Sound("audios/level_up.mp3")


WIDTH, HEIGHT = 1280, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wing Shot")

# JOGADOR
picture = pygame.image.load("imagens/airplane.png")
NAVE_JOGADOR = pygame.transform.scale(picture, (130, 130))

# LASERS
LASER_VERMELHO = pygame.image.load(os.path.join("imagens/pixel_laser_red.png"))
LASER_VERDE = pygame.image.load(os.path.join("imagens/pixel_laser_green.png"))
LASER_ROXO = pygame.image.load(os.path.join("imagens/pixel_laser_purple.png"))
LASER_AZUL = pygame.image.load(os.path.join("imagens/pixel_laser_blue.png"))

# CARREGA AS IMAGENS
NAVE_VERMELHA = pygame.image.load(os.path.join("imagens/pixel_ship_red_small.png"))
NAVE_VERDE = pygame.image.load(os.path.join("imagens/pixel_ship_green_small.png"))
NAVE_VERDE2 = pygame.image.load(os.path.join("imagens/pixel_ship_green_small_2.png"))

# IMAGEM DE FUNDO
BG = pygame.transform.scale(pygame.image.load(os.path.join("imagens/background-black.jpeg")), (WIDTH, HEIGHT))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(pygame.transform.rotate(self.img, -90), (self.x, self.y))
    def move(self, vel):
        self.x -= vel
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 20
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(pygame.transform.rotate(self.ship_img, -90), (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 100, self.y + 45, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()

class Jogador(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = NAVE_JOGADOR
        self.laser_img = LASER_AZUL
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    #DEFINE A VIDA DO JOGADOR
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Inimigo(Ship):
    COLOR_MAP = {
                "vermelho": (NAVE_VERMELHA, LASER_VERMELHO),
                "verde": (NAVE_VERDE, LASER_VERDE),
                "azul": (NAVE_VERDE2, LASER_ROXO)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.x -= vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60

    level = 0
    vidas = 5
    score = 0

    RODANDO = 0
    pausado = 1

    jogo = RODANDO

    font = pygame.font. SysFont("Arial", 50)
    main_font = pygame.font.SysFont("Arial", 50)
    lost_font = pygame.font.SysFont("Arial", 60)
    font_pause = pygame.font.SysFont("Arial", 40)

    inimigos = []
    wave_length = 5
    inimigo_vel = 1

    jogador_vel = 5
    laser_vel = 5

    jogador = Jogador(100, 330)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))
        # desenha textos
        #vidas_label = main_font.render(f"Vidas: {vidas}", 1, (255,255,255))
        level_label = main_font.render(f"Nível: {level}", 1, (255,255,255))
        texto = font.render('Score: {0}'.format(score), True, (255,255,255))
        WIN.blit(texto, (10,10))

        highScore = 0

        with open("highscore.txt", "r") as highscore_file:
            highScore = highscore_file.readline()

            if(int(score) > int(highScore)):
                with open("highscore.txt", "w") as highscore_file:
                    highscore_file.write(str(score))

        highscore_label = font.render('Highscore: {0}'.format(highScore), True, (255,255,255))
        WIN.blit(highscore_label, (10,60))

        #WIN.blit(vidas_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for inimigo in inimigos:
            inimigo.draw(WIN)

        jogador.draw(WIN)

        if lost:
            lost_label = pygame.image.load(os.path.join("imagens/background-black.png"))
            lost_label = lost_font.render("GAME OVER!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            game_over.play()

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        #VIDAS
        if vidas <= 0 or jogador.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        #VIDAS

        if len(inimigos) == 0:
            level += 1
            wave_length += 3
            som_nivel.play()
            for i in range(wave_length):
                inimigo = Inimigo(random.randrange(1000, WIDTH), random.randrange(0, HEIGHT), random.choice(["vermelho", "azul", "verde"]))
                inimigos.append(inimigo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        #MOVIMENTAÇÃO DO JOGADOR
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] and jogador.x - jogador_vel > 0: # MOVE PARA ESQUERDA
            jogador.x -= jogador_vel

        if tecla[pygame.K_RIGHT] and jogador.x + jogador_vel + jogador.get_width() < WIDTH: # MOVE PARA DIREITA
            jogador.x += jogador_vel

        if tecla[pygame.K_UP] and jogador.y - jogador_vel > 0: # MOVE PARA CIMA
            jogador.y -= jogador_vel

        if tecla[pygame.K_DOWN] and jogador.y + jogador_vel + jogador.get_height() + 15 < HEIGHT: # MOVE PARA BAIXO
            jogador.y += jogador_vel

        if tecla[pygame.K_SPACE]:
            jogador.shoot()
            som_tiro.play()
                
        if tecla[pygame.K_p]:
            if jogo != pausado:
                #pygame.image.load(os.path.join("imagens/menu_ws.png"))
                pygame.mixer.music.pause()
                pause = font_pause.render("PAUSE", 1, (255,255,255))
                WIN.blit(pause, (600,400))
                jogo = pausado
            else:
                pygame.mixer.unpause()
                jogo = RODANDO

        if tecla[pygame.K_m]:
            pygame.mixer.pause()
            pause = font_pause.render("MUTE", 1, (255,255,255))
            WIN.blit(pause, (600,400))
        else:
            pygame.mixer.unpause()

        if jogo == RODANDO:
            score +=1

        if jogo == pausado:
            score +=0
            pygame.display.update()
            continue

        for inimigo in inimigos[:]:
            inimigo.move(inimigo_vel)
            inimigo.move_lasers(laser_vel, jogador)
            if random.randrange(0, 2*60) == 1:
                inimigo.shoot()
            if collide(inimigo, jogador):
                jogador.health -= 10
                inimigos.remove(inimigo)
                som_colisao.play()
            elif inimigo.y + inimigo.get_height() > HEIGHT:
                vidas -= 1
                inimigos.remove(inimigo)
        jogador.move_lasers(-laser_vel, inimigos)

        pygame.display.update()

def main_menu():
    #title_font = pygame.font.SysFont("Arial", 60)
    run = True
    while run:
        BG = pygame.transform.scale(pygame.image.load(os.path.join("imagens/menu_ws.png")), (WIDTH, HEIGHT))
        WIN.blit(BG, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                som_click.play()
                main()
    pygame.quit()


main_menu()