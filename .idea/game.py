#Yiheng Su
#Jan, 10, 2022

####################### Setup #########################
# useful imports
import sys
import random
import math

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
PLAYER1TURN = pygame.USEREVENT + 1

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
BALL_WIDTH, BALL_HEIGHT = 80, 80 
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
def ballRect_movement(ballRect):
    """Implement ball movement"""
    angleInDegree = 0
    angularVel = 10
    player1trun = True

    while player1trun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    angleInDegree -= angularVel
      
                if event.key == pygame.K_d:
                    angleInDegree += angularVel
                
                if event.key == pygame.K_SPACE:
                    angleInRadian = angleInDegree * (math.pi / 180)
                    velocity = 30 # initial velocity is hard coded for now

                    # move some distance
                    while velocity != 0:
                        velocity_x = velocity * math.cos(angleInRadian)
                        velocity_y = velocity * math.sin(angleInRadian)
                        ballRect.x += velocity_x
                        ballRect.y += velocity_y
                        velocity -= 1
                        draw_window(ballRect, ballRect)
                        gameClock.tick(FPS)
                    
                    # end player 1's turn
                    player1trun = False
                    pygame.event.clear()


def handle_collision(ballRect, goalRect):
    """If collide, add GOAL to the event list"""
    if ballRect.colliderect(goalRect):
        print("Collision!")
        pygame.event.post(pygame.event.Event(GOAL))

def handle_startScreen():
    """Implement start screen"""

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

def main():
    ballRect = pygame.Rect((100, 200), (BALL_WIDTH, BALL_HEIGHT)) # put the initial position of the ball into bracket
    goalRect = pygame.Rect((400, 200), (GOAL_WIDTH, GOAL_HEIGHT)) # put the initial position of the goal into bracket
    draw_window(ballRect, goalRect)


    pygame.event.post(pygame.event.Event(PLAYER1TURN))

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

            if event.type == PLAYER1TURN:
                # move ball according to the rule
                ballRect_movement(ballRect)
                # isPlayer1Turn = False

        key_pressed = pygame.key.get_pressed()

        # move to gameover screen when collided
        handle_collision(goalRect, ballRect)

        # update the screen
        draw_window(ballRect, goalRect)

        # set FPS
        gameClock.tick(FPS)

if __name__ == "__main__":
    main()
