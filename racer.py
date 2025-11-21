import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

# ---------------------------
# Basic settings
# ---------------------------
FPS = 60
FramePerSec = pygame.time.Clock()

WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600

SPEED = 5            
SCORE = 0           
COINS = 0           
COINS_TO_SPEEDUP = 5 


font = pygame.font.SysFont("Arial", 60)
font_small = pygame.font.SysFont("Arial", 20)
game_over = font.render("Game Over", True, BLACK)


background = pygame.image.load("AnimatedStreet.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))


DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")



# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png").convert()
        self.image.set_colorkey(WHITE)                     # Remove white bg
        self.image = pygame.transform.scale(self.image, (80, 160))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)


# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png").convert()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (80, 160))
        self.rect = self.image.get_rect()
        self.reset_pos()

    def move(self):
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset_pos()

    def reset_pos(self):
        self.rect.center = (random.randint(70, SCREEN_WIDTH - 70), -160)

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coin.png").convert()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()

        self.value = 1 
        self.reset_pos()

    def move(self):
        
        self.rect.move_ip(0, SPEED)

      
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_pos()

    def reset_pos(self):
        
        self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), -50)

        self.value = random.choice([1, 3, 5])


player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group(player, enemy, coin)
enemies = pygame.sprite.Group(enemy)
coins_group = pygame.sprite.Group(coin)


INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Optional: speed increases every second
        if event.type == INC_SPEED:
            SPEED += 1

    
    DISPLAYSURF.blit(background, (0, 0))

    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    coins_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(coins_text, (300, 10))

    
    player.move()
    enemy.move()
    coin.move()

    # Draw sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)

    
    # Collision with Enemy
    if pygame.sprite.spritecollideany(player, enemies):
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()


    # Collision with Coin 
    if pygame.sprite.spritecollideany(player, coins_group):
        COINS += coin.value       
        SCORE += coin.value       
        coin.reset_pos()

        
        if COINS % COINS_TO_SPEEDUP == 0:
            SPEED += 1

    pygame.display.update()
    FramePerSec.tick(FPS)
