import pygame
from pygame.locals import *

# Zmienne
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLOR_BLACK = (0, 0, 0)
FPS = 60

#initialize
pygame.init()

# create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

#Title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0.0
playerSpeed = 5

def player(x, y):
    screen.blit(playerImg, (x, y))


#========== Game loop ==========#
running = True
while running:

    # Screen display
    screen.fill((COLOR_BLACK))

    # Quiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Moving
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                playerX_change = -playerSpeed
            if event.key == K_RIGHT:
                playerX_change = playerSpeed

        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                playerX_change = 0


    playerX += playerX_change    
    player(playerX, playerY)
    pygame.display.update()
    clock.tick(FPS)