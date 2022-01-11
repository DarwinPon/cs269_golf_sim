#Yiheng Su
#Jan, 10, 2022

####################### Setup #########################
# useful imports
import sys
import random

# import pygame
import pygame

# initialize pygame
pygame.init()

# Frames per second
FPS = 30

# set RGB of colors
WHITE = (255, 255, 255)

# game events
GOAL = pygame.USEREVENT + 1

# initialize the fonts
try:
    pygame.font.init()
except:
    print("Fonts unavailable")
    sys.exit()

# create a game clock
gameClock = pygame.time.Clock()

# create a screen and set its width and height
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )


# create caption for the screen
pygame.display.set_caption("Golf")

####################### Making Content #########################

# load some images
# set the size of the image
BALL_WIDTH, BALL_HEIGHT = 30, 30
GOAL_WIDTH, GOAL_HEIGHT = 90, 90
ball = pygame.image.load( "ball.png" ).convert_alpha() # put the name of ball image here
ball = pygame.transform.scale(ball, (BALL_WIDTH, BALL_HEIGHT)) # scale an image
goal = pygame.image.load( "ball.png" ).convert_alpha() # put the name of ball image here
goal = pygame.transform.scale(ball, (GOAL_WIDTH, GOAL_HEIGHT)) # scale an image

# create a font
afont = pygame.font.SysFont( "Helvetica", 32, bold=True )
# render a surface with some text
text = afont.render( "Clean up time", True, (0, 0, 0) )

####################### Filling the Screen #########################
def draw_window(ballRect, goalRect):
    # clear the screen with white
    screen.fill(WHITE)

    # now draw the surfaces to the screen using the blit function
    screen.blit( ball, (ballRect.x, ballRect.y) )

    # update the screen
    pygame.display.update()

####################### Add Movement #########################
def ballRect_movement(key_pressed, ballRect):
    """Implement ball movement"""

def handle_collision(ballRect, goalRect):
    """If collide, add GOAL to the event list"""
    if ballRect.colliderect(goalRect):
        print("Collision!")
        pygame.event.post(pygame.event.Event(GOAL))

def handle_startScreen():
    """Implement start screen"""

def apply_launch_force(key_pressed, ball, force_scale):
    """Decides the force applied to the ball based on user input"""

    #scale up by 1 if current scale is less than 10
    if key_pressed[pygame.K_UP] and force_scale < 10:
        return force_scale + 1
    #scale down by 1 if current scale is larger than 0
    elif key_pressed[pygame.K_DOWN] and force_scale > 0:
        return force_scale - 1
    else:
        return force_scale


def handle_gameover():
    """Implement gameover screen"""
    handle_endScreen()

def handle_endScreen():
    """Implement end screen"""

def check_button_clicked(button) -> bool:
    """Check if player click the button"""
    mousePos = pygame.mouse.get_pos()
    if button.left < mousePos[0] < button.right and button.top < mousePos[1] < button.bottom:
        return True
    else:
        return False

####################### Main Event Loop #########################
# go into a holding pattern until someone clicks a mouse or hits a key

def main():
    ballRect = pygame.Rect((100, 200), (BALL_WIDTH, BALL_HEIGHT)) # put the initial position of the ball into bracket
    goalRect = pygame.Rect((400, 200), (GOAL_WIDTH, GOAL_HEIGHT)) # put the initial position of the goal into bracket

    # show the start screen
    handle_startScreen()

    print("Entering main loop")
    while True:
        # Check every event in the event list
        for event in pygame.event.get():
            # click quit button, then quit
            if event.type == pygame.QUIT:
                sys.exit()

            # if one player goal, then go to the gameover event
            if event.type == GOAL:
                handle_gameover()

        key_pressed = pygame.key.get_pressed()

        # move ball according to the rule
        ballRect_movement(key_pressed, ballRect)

        # move to gameover screen when collided
        handle_collision(goalRect, ballRect)

        # update the screen
        draw_window(ballRect, goalRect)

        # set FPS
        gameClock.tick(FPS)

if __name__ == "__main__":
    main()
