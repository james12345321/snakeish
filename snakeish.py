import random
import pygame
import numpy as np
import operator
import time
import sys

GREEN, BLACK, RED, WHITE = (0, 255, 0), (0, 0, 0), (255, 0, 0), (255, 255, 255)

pygame.init()
clock = pygame.time.Clock()
titlefont = pygame.font.SysFont(None, 100)
smallfont = pygame.font.SysFont(None, 50)
screen = pygame.display.set_mode((800, 800), pygame.NOFRAME)
pygame.display.set_caption("game")
score=1

block1image=pygame.image.load('snakehead1.png').convert_alpha()
block1=block1image.get_rect()
block1.center=(120, 120)

matrix = np.array([[80, 80]])
tobeadded = np.array([[0, 0]])

def movement(key, pixel, xory, op):
    if event.type == pygame.KEYDOWN:    
        if event.key == key:
            try:
                if screen.get_at(pixel) != GREEN:
                    if key == pygame.K_LEFT or key == pygame.K_RIGHT:
                        block1.x = op(xory, 80)
                    if key == pygame.K_UP or key == pygame.K_DOWN:
                        block1.y = op(xory, 80)
                    global waiting
                    waiting = True
            except IndexError:
                pass

def generateApple(num1, num2):
    global apple
    apple = pygame.Rect((num1*(80)+20), (num2*(80)+20), 40, 40)

def drawApple():  
    generateApple(random.randint(0, 9), random.randint(0, 9))
    global appleLocation
    appleLocation=[apple.x-20, apple.y-20]
    for row in matrix:
        if np.array_equal(row, appleLocation):
            global getNewApple
            getNewApple=True
            return        
    pygame.draw.rect(screen, RED, apple)
    pygame.display.flip()
    getNewApple=False

drawApple()
screen.blit(block1image, block1)
pygame.display.flip()

startTimer=True
running = True
listening=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        waiting = False
        if listening:
            movement(pygame.K_LEFT, (block1.x-80, block1.y), block1.x, operator.sub)
        if listening:
            movement(pygame.K_RIGHT, (block1.x+80, block1.y), block1.x, operator.add)
        if listening:
            movement(pygame.K_UP, (block1.x, block1.y-80), block1.y, operator.sub)
        if listening:
            movement(pygame.K_DOWN, (block1.x, block1.y+80), block1.y, operator.add)
        
        while startTimer:
            global timestart
            timestart=time.perf_counter()
            startTimer=False
        
        if appleLocation[0] == (matrix[-1][-2]) and appleLocation[1] == (matrix[-1][-1]) and listening:
            score=score+1
            print(f'score is {score-1}')
            getNewApple=True
            while getNewApple:
                drawApple()

        if len(matrix) > score and listening:
            pygame.draw.rect(screen, BLACK, (matrix[0][0], matrix[0][1], 80, 80))
            matrix = np.delete(matrix, 0, axis=0)
        
        if waiting and listening:
            tobeadded[0, 0] = block1.x
            tobeadded[0, 1] = block1.y
            matrix = np.concatenate((matrix, tobeadded), axis=0)
            screen.blit(block1image, block1) #make the head rotate according to which direction its facing
            pygame.draw.rect(screen, GREEN, (matrix[-2][-2], matrix [-2, -1], 80, 80))
            pygame.display.flip()
        
        if score>10:
            if listening:
                timeend=time.perf_counter()
            listening=False
            elapsedTime=timeend-timestart
            try:
                with open('highscore.txt', 'r+') as highwrite:
                    highscorenum=float(highwrite.read())
                    if elapsedTime<highscorenum:
                        highwrite.seek(0)
                        highwrite.truncate(0)
                        highwrite.write(str(round(elapsedTime, 5)))
                        highwrite.close()
                    else:
                        highwrite.close()
                if elapsedTime<highscorenum:
                    with open('highscore.txt', 'r') as highread:
                        highscorenum=str(highread.read())
                        highread.close()
            except FileNotFoundError:
                highscore=smallfont.render('missing highscore.txt file!')
            gameover = titlefont.render('GAME OVER', True, RED)
            text = smallfont.render(f'time took: {round(elapsedTime, 5)} seconds', True, WHITE)
            highscore = smallfont.render(f'your high score is {highscorenum} seconds', True, WHITE)
            moretext = smallfont.render('press space to quit, enter to restart', True, WHITE)
            screen.fill(BLACK)
            screen.blit(gameover, (10, 10))
            screen.blit(text, (10, 100))
            screen.blit(highscore, (10, 150))
            screen.blit(moretext, (10, 200))

            pygame.display.flip()
            getInfo=True
            while getInfo:
                for e in pygame.event.get():
                    if e.type==pygame.KEYDOWN:
                        if e.key==pygame.K_SPACE:
                            sys.exit()
                        if e.key==pygame.K_RETURN:
                            screen.fill(BLACK)
                            listening=True
                            score=1
                            block1=block1image.get_rect()
                            block1.center=(120, 120)
                            matrix = np.array([[80, 80]])
                            tobeadded = np.array([[0, 0]])
                            drawApple()
                            screen.blit(block1image, block1)
                            pygame.display.flip()
                            startTimer=True
                            getInfo=False
    clock.tick(240)
pygame.quit()
