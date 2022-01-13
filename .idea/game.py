#Yiheng Su
#Jan, 10, 2022

####################### Setup #########################
# useful imports
import sys
import random
import math

# import pygame
import pygame
from Ball import Ball
from Arrow import Arrow

# initialize pygame
pygame.init()

# Frames per second
FPS = 30

# set RGB of colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# game events
GOAL = pygame.USEREVENT + 1

#initial velocity when force scale is 0
VELOCITY = 5
TURN_ANGLE = 15

current_player = 0

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
<<<<<<< HEAD
ARROW_WIDTH, ARROW_HEIGHT = 90, 90
ball = pygame.image.load( "player1ball.png" ).convert_alpha() # put the name of ball image here
arrow = pygame.image.load( "white_arrow.png" ).convert_alpha()
=======
ARROW_WIDTH, ARROW_HEIGHT = BALL_WIDTH*3, BALL_HEIGHT*3
ball_img1 = pygame.image.load( "../assets/player1ball.png" ).convert_alpha() # put the name of ball image here
ball_img2 = pygame.image.load( "../assets/player2ball.png" ).convert_alpha()
arrow_img = pygame.image.load( "../assets/black_arrow.png" ).convert_alpha()

>>>>>>> remotes/origin/Blitzen


<<<<<<< HEAD
=======
arrow = Arrow(arrow_img, 0, 0, BALL_WIDTH*3, BALL_HEIGHT*3)
player1 = Ball(ball_img1, 75, 150, BALL_WIDTH, BALL_HEIGHT, arrow)
player2 = Ball(ball_img2, 75, 250, BALL_WIDTH, BALL_HEIGHT, arrow)

arrow.reset(player1)
player_list = [player1, player2]

>>>>>>> remotes/origin/Blitzen
# create a font
afont = pygame.font.SysFont( "Helvetica", 32, bold=True )
# render a surface with some text
text = afont.render( "Clean up time", True, (0, 0, 0) )

####################### Filling the Screen #########################
def draw_window(scale):
    # clear the screen with white
    screen.fill(WHITE)

    # now draw the surfaces to the screen using the blit function


    # display debug info
    force_text = INFO_FONT.render("Launch force: " + str(scale), 1, BLACK)
    screen.blit(force_text, (10, HEIGHT-force_text.get_height()-5))

    # update the screen
    pygame.display.update()

def draw_players(player_list, current_player, arrow):

<<<<<<< HEAD
                draw_window(rot_arrow, ballRect, rot_rect, force_scale)

                if event.key == pygame.K_a:
                    angleInDegree -= angularVel
                    rot_arrow, rot_rect.x, rot_rect.y = rot_image(arrowRect, arrow, -angleInDegree)

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
                    pygame.event.clear()

                #reset arrow position
                draw_window(rot_arrow, ballRect, rot_rect, force_scale)
=======
    if arrow.is_visible:
        screen.blit(arrow.rot_img, (arrow.rot_rect.x, arrow.rot_rect.y))
    for plr in player_list:
        screen.blit(plr.image, (plr.get_x(), plr.get_y()))
    # update the screen
    pygame.display.update()

####################### Add Movement #########################

>>>>>>> remotes/origin/Blitzen


def handle_collision(ballRect, goalRect):
    """If collide, add GOAL to the event list"""
    if ballRect.colliderect(goalRect):
        print("Collision!")
        pygame.event.post(pygame.event.Event(GOAL))


def handle_boundries(plr):
    """Make sure the ball bounces on the boundries"""

    if plr.x <= 0 or plr.x >= 640-plr.width:

        print("reached")
        plr.reflect_y()
    if plr.y <= plr.height/5 or plr.y >= 480-plr.height:
        plr.reflect_x()


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
    global current_player
    draw_window(0)
    draw_players(player_list, current_player, arrow)


    # show the start screen
    handle_startScreen()

    print("Entering main loop")
    force_scale = 0
    while True:
        # Check every event in the event list
        for event in pygame.event.get():
            plr = player_list[current_player]
            # click quit button, then quit
            if event.type == pygame.QUIT:
                sys.exit()

            # if one player goal, then go to the gameover event
            if event.type == GOAL:
                handle_gameover()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    plr.increase_launchF()

                if event.key == pygame.K_DOWN:
                    plr.decrease_launchF()

                force_scale = plr.launchF
                draw_window(force_scale)

                if event.key == pygame.K_LEFT:
                    plr.left(TURN_ANGLE)
                    rot_img, rot_x, rot_y = rot_image(arrow.rect, arrow.image, -plr.get_angle())

                    arrow.set_rot(rot_img, rot_x, rot_y)

                if event.key == pygame.K_RIGHT:
                    plr.right(TURN_ANGLE)
                    rot_img, rot_x, rot_y = rot_image(arrow.rect, arrow.image, -plr.get_angle())
                    arrow.set_rot(rot_img, rot_x, rot_y)

                if event.key == pygame.K_SPACE:
                    plr.launch(VELOCITY)
                    arrow.is_visible = False
                    current_player = len(player_list)-1-current_player
                    nxt_p = player_list[current_player]
                    if nxt_p.vel < 1:
                        arrow.reset(nxt_p)

                draw_players(player_list, current_player, arrow)

        key_pressed = pygame.key.get_pressed()




        key_pressed = pygame.key.get_pressed()

        # move to gameover screen when collided
        #handle_collision(goalRect, ballRect)

        # update the screen
        draw_window(force_scale)
        for i in range(len(player_list)):
            player_list[i].move()
            handle_boundries(player_list[i])
        plr = player_list[current_player]
        if plr.vel < 1 and plr.vel != 0:
            arrow.reset(plr)


        draw_players(player_list, current_player, arrow)


        # set FPS
        gameClock.tick(FPS)

if __name__ == "__main__":
    main()