import pygame
import os
import sys
import random
import time
from pygame.locals import *
 
pygame.init()
BASE_DIR = os.path.dirname(__file__)
FPS = 60
FramePerSeck = pygame.time.Clock()

RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)

SCREEN_WIDTH , SCREEN_HEIGHT = 400 , 600
SPEED = 5
SCORE = 0 
COINS = 0
LASTCOINS = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_coin = pygame.font.SysFont("comicsans", 20)
game_over = font.render("Game Over",True,BLACK)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer game")

background = pygame.image.load(os.path.join(BASE_DIR , "AnimatedStreet.png"))
coin_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Practice 11_get_coin.wav"))
crash_soud = pygame.mixer.Sound(os.path.join(BASE_DIR, "Practice 11_crash.wav"))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(os.path.join(BASE_DIR,"Enemy.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH - 40),0)
    
    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE +=1
            self.rect.top = 0
            self.rect.center = (random.randint(40,SCREEN_WIDTH -40),0)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(os.path.join(BASE_DIR, "Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (160,520)
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5,0)
class Coins(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
          
        drawing, value = self.get_random_drawing_and_value()

        self.image = pygame.image.load(os.path.join(BASE_DIR,drawing)).convert_alpha()
        self.value = value
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(self.rect.width // 2 , SCREEN_WIDTH - self.rect.width // 2), -50)
    def get_random_drawing_and_value(self):
        chance = random.random()
        
        if chance < 0.3:
            return "Coin3.png",3
        elif chance < 0.5:
            return "Coin2.png",2
        else:
            return "Coin1.png",1
    def move(self):
        self.rect.move_ip(0,5)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            spawn_new_coin()

def spawn_new_coin():
    new_coin = Coins()
    all_sprites.add(new_coin)
    coins.add(new_coin)
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)


for i in range(3):
    C1 = Coins()
    all_sprites.add(C1)
    coins.add(C1)

ENC_SPEED = pygame.USEREVENT +1
pygame.time.set_timer(ENC_SPEED,1000)

while True:
    for event in pygame.event.get():
        if event.type == ENC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background,(0,0))
    scores = font_small.render(str(SCORE),True,BLACK)
    DISPLAYSURF.blit(scores,(10,10))
    amount_coins = font_coin.render(f"Coins: {COINS}",True,BLACK)
    DISPLAYSURF.blit(amount_coins,(305,10))
    
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image,entity.rect)

    if pygame.sprite.spritecollideany(P1,enemies):
        crash_soud.play()
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over,(30,250))
        pygame.display.update()

        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()
    collected_coins = pygame.sprite.spritecollide(P1,coins,True)  
    for coin in collected_coins:
        coin_sound.play()
        COINS += coin.value
        spawn_new_coin()
        if COINS - LASTCOINS >=15:
            SPEED +=1
            LASTCOINS = COINS
    pygame.display.update()
    FramePerSeck.tick(FPS)