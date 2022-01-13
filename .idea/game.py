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
BLACK = (0, 0, 0)

# game events
GOAL = pygame.USEREVENT + 1
PLAYER1TURN = pygame.USEREVENT + 1

#initial velocity when force scale is 0
VELOCITY = 5

# initialize the fonts
try:
    pygame.font.init()
except:
    print("Fonts unavailable")
    sys.exit()

# create font for displaying debug info
INFO_FONT = pygame.font.SysFont("comicsans", 15)

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
ARROW_WIDTH, ARROW_HEIGHT = 90, 90
ball = pygame.image.load( "golfball.png" ).convert_alpha() # put the name of ball image here
arrow = pygame.image.load( "arrow.png" ).convert_alpha()

ball = pygame.transform.scale(ball, (BALL_WIDTH, BALL_HEIGHT)) # scale an image
<<<<<<< Yiheng1.1
arrow = pygame.transform.scale(arrow, (ARROW_WIDTH, ARROW_HEIGHT)) # scale an image

=======
ball = pygame.transform.rotate(ball, -90)
>>>>>>> local


# create a font
afont = pygame.font.SysFont( "Helvetica", 32, bold=True )
# render a surface with some text
text = afont.render( "Clean up time", True, (0, 0, 0) )

####################### Filling the Screen #########################
def draw_window(image, ballRect, arrowRect, scale):
    # clear the screen with white
    screen.fill(WHITE)

    # now draw the surfaces to the screen using the blit function

    if arrowRect != None:
        screen.blit(image , (arrowRect.x, arrowRect.y) )
    screen.blit(ball , (ballRect.x, ballRect.y) )

    # display debug info
    force_text = INFO_FONT.render("Launch force: " + str(scale), 1, BLACK)
    screen.blit(force_text, (10, HEIGHT-force_text.get_height()-5))

    # update the screen
    pygame.display.update()

####################### Add Movement #########################
def ballRect_movement(ballRect, arrowRect):
    """Implement ball movement"""
<<<<<<< Yiheng1.1
    global arrow, ball
=======
    global ball
>>>>>>> local
    angleInDegree = 0
    angularVel = 15
    player1trun = True
    force_scale = 0

    arrowRect = pygame.Rect((ballRect.x-ballRect.width, ballRect.y-ballRect.height), (ARROW_WIDTH, ARROW_HEIGHT))
    while player1trun:
        rot_rect = arrowRect.copy()
        rot_arrow = arrow.copy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and force_scale < 10:
                    force_scale += 1
                if event.key == pygame.K_DOWN and force_scale > 0:
                    force_scale -= 1

                draw_window(rot_arrow, ballRect, rot_rect, force_scale)

                if event.key == pygame.K_a:
                    angleInDegree -= angularVel
<<<<<<< Yiheng1.1
                    rot_arrow, rot_rect.x, rot_rect.y = rot_image(arrowRect, arrow, -angleInDegree)

=======
                    blitRotateCenter(ball, ballRect.topleft, -angleInDegree)
      
>>>>>>> local
                if event.key == pygame.K_d:
                    angleInDegree += angularVel
                    rot_arrow, rot_rect.x, rot_rect.y = rot_image(arrowRect, arrow, -angleInDegree)

                if event.key == pygame.K_SPACE:
                    angleInRadian = angleInDegree * (math.pi / 180)

                    velocity = VELOCITY * (1 + force_scale/2)
                    # move some distance
                    while abs(velocity) > 1:
                        velocity_x = velocity * math.cos(angleInRadian)
                        velocity_y = velocity * math.sin(angleInRadian)
                        ballRect.x += velocity_x
                        ballRect.y += velocity_y
                        velocity -= 1
                        draw_window(ball, ballRect, ballRect, 0)
                        gameClock.tick(FPS)

                    # end player 1's turn
                    player1trun = False
                    # pygame.event.clear()

                #reset arrow position


                draw_window(rot_arrow, ballRect, rot_rect, force_scale)


def blitRotateCenter(image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    screen.fill(WHITE)
    screen.blit(rotated_image, new_rect)
    pygame.display.update()

def handle_collision(ballRect, goalRect):
    """If collide, add GOAL to the event list"""
    if ballRect.colliderect(goalRect):
        print("Collision!")
        pygame.event.post(pygame.event.Event(GOAL))


def handle_boundries(ballRect):
    """Make sure the ball bounces on the boundries"""
    pass
    #if ballRect.x <= 0 or ballRect.x >= 640-ballRect.width:


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


def rot_image(rect, image, angle):
    rotated_img = pygame.transform.rotate(image, angle)

    return rotated_img, rect.x + rect.width/2 - (rotated_img.get_width()/2), rect.y + rect.height/2 - (rotated_img.get_height()/2)


####################### Main Event Loop #########################

def main():
    ballRect = pygame.Rect((100, 200), (BALL_WIDTH, BALL_HEIGHT)) # put the initial position of the ball into bracket
    arrowRect = pygame.Rect((ballRect.x-ballRect.width, ballRect.y-ballRect.height), (ARROW_WIDTH, ARROW_HEIGHT))
    draw_window(ball, ballRect, ballRect, 0)


    pygame.event.post(pygame.event.Event(PLAYER1TURN))

    # show the start screen
    handle_startScreen()

    print("Entering main loop")
    force_scale = 0
    velocity = 0
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
                ballRect_movement(ballRect, arrowRect)
                # isPlayer1Turn = False

        key_pressed = pygame.key.get_pressed()


        # move ball according to the rule
        ballRect_movement(ballRect, arrowRect)



        key_pressed = pygame.key.get_pressed()

        # move to gameover screen when collided
        #handle_collision(goalRect, ballRect)

        # update the screen
        draw_window(ball, ballRect, None, force_scale)

        # set FPS
        gameClock.tick(FPS)

if __name__ == "__main__":
    main()
