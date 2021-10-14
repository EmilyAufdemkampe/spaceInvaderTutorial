import random
import math
import pygame
from pygame import mixer

# Initialise pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Set Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Shows score
def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Shows Game Over
def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Draws Player to screen
def player(x, y):
    screen.blit(playerImg, (x, y))

# Draws Enemy to screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Draws laser to screen
def fire_laser(x, y):
    global laser_ready
    laser_ready = False
    screen.blit(laserImg, (x + 16, y + 10))

# Calculate distance between enemy and laser
def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.hypot(enemyX - laserX, enemyY - laserY)
    if distance < 27:
        return True
    else:
        return False

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Laser
laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 480
laserY_change = 10
laser_ready = True

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
game_over = False
over_font = pygame.font.Font('freesansbold.ttf', 64)
restart_font = pygame.font.Font('freesansbold.ttf', 20)

# Game Loop
running = True

while running:

    # Screen RGB
    screen.fill((0,0,0))
    # Background images
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        # Closes Window when Quit is pressed
        if event.type == pygame.QUIT:
            running = False

        # Checks if keystroke is right or left
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT: 
                playerX_change = -4

            if event.key == pygame.K_RIGHT:
                playerX_change = 4

            if event.key == pygame.K_SPACE:
                if laser_ready:
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()
                    laserX = playerX
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Sets playerX boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over_text()
            game_over = True
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            explosion_sound = mixer.Sound('splatter.wav')
            explosion_sound.play()
            laserY = 480
            laser_ready = True
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)

    # Laser movement
    if laserY <= 0:
        laserY = 480
        laser_ready = True

    if not laser_ready:
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    player(playerX, playerY)
    show_score(textX, textY)
    
    pygame.display.update()