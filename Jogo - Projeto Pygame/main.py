import random
from pyclbr import readmodule_ex
import pygame
import random

pygame.font.init()
pygame.init()

x=1280
y=780

#IMAGENS
screen=pygame.display.set_mode((x,y))
pygame.display.set_caption('Wing Shot')

bg=pygame.image.load('city.png').convert_alpha()
bg=pygame.transform.scale(bg, (x,y))

alien=pygame.image.load('alien.png').convert_alpha()
alien=pygame.transform.scale(alien, (50,50))

airplane=pygame.image.load('airplane.png').convert_alpha()
airplane=pygame.transform.scale(airplane,(130,130))
airplane=pygame.transform.rotate(airplane, -90)

tiro = pygame.image.load('tiro.png').convert_alpha()
tiro = pygame.transform.scale(tiro,(120,60))
tiro = pygame.transform.rotate(tiro, -90)

#POSIÇÕES IMAGENS
position_alien_x=400
position_alien_y=200

position_airplane_x=10
position_airplane_y=10

speed_tiro_x = 0
position_tiro_x = 10
position_tiro_y = 10

triggered = False
running=True

#FUNÇÕES
def respawn_tiro():
    triggered = False
    respawn_tiro_x = position_airplane_x
    respawn_tiro_y = position_airplane_y
    speed_x_tiro = 0
    return [respawn_tiro_x, respawn_tiro_y, triggered, speed_x_tiro]
    
def respawn():
    alienx=random.randint(200, 400)
    alieny=random.randint(0, 600)
    return [alienx, alieny]
direcao = ''
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    screen.blit(bg, (0,0))

    rel_x=x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width,0)) #CRIA IMAGEM DE FUNDO
    if rel_x < 1280:
        screen.blit(bg, (rel_x, 0))


    #BOTÕES
    botao=pygame.key.get_pressed()
    if botao[pygame.K_UP] and position_airplane_y > 1:
        position_airplane_y -=1
        if not triggered:
            position_tiro_y -=1

    if botao[pygame.K_DOWN] and position_airplane_y < 665:
        position_airplane_y +=1

        if not triggered:
            position_tiro_y +=1

    if botao[pygame.K_SPACE]:
        triggered = True
        speed_tiro_x = 2

    # #RENASCER (RESPAWN)
    # if position_alien_y>=400 or position_alien_x <= 400:
    #     position_alien_x=respawn()[0]
    #     position_alien_y=respawn()[1]



    #MOVIMENTAÇÃO
    x-=1
    
    position_tiro_x += speed_tiro_x

    if position_tiro_x == 1200:
        position_tiro_x, position_tiro_y, triggered, speed_tiro_x = respawn_tiro()

    position_alien_x +=1

    if position_alien_x == 1200:
        position_alien_x=respawn()[0]
        position_alien_y=respawn()[1]

    if position_alien_y > 400:
        
        direcao = 'down'
    elif position_alien_y < 50:
        
        direcao = 'up'

    if direcao == 'up':
        position_alien_y +=1
    else: 
        position_alien_y -=1

    #CRIAÇÃO DE IMAGENS
    screen.blit(alien, (position_alien_x, position_alien_y))
    screen.blit(tiro, (position_tiro_x,position_tiro_y))
    screen.blit(airplane, (position_airplane_x, position_airplane_y))


    pygame.display.update()

