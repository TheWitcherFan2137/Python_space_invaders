import pygame
import random
import math
from pygame.locals import *


# Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SPEED = 5
SCORE = 0


# Initialize
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('background.png')
clock = pygame.time.Clock()

# Title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)



#========== Functions ==========#
def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def random_enemy_position(width):
    enemyX = random.randint (0, SCREEN_WIDTH - width)
    enemyY = random.randint (50, 150)
    return enemyX, enemyY

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + player_width / 2 - bullet_width / 2, y - bullet_height))

def isCollision (enemyX, enemyY, bulletX, bulletY):
    enemy_rect = pygame.Rect(enemyX, enemyY, enemy_width, enemy_height)
    bullet_rect = pygame.Rect(bulletX, bulletY, bullet_width, bullet_height)
    return enemy_rect.colliderect(bullet_rect)

#========= Entity data =========#
# Player
playerImg = pygame.image.load("player.png")
player_width, player_height = playerImg.get_size()

playerX = 370
playerY = 480
playerX_change = 0.0
playerSpeed = SPEED


# Enemy
enemyImg = pygame.image.load("enemy.png")
enemy_width, enemy_height = enemyImg.get_size()

random_enemy_position(enemy_width)
enemyX = random.randint (0, SCREEN_WIDTH - enemy_width)
enemyY = random.randint (50, 150)
enemyX_change = SPEED / 2
enemyY_change = SCREEN_HEIGHT // 15


# Bullet
bulletImg = pygame.image.load('bullet.png')
bullet_width, bullet_height = bulletImg.get_size()
bulletX = 0
bulletY = 480
bulletY_change = SPEED * 2
bullet_state = "ready"
# ready - You can't see the bullet on the screen
# fire - The bullet is currently moving



#========== Game loop ==========#
running = True
while running:

    # Screen display
    screen.blit(background, (0, 0))



    #========= Events ==========#
    for event in pygame.event.get():
        # Quiting
        if event.type == pygame.QUIT:
            running = False

    # Player moving
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] or keys[K_a]:
        playerX_change = -playerSpeed
    elif keys[K_RIGHT] or keys[K_d]:
        playerX_change = playerSpeed
    else:
        playerX_change = 0

    # Shoting
    if keys[K_SPACE]:
        if bullet_state == "ready":
            bulletX = playerX
            fire_bullet(bulletX, bulletY)
 
    # Player borders
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= SCREEN_WIDTH - player_width:
        playerX = SCREEN_WIDTH - player_width
    
    # Enemy moving
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = SPEED / 2
        enemyY += enemyY_change
    elif enemyX >= SCREEN_WIDTH - enemy_width:
        enemyX_change = -SPEED / 2
        enemyY += enemyY_change

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        SCORE += 1
        enemyX, enemyY = random_enemy_position(enemy_width)
        
    
    #==== Display on screen ====#
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
    clock.tick(FPS)