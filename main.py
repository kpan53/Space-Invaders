import pygame
import random
import math
from pygame import mixer


# Initialize all the functions for use
pygame.init()

#Create screen with Width: 800 Pixels, Height: 600 pixels (x-y axis starts at top left corner)
screen = pygame.display.set_mode((800, 600))

#Background
background = pygame.image.load('background.png')
#Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

def player(x,y):
    screen.blit(playerImg, (x, y)) #Draws the player

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):

    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y)) #Draws the enemy

#Bullet
bulletImg =pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready" #Ready - Can't see bullet yet -> Fire: The bullet is currently moving

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = over_font.render("Game Over !!!", True, (255,255,255))
    screen.blit(over_text, (200,250))

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16,y + 10))

def increase_enemies():
    global num_of_enemies
    num_of_enemies += 1

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop (Anything that needs to consistently update should be in here)
running = True
while running:
    # Red, Green, Blue
    screen.fill((0, 0, 0))
    #Background Image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print("Arrow has been pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -3 #Moving Left
                print ("Left Arrow Pressed")
            if event.key == pygame.K_RIGHT:
                print("Right Arrow Pressed")
                playerX_change = 3 #Moving Right
            if event.key == pygame.K_SPACE:
                if bullet_state =="ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX #Gets current x-coordinate of the ship, but then doesn't change its movement with the ship after
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("Arrow has been released")
                playerX_change = 0 #Stop Moving

    playerX += playerX_change
    #Sets Player Bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # Sets Enemy Bounds and Movement
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

            # Collision Detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY) # Gotta draw the player after you draw the background (done at the start)
    show_score(textX,textY)
    pygame.display.update()