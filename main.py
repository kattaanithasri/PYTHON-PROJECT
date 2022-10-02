import pygame
import random
import math
from pygame import mixer

#initialization
pygame.init()
#create the screen
screen = pygame.display.set_mode((800,600))
#sound
mixer.music.load("bg_music_1.mp3")
mixer.music.play(-1)


#background
background = pygame.image.load('background.jpg')
#caption and logo
pygame.display.set_caption("saving chicken")
icon = pygame.image.load('tambourinenew.png')
pygame.display.set_icon(icon)
#player
playerImg = pygame.image.load('hennew1.png')
playerX = 370
playerY = 480
playerX_change = 0


#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change=[]
enemyY_change=[]
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('OEMBXF0new.jpg'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)



#Bullet
#ready -you can't see the bullet on screen
#fire- the bullet is currently moving

bulletImg = pygame.image.load('v789new.jpg')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


#Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x,y):
    score = font.render("Score:" +str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))






def player(x,y):
    screen.blit(playerImg, (x,y))

def bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x,y))




def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


#Game loop
running = True
while running:
    #RGB is Red,Blue,Green
    screen.fill((255,255,255))
    screen.blit(background,(0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #when we close button
            running = False

        if event.type == pygame.KEYDOWN:
            #keydown means pressing key
            if event.key == pygame.K_LEFT:
               playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("explosion.wav")
                    bulletSound.play()
                    #get the current x coordinate of the spaceship
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               playerX_change = 0



    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    #enemy movement
    for i in range(num_of_enemies):
         #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i]  <= 0:
            enemyX_change[i]  = 0.5
            enemyY[i]  += enemyY_change[i]
        elif enemyX[i]  >= 736:
            enemyX_change[i]  = -0.5
            enemyY[i]  += enemyY_change[i]

         # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("laser.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
 #bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"




    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change








    player(playerX, playerY)

    show_score(textX, textY)
    pygame.display.update()