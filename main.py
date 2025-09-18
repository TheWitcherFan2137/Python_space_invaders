import pygame
import random
import math
from pygame.locals import *
from pygame import mixer


# Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLOR_WHITE = (255, 255, 255)
FPS = 60
SPEED = 5


# Initialize
pygame.init()
clock = pygame.time.Clock()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('background.png')

# Sounds
mixer.music.load('background.wav')
mixer.music.play(-1)
bullet_sound = mixer.Sound('laser.wav')
explosion_sound = mixer.Sound('explosion.wav')


# Title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)



#========== Functions ==========#
def draw_player(x, y):
        screen.blit(player_img, (x, y))

def random_enemy_position(width):
    x = random.randint (0, SCREEN_WIDTH - width)
    y = random.randint (50, 150)
    return x, y

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + player_width / 2 - bullet_width / 2, y - bullet_height))

def is_collision (enemy_x, enemy_y, bullet_x, bullet_y, enemy_width, enemy_height):
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
    return enemy_rect.colliderect(bullet_rect)

def show_score(x, y):
    score_text = font.render("Score : " + str(score_value), True, COLOR_WHITE)
    screen.blit(score_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, COLOR_WHITE)
    tx = (SCREEN_WIDTH - over_text.get_width()) // 2
    ty = (SCREEN_HEIGHT - over_text.get_height()) // 2
    screen.blit(over_text, (tx, ty))

    



#========= Entity data =========#
# Player
player_img = pygame.image.load("player.png")
player_width, player_height = player_img.get_size()

player_x = 370
player_y = 480
player_x_change = 0.0
player_speed = SPEED


# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemy_width, enemy_height = enemy_img[i].get_size()
    x, y = random_enemy_position(enemy_width)
    enemy_x.append(x)
    enemy_y.append(y)
    enemy_x_change.append(SPEED / 2)
    enemy_y_change.append(SCREEN_HEIGHT // 15)


# Bullet
bullet_img = pygame.image.load('bullet.png')
bullet_width, bullet_height = bullet_img.get_size()
bullet_x = 0
bullet_y = 480
bullet_y_change = SPEED * 2
bullet_state = "ready"
# ready - You can't see the bullet on the screen
# fire - The bullet is currently moving


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
GAME_OVER = False



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
        player_x_change = -player_speed
    elif keys[K_RIGHT] or keys[K_d]:
        player_x_change = player_speed
    else:
        player_x_change = 0

    # Shoting
    if not GAME_OVER and keys[K_SPACE]:
        if bullet_state == "ready":
            bullet_sound.play()
            bullet_x = player_x
            fire_bullet(bullet_x, bullet_y)
 
    # Player borders
    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= SCREEN_WIDTH - player_width:
        player_x = SCREEN_WIDTH - player_width
    
    # Update enemies, bullets and collisions
    if not GAME_OVER:
        for i in range(num_of_enemies):
            ew, eh = enemy_img[i].get_size() 

            # Game over
            if enemy_y[i] + eh >= player_y:
                GAME_OVER = True
                mixer.music.stop()
                break

            enemy_x[i] += enemy_x_change[i]

            #boundaries per enemy width
            if enemy_x[i] <= 0:
                enemy_x_change[i] = SPEED / 2
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= SCREEN_WIDTH - enemy_width:
                enemy_x_change[i] = -SPEED / 2
                enemy_y[i] += enemy_y_change[i]

        # Bullet movement
        if bullet_state == "fire":
            bullet_y -= bullet_y_change
            screen.blit(bullet_img, (bullet_x, bullet_y))

            if bullet_y <= 0:
                bullet_y = player_y
                bullet_state = "ready"

        # Collision
        for i in range(num_of_enemies):
            ew, eh = enemy_img[i].get_size()
            collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y, ew, eh)
            if bullet_state == "fire" and collision:
                explosion_sound.play()
                bullet_y = player_y
                bullet_state = "ready"
                score_value += 1
                enemy_x[i], enemy_y[i] = random_enemy_position(ew)
        
    
    #==== Display on screen ====#
    draw_player(player_x, player_y)
    
    for i in range(num_of_enemies):
        screen.blit(enemy_img[i], (enemy_x[i], enemy_y[i]))
    
    show_score(textX, textY)

    if GAME_OVER:
        bullet_state = "ready"
        game_over_text()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()