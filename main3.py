import pygame
import random
import time
pygame.init()

from pygame import mixer
from bullet import Bullet
from player import Player
from Enemy import Enemy
from Explosion import Explosion

winW = 500
winH = 600

size=[winW, winH]
display = pygame.display.set_mode(size)

green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
laguna = (7, 235, 250)

#shoot_sound = pygame.mixer

bg_pic = pygame.image.load('assets/background_2.png')
bg_pic = pygame.transform.scale(bg_pic, (900, 600))

MAIN_MENU_STATUS = 'main_menu'
RUNNING_GAME_STATUS = 'running_game'
GAME_OVER_STATUS = 'game_over'

bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (bullet_img.get_width()//2,bullet_img.get_height()//2))
player_img = pygame.image.load('img/player.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (player_img.get_width()//2,player_img.get_height()//2))

meteor_img = []
explosion_img = []

m_list = [
    'meteor_5.png',
    'meteor_4.png',
    'meteor_3.png',
    'meteor_2.png',
    'meteor_1.png',
]

e_list = [
    '1.png',
    '2.png',
    '3.png',
    '4.png',
    '5.png',
    '6.png',
    '7.png',
    '8.png',
    '9.png'
]

for img in m_list:
    meteor_img.append(pygame.image.load('img/'+img).convert_alpha())

for img in e_list:
    explosion_img.append(pygame.image.load('img/' + img).convert_alpha())

mixer.music.load('sound/melod.ogg')
mixer.music.set_volume(1)
mixer.music.play(-1)



all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = []

player = Player(size, player_img)

for i in range(10):
    ind = random.randrange(0, len(meteor_img))
    enemy = Enemy(size, meteor_img[ind], ind+1)

    all_sprites.add(enemy)

    enemies.add(enemy)

all_sprites.add(player)

x = 300
y = 200
speed = 5
score = 0

game = True
game_status = MAIN_MENU_STATUS

clock = pygame.time.Clock()


def check_collision():

    for enemy in enemies:
        for bullet in bullets:
            if enemy.rect.colliderect(bullet):
                all_sprites.remove(bullet)
                bullets.remove(bullet)
                bullet.kill()
                global score
                enemy.hp =- 1
                if enemy.hp <= 0:
                    all_sprites.remove(enemy)

                    enemies.remove(enemy)

                    score += 10 * enemy.type
                    explosions.append(Explosion(enemy.rect.left, enemy.rect.top, 0, enemy.rect.width, enemy.rect.width))
                    prev_x = enemy.rect.x
                    prev_y = enemy.rect.y
                    prev_ind = enemy.type - 1
                    enemy.kill()

                    bullet_sound = mixer.Sound('assets/explosion.wav')
                    bullet_sound.play()

                    if prev_ind in [4, 3, 2]:

                        ind = random.randrange(0, len(meteor_img))
                        enemy = Enemy(size, meteor_img[ind], ind+1)
                        if len(enemies) < 10:
                            all_sprites.add(enemy)

                            enemies.add(enemy)
                    elif prev_ind == 1:
                        ind = 4
                        enemy = Enemy(size, meteor_img[ind], ind + 1, prev_x, prev_y)
                        all_sprites.add(enemy)
                        enemies.add(enemy)
                        enemy2 = Enemy(size, meteor_img[ind], ind + 1, prev_x, prev_y)
                        enemy2.speedx = -enemy.speedx
                        enemy2.speedy = -enemy.speedy
                        all_sprites.add(enemy2)
                        enemies.add(enemy2)
                    elif prev_ind == 0:
                        ind = 3
                        enemy = Enemy(size, meteor_img[ind], ind + 1, prev_x, prev_y)
                        all_sprites.add(enemy)
                        enemies.add(enemy)
                        enemy2 = Enemy(size, meteor_img[ind], ind + 1, prev_x, prev_y)
                        enemy2.speedx = -enemy.speedx
                        enemy2.speedy = -enemy.speedy
                        all_sprites.add(enemy2)
                        enemies.add(enemy2)

        if enemy.rect.colliderect(player):
            global game_status
            game_status = GAME_OVER_STATUS


while game:
    events = pygame.event.get()

    if game_status == MAIN_MENU_STATUS:

        for event in events:
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_status = RUNNING_GAME_STATUS

        display.blit(bg_pic, (0, 0))

        font = pygame.font.SysFont(None, 30)
        img = font.render('Нажмите [пробел] чтобы начать игру', True, (255, 255, 255))
        text_rect = img.get_rect(center=(winW / 2, winH * 0.3))
        display.blit(img, text_rect)


    elif game_status == RUNNING_GAME_STATUS:
        for event in events:
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(all_sprites, bullets, bullet_img)
                    bullet_sound = mixer.Sound('assets/laser.wav')
                    bullet_sound.play()

        display.blit(bg_pic, (0, 0))

        all_sprites.update(size)
        check_collision()
        #display.fill(white)

        all_sprites.draw(display)

        for explosion in explosions:
            explosion.draw(display, explosion_img)
            explosion.frame += 1

        i=0
        while i < len(explosions):
            if explosions[i].frame > len(explosion_img)-1:
                explosions.pop(i)
                i-=1
            i+=1

        font = pygame.font.SysFont(None, 30)
        img = font.render('{}'.format(score), True, (255, 255, 255))
        text_rect = img.get_rect(center=(winW / 2, winH * 0.05))
        display.blit(img, text_rect)

    elif game_status == GAME_OVER_STATUS:
        for event in events:
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_status = RUNNING_GAME_STATUS
                    all_sprites = pygame.sprite.Group()
                    enemies = pygame.sprite.Group()
                    bullets = pygame.sprite.Group()

                    player = Player(size, player_img )

                    for i in range(10):
                        ind = random.randrange(0, len(meteor_img))
                        enemy = Enemy(size, meteor_img[ind], ind+1)
                        all_sprites.add(enemy)

                        enemies.add(enemy)

                    all_sprites.add(player)
                    x = 300
                    y = 200
                    score = 0
        display.blit(bg_pic, (0, 0))



        all_sprites.draw(display)

        font = pygame.font.SysFont(None, 30)
        img = font.render('Игра окончена!', True, (255, 255, 255))
        text_rect = img.get_rect(center=(winW / 2, winH * 0.3))
        display.blit(img, text_rect)

        font = pygame.font.SysFont(None, 30)
        img = font.render('Ваш счёт: {}'.format(score), True, (255, 255, 255))
        text_rect = img.get_rect(center=(winW / 2, winH * 0.4))
        display.blit(img, text_rect)

        font = pygame.font.SysFont(None, 30)
        img = font.render('Нажмите [пробел] чтобы начать игру', True, (255, 255, 255))
        text_rect = img.get_rect(center=(winW / 2, winH * 0.5))
        display.blit(img, text_rect)



    pygame.display.update()


    clock.tick(30)