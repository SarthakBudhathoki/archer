import pygame
import random
import math
import time
from pygame import mixer
# initialize pygame
pygame.init()
# Create the screen
screen = pygame.display.set_mode((1111,418))
# Create background
background = pygame.image.load('background2.png')
# Background sound
mixer.music.load('bg1.wav')
mixer.music.play(-1)
# title and icon
pygame.display.set_caption("BOMB ARCHER")
icon = pygame.image.load('archery(1).png')
pygame.display.set_icon(icon)
# Adding player
playerImg = pygame.image.load('archery(1).png')
playerX = 20
playerY = 142
playerY_change = 0
# Adding enemy
enemyImg = pygame.image.load('bomb.png')
enemyX = 1031
enemyY = random.randint(0,142)
# increase the speed based upon your needs

enemyY_change = 1

#Adding obstacles
obstacleImg = pygame.image.load('nuclear.png')
obstacleX = 500
obstacleY = 0
obstacleY_change = 2

# Adding arrow
bulletImg = pygame.image.load('right-arrow.png')
bulletX = 20
bulletY = 138
bulletX_change = 10
bulletY_change = 0

# Ready state - you can't see bullet on screen
# Fire state - bullet moving currently
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',68)

# x and y coordinate passed
def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))
def game_over_text():
    over_text = over_font.render(" GAME OVER ", True, (255,255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    #blit --> draw
    screen.blit(playerImg, (x,y))

def enemy(x,y):
    #blit --> draw
    screen.blit(enemyImg, (x,y))

def obstacle(x,y):
    #blit --> draw
    screen.blit(obstacleImg, (x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+10, y+0))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 40:
        return True
    else:
        return False

def wasCollision(obstacleX, obstacleY, bulletX, bulletY):
    distance = math.sqrt((math.pow(obstacleX-bulletX,2)) + (math.pow(obstacleY - bulletY,2)))
    if distance < 25:
        return True
    else:
        return False

# Game loop
running = True
while running:
    # RGB COLOR TO RGB for background color
    screen.fill((0, 110, 178))
    # background image makes speed slow--> needs to increase speed
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                # Increase to 0.3 if u want to increase the speed
                playerY_change = 2
            if event.key == pygame.K_UP:
                playerY_change = -2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('shoot.wav')
                    bullet_Sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletY = playerY

                    fire_bullet(bulletX,playerY)

        #to stop movement when the butoons are not pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
    #   Checking for boundaries of spaceship so it doesn't go out of boundary
    playerY += playerY_change

    # Creating boundaries
    if playerY <= 0:
        playerY = 0
    elif playerY >= 142:
        playerY = 142
    # Enemy movement
    enemyY += enemyY_change
    #Obstacle movement
    obstacleY += obstacleY_change
    if obstacleY >= 418:
        obstacleY = 0
    # Bullet movement
    if bulletX >=1111:
        bulletX = 20
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,playerY)
        bulletX += bulletX_change

        # Obstacle movement
        collision = isCollision(obstacleX, obstacleY, bulletX, bulletY)
        if collision:
            try:

                blast_Sound = mixer.Sound('nuke.wav')
                blast_Sound.play()
                game_over_text()

            finally:
                time.sleep(1)
                running = False


        # Collision
        collision = isCollision(enemyX, enemyY, bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('bomb.wav')
            explosion_Sound.play()
            # Reset the bullet
            bulletX = 20
            bullet_state = "ready"
            score_value += 1

            enemyX = random.randint(741,941)
            enemyY = random.randint(0, 142)

    # Creating boundaries
    if enemyY <= 0:
        enemyY_change = 1
        enemyY += enemyY_change
    elif enemyY >= 142:
        enemyY_change = -1
        enemyY += enemyY_change
    player(playerX, playerY)
    show_score(textX, textY)
    enemy(enemyX, enemyY)
    obstacle(obstacleX, obstacleY)
    pygame.display.update()