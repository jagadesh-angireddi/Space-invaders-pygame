import pygame
import os
import random
import math
from pygame import mixer

pygame.init()

#Game window
screen = pygame.display.set_mode((800,600))

#Background

background= pygame.image.load('background.png')

#background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(os.path.join('ufo.png'))
pygame.display.set_icon(icon)

#player
playerImg=pygame.image.load('player.png')
playerX= 370
playerY= 480
playerX_change=0

def player(x,y):
    screen.blit(playerImg,(x,y))

#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
enemies_no=6

for i in range(enemies_no):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))


#bullet
bulletImg=pygame.image.load('bullet.png')

bulletX = 0
bulletY = 480
bulletY_change = 15
bullet_state = 'ready'

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg,(x+16,y+10))

#collison function
def is_collison(enemyX,bulletX,enemyY,bulletY):
    distance= math.sqrt(math.pow((enemyX-bulletX),2)+math.pow((enemyY-bulletY),2))
    if distance < 27:
        return True
    else:
        False

score_value=0
font = pygame.font.Font('freesansbold.ttf',32)

over_font = pygame.font.Font('freesansbold.ttf',64)


    
textX=10
textY=10

def show_score(x,y):
    score=font.render("Score : " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over():
    over = over_font.render("Game Over",True,(255,255,255))
    screen.blit(over,(200,250))    



#event loop
running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        
        #keystroke for movement
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                playerX_change = -7
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
                   
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or  event.key == pygame.K_RIGHT:
                playerX_change = 0
                  
    #boundaries controlling 

    playerX += playerX_change
    if playerX <= 0:
        playerX=0
    elif playerX >= 736:
        playerX= 736 

    #enemy movement
    for i  in range(enemies_no):
        if enemyY[i]>420:
            for j in  range(enemies_no):
                enemyY[j]=2000
            game_over()
            break    
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i]=4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i]= -4
            enemyY[i] += enemyY_change[i] 

    #collision        
        collison=is_collison(enemyX[i],bulletX,enemyY[i],bulletY)
        if collison:
            explosin_sound= mixer.Sound('explosion.wav')
            explosin_sound.play()
            bullet_state = "ready"
            bulletY=480
            
            score_value +=1
        
            enemyX[i]= random.randint(0,735)
            enemyY[i]= random.randint(50, 150)
        
        enemy(enemyX[i],enemyY[i],i)    
    #bullet movement
    if bulletY <=0:
        bullet_state ="ready"
        bulletY= 480

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change 


               
    


    player(playerX,playerY)
    show_score(textX,textY)
    
    pygame.display.update()        


