# CS 269
# Chloe Zhang
# Starting screen

import pygame
from pygame import mixer
import os

# initialize pygame
pygame.init()
#load music
mixer.init()
mixer.music.load('../audios/BGM_start.mp3')
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Golf Simulator")
clock = pygame.time.Clock()

# game variables
FPS = 30
font = pygame.font.Font('freesansbold.ttf', 42)

# set RGB of colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG = (248, 249, 216)# background yellow

#read and transform images needed
start_ori = pygame.image.load(os.path.join('assets', 'startScreen.png'))
start_img = pygame.transform.scale(start_ori, (796,562))
ball_ori = pygame.image.load(os.path.join('assets', 'player1ball.png')).convert()
ball_img = pygame.transform.scale(ball_ori, (60,60))
ball_img.set_colorkey(BG)


def interface():
    #start music
    mixer.music.play()
    WIN.fill(BG)
    pygame.display.flip()
    pygame.time.wait(200)

    #displaying start image
    WIN.blit(start_img,(242,79))
    pygame.display.flip()
    pygame.time.wait(200)

    #fading out the start image
    fadeOut(1280, 720, BG)

    # blit the text onto the screen
    start_text = font.render('Click to Start', True, BLACK)
    WIN.blit(start_text, (540, 160))
    pygame.display.flip()

    #rotate and move ball image
    blitRotateBall(WIN, ball_img)

    #set up click to start game play and text disappearance
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            fadeOut(1280, 720, BLACK)

#fade out function used to fade out a selected area
def fadeOut(width, height, color):
    sur = pygame.Surface((width, height))
    sur.fill(color)
    for alpha in range (0, 300):
        sur.set_alpha(alpha)
        WIN.blit(sur, (0,0))
        pygame.display.flip()
        pygame.time.wait(90)

#rotate the ball and blit the img with its new position
def blitRotateBall(win, img):
    angle = 0
    loop = True
    while loop:
        angle += 6
        win.fill(BG)
        start_text = font.render('Click to Start', True, BLACK)
        WIN.blit(start_text, (540, 160))
        mx, my = pygame.mouse.get_pos()
        img_copy = pygame.transform.rotate(img, angle)
        img_copy.set_colorkey(BG)
        win.blit(img_copy, (mx - int(img.get_width() / 2), my - int(img.get_height() / 2)))
        pygame.display.flip()
        pygame.time.wait(50)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                loop = False


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        interface()
main()