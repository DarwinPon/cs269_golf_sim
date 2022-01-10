# Bruce A. Maxwell
# January 2015
#
# Pygame Tutorial Example 1
#
# Creates a static scene and then waits for an event to quit
#

####################### Setup #########################
# useful imports
import sys
import random

# import pygame
import pygame
from pygame import key
from pygame import sprite
from pygame import mouse
from pygame.display import set_caption

# initialize pygame
pygame.init()

FPS = 30
VEL = 5 # velocity

# game state
CLEAR = pygame.USEREVENT + 1

# initialize the fonts
try:
    pygame.font.init()
except:
    print("Fonts unavailable")
    sys.exit()

# create a game clock
gameClock = pygame.time.Clock()

# create a screen (width, height)
screen = pygame.display.set_mode( (640, 480) )

# create caption for the screen
pygame.display.set_caption("First game!")

####################### Making Content #########################

OBJECT_WIDTH, OBJECT_HEIGHT = 80, 80
# load some images
spider = pygame.image.load( "Spider.png" ).convert_alpha()
spider = pygame.transform.scale(spider, (OBJECT_WIDTH, OBJECT_HEIGHT)) # scale an image
# spider = pygame.transform.rotate(spider, 90) # rotate an image 
broom = pygame.image.load( "Broom.png" ).convert_alpha()
broom = pygame.transform.scale(broom, (OBJECT_WIDTH, OBJECT_HEIGHT))

# create a font
afont = pygame.font.SysFont( "Helvetica", 32, bold=True )

# render a surface with some text
text = afont.render( "Clean up time", True, (0, 0, 0) )

####################### Filling the Screen #########################
def draw_window(spiderRec, broomRec):
    # clear the screen with white
    screen.fill( (255, 255, 255) )

    # # draw a rectangle behind the text
    # pygame.draw.rect( screen, (70, 210, 80), pygame.Rect( (180, 80), (280, 80) ) )
    # # blit the text surface onto the screen
    # screen.blit( text, (220, 100) )

    # now draw the surfaces to the screen using the blit function
    screen.blit( spider, (spiderRec.x, spiderRec.y) )
    screen.blit( broom, (broomRec.x, broomRec.y) )

    # update the screen
    pygame.display.update()

####################### Add Movement #########################
def spiderRect_movement(spiderRect):
    moveDirection = random.randint(1,4)
    moveDistance = random.randint(3, 10)
    if moveDirection == 1 and spiderRect.x - moveDirection > 0:
        spiderRect.x -= moveDistance
    elif moveDirection == 2 and spiderRect.x + moveDirection < 640 - OBJECT_WIDTH:
        spiderRect.x += moveDistance
    elif moveDirection == 3 and spiderRect.y - moveDirection > 0:
        spiderRect.y -= moveDistance
    elif moveDirection == 4 and spiderRect.y + moveDirection < 480 - OBJECT_HEIGHT:
        spiderRect.y += moveDistance


def broomRect_movement(key_pressed, broomRect, xvel, yvel):
    if broomRect.x - xvel <= 0 or broomRect.x + xvel >= 640 - OBJECT_WIDTH:
        xvel = -xvel
    if broomRect.y - yvel <= 0 or broomRect.y + yvel >= 480 - OBJECT_HEIGHT:
        yvel = -yvel

    broomRect.x += xvel
    broomRect.y += yvel
    return xvel - 0.04, yvel-0.03
    # if key_pressed[pygame.K_a] and broomRect.x - VEL > 0:
    #     broomRect.x += xvel
    #     broomRect.y += yvel
    # if key_pressed[pygame.K_d] and broomRect.x + VEL < 640 - OBJECT_WIDTH:
    #     broomRect.x += VEL
    # if key_pressed[pygame.K_w] and broomRect.y - VEL > 0:
    #     broomRect.y -= VEL
    # if key_pressed[pygame.K_s] and broomRect.y + VEL < 480 - OBJECT_HEIGHT:
    #     broomRect.y += VEL

def handle_collision(broomRect, spiderRect):
    if broomRect.colliderect(spiderRect):
        print("Collision!")
        pygame.event.post(pygame.event.Event(CLEAR))

def handle_gameover():
    print("Entering gameover screen")
    gameover_text = afont.render( "You clean up the bug!", True, (0, 0, 0) )
    # blit the text surface onto the screen
    screen.blit( gameover_text, (150, 100) )
    pygame.display.update()
    pygame.time.wait(2000)
    handle_endScreen()

def check_button_clicked(button) -> bool:
    mousePos = pygame.mouse.get_pos()
    if button.left < mousePos[0] < button.right and button.top < mousePos[1] < button.bottom:
        return True
    else:
        return False
    
def handle_endScreen():
    screen.fill( (255, 255, 255) )
    playagain_text = afont.render("Play again!", True, (0, 0, 0))
    button = pygame.Rect( (180, 80), (280, 80) )
    pygame.draw.rect( screen, (70, 210, 80), button )
    screen.blit( playagain_text, (230, 100) )
    pygame.display.update()

    print("Entering end screen")
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_button_clicked(button):
                    pygame.event.clear()
                    main()


####################### Main Event Loop #########################
# go into a holding pattern until someone clicks a mouse or hits a key

def main():
    spiderRect = pygame.Rect((100, 200), (OBJECT_WIDTH, OBJECT_HEIGHT))
    broomRect = pygame.Rect((400, 200), (OBJECT_WIDTH, OBJECT_HEIGHT))

    xvel = 0.8 * 5
    yvel = 0.6 * 5

    # pygame.event.post(pygame.event.Event(CLEAR))


    print("Entering main loop")
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == CLEAR:
                handle_gameover()

        key_pressed = pygame.key.get_pressed()
        # move spider automatically
        spiderRect_movement(spiderRect)
        # move broom according to the key pressed
        xvel, yvel = broomRect_movement(key_pressed, broomRect, xvel, yvel)
        # move to gameover screen when collided
        handle_collision(broomRect, spiderRect)

        draw_window(spiderRect, broomRect)
        gameClock.tick(FPS)

if __name__ == "__main__":
    main()
