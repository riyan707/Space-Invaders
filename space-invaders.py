#Setup Python --------------------------------------------------#
import pygame, sys
import random
import math
from pygame import mixer

#Constants -----------------------------------------------------#
WIDTH, HEIGHT = (800,600)
WHITE = (255,255,255)
BLACK = (0,0,0)

#Setup pygame/window -------------------------------------------#
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Space-Invaders')
icon = pygame.image.load(r'C:\Users\riyan\Documents\Code\home\python\python projects\Games\space invaders\spaceship.png')
pygame.display.set_icon(icon)
#screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Player --------------------------------------------------------#
playerImg = pygame.image.load(r'C:\Users\riyan\Documents\Code\home\python\python projects\Games\space invaders\player.png')
playerImg = pygame.transform.scale(playerImg, (65,65))
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

def player(x,y):
    screen.blit(playerImg, (x,y))

#Enemy --------------------------------------------------------#
enemyImg = []
enemyX = []
enemyY = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(r'C:\Users\riyan\Documents\Code\home\python\python projects\Games\space invaders\enemyy.png'))
    #enemyImg.append(pygame.transform.scale(enemyImg, (40,40)))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1.5)
    enemyY_change.append(40)

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

#Lazer ---------------------------------------------------------#
lazerImg = pygame.image.load(r'C:\Users\riyan\Documents\Code\home\python\python projects\Games\space invaders\lazer.png')
lazerImg = pygame.transform.scale(lazerImg, (20,20))
lazerX = 0
lazerY = 480
lazerX_change = 0
lazerY_change = 10
lazer_state = "ready"

def fire_lazer(x,y):
    global lazer_state
    lazer_state = "fire"
    screen.blit(lazerImg, (x+22,y+10))

#Enemy Killed by Lazer------------------------------------------#
def isCollision(enemyX,enemyY,lazerX,lazerY):
    distance = math.sqrt((math.pow(enemyX-lazerX,2)) + (math.pow(enemyY-lazerY,2)))
    if distance < 27:
        return True
    else:
        return False

#Score ---------------------------------------------------------#
score_value = 0
font = pygame.font.Font('freesansbold.ttf',14)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (WHITE))
    screen.blit(score, (x,y))

#Game over
score_value = 0
over_font = pygame.font.Font('freesansbold.ttf',74)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (WHITE))
    screen.blit(over_text, (200,250))

#you win
score_value = 0
win_font = pygame.font.Font('freesansbold.ttf',74)


def you_win_text():
    win_text = win_font.render("YOU WIN", True, (WHITE))
    screen.blit(win_text, (200,250))


#Loop ----------------------------------------------------------#
while True:

    #Background ------------------------------------------------#
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BLACK)

    #Load Player -----------------------------------------------#
    player(playerX,playerY)
    playerX += playerX_change


    #Buttons ---------------------------------------------------#
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        #Player Movement ---------------------------------------#
         #win
        if score_value >= 6:
            you_win_text()


        for i in range(num_of_enemies):
            enemyX[i] += enemyX_change[i]

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_a: #left
                playerX_change = -3
            if event.key == pygame.K_d: #right
                playerX_change = 3

        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_a: #left
                playerX_change = -0
            if event.key == pygame.K_d: #right
                playerX_change = 0 

        #Firing -----------------------------------------------#
        key = pygame.key.get_pressed() 
        if key[pygame.K_SPACE]: #fire
            if lazer_state is "ready":
                lazer_sound = mixer.Sound(r'C:\Users\riyan\Documents\Code\home\python\python projects\Games\space invaders\beam.wav')
                lazer_sound.play()
                lazerX = playerX
                fire_lazer(playerX,lazerY)

        if lazerY <= 0:
            lazerY = 480
            lazer_state = "ready"     

        if lazer_state is "fire":
            fire_lazer(lazerX,lazerY)
            lazerY -= lazerY_change

        #Colllison Logic -------------------------------------#
        #Game Border -----------------------------------------#
        if playerX <= 0:
            playerX = 0
        elif playerX >= 735:
            playerX = 735

        for i in range(num_of_enemies): 
            #game over  
            if enemyY[i] > 200 :
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            if enemyX[i] < 0:
                enemyX_change[i] = 1.5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] > 760:
                enemyX_change[i] = -1.5
                enemyY[i] += enemyY_change[i]

            #Enemy Collision --------------------------------#
            collision = isCollision(enemyX[i],enemyY[i],lazerX,lazerY)
            if collision:
                lazerY = 480
                lazer_state = "ready"
                num_of_enemies -= 1
                score_value += 1
                enemyX[i] = random.randint(0,735)
                enemyY[i] = random.randint(50,150)
            
            #Load Enemy --------------------------------------#
            enemy(enemyX[i],enemyY[i], i)


        
          
    #Update ---------------------------------------------------#
    show_score(textX,textY)
    pygame.display.update()
    mainClock.tick(60)




