#Yiheng Su
#Jan, 10, 2022

####################### Setup #########################
# useful imports
from cmath import tan
from email.mime import image
import sys
import random
import math
from turtle import width
from webbrowser import BackgroundBrowser
import numpy as np

# import pygame
import pygame
from game_objects import Ball
from game_objects import Arrow

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
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )


# create caption for the screen
pygame.display.set_caption("Golf")

####################### Making Content #########################

# load some images
# set the size of the image

BALL_WIDTH, BALL_HEIGHT = 30, 30
ARROW_WIDTH, ARROW_HEIGHT = BALL_WIDTH*3, BALL_HEIGHT*3
ball_img1 = pygame.image.load( "../pictures/player1ball.png" ).convert_alpha() # put the name of ball image here
ball_img2 = pygame.image.load( "../pictures/player2ball.png" ).convert_alpha()
arrow_img = pygame.image.load( "../pictures/black_arrow.png" ).convert_alpha()
hole_img = pygame.image.load("../pictures/hole.png").convert_alpha()

# background scenes
BACKGROUND = pygame.transform.scale(pygame.image.load("../pictures/background.png").convert_alpha(), (WIDTH, HEIGHT))
STARTSCREEN = pygame.transform.scale(pygame.image.load("../pictures/startScreen.png").convert_alpha(), (WIDTH, HEIGHT))


arrow = Arrow(arrow_img, 0, 0, BALL_WIDTH*3, BALL_HEIGHT*3)
player1 = Ball(ball_img1, 75, HEIGHT / 2 - 50 - BALL_WIDTH / 2, BALL_WIDTH, BALL_HEIGHT, arrow)
player2 = Ball(ball_img2, 75, HEIGHT / 2 + 50 + BALL_WIDTH / 2, BALL_WIDTH, BALL_HEIGHT, arrow)
hole = Ball(hole_img, WIDTH - 75, HEIGHT / 2 - BALL_WIDTH / 2, BALL_WIDTH, BALL_HEIGHT, arrow)

arrow.reset(player1)
player_list = [player1, player2]

# put rectangles on the boundaries
UPPERBOUND_RECT = pygame.Rect( (0, 0), (WIDTH, 25) )
LOWERBOUND_RECT = pygame.Rect( (0, HEIGHT - 25), (WIDTH, 25) )
LEFTBOUND_RECT = pygame.Rect( (0, 0), (33, HEIGHT) )
RIGHTBOUND_RECT = pygame.Rect( (WIDTH - 30, 0), (30, HEIGHT) )
BOUNDARY = [UPPERBOUND_RECT, LOWERBOUND_RECT, LEFTBOUND_RECT, RIGHTBOUND_RECT]

# create a font
afont = pygame.font.SysFont( "Helvetica", 32, bold=True )
# render a surface with some text
text = afont.render( "Clean up time", True, (0, 0, 0) )

####################### Filling the Screen #########################
def draw_window(scale):
    # clear the screen with background
    screen.blit(BACKGROUND, (0,0))

    # now draw the surfaces to the screen using the blit function

    # display debug info
    force_text = INFO_FONT.render("Launch force: " + str(scale), 1, BLACK)
    screen.blit(force_text, (10, HEIGHT-force_text.get_height()-5))

    # update the screen
    # pygame.display.update()

def draw_players(player_list, current_player, hole, arrow):
    if arrow.is_visible:
        screen.blit(arrow.rot_img, (arrow.rot_rect.x, arrow.rot_rect.y))
    for plr in player_list:
        screen.blit(plr.image, (plr.get_x(), plr.get_y()))
    screen.blit(hole.image, (hole.get_x(), hole.get_y()))
    # update the screen
    pygame.display.update()

####################### Add Movement #########################

def handle_collision_ball_ball(ball1, ball2):

    dx = ball1.x - ball2.x
    dy = ball1.y - ball2.y

    distance = math.hypot(dx, dy)
    if distance <= ball1.RADIUS + ball2.RADIUS:
        print("Collide!")
        if ball1.get_vel() == 0 and ball2.get_vel() == 0:
            ball1.vel_x = 1
            ball1.vel_y = 1
        m1, m2 = ball1.mass, ball2.mass
        M = m1 + m2
        r1, r2 = np.array((ball1.x+ball1.RADIUS, ball1.y+ball1.RADIUS)), np.array((ball2.x+ball2.RADIUS, ball2.y+ball2.RADIUS))
        d = np.linalg.norm(r1 - r2)**2
        v1, v2 = np.array((ball1.vel_x, ball1.vel_y)), np.array((ball2.vel_x, ball2.vel_y))
        u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
        u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
        ball1.vel_x, ball1.vel_y = u1[0], u1[1]
        ball2.vel_x, ball2.vel_y = u2[0], u2[1]
        ball1.update_angle()
        ball2.update_angle()
        ball1.move()
        ball2.move()

        # tangent = -math.degrees(math.atan2(dx, dy)) -90
        # ball1.angle = tangent
        # ball2.angle = tangent
        # (ball1.vel, ball2.vel) = (ball2.vel, ball1.vel)
        #
        # angle = 0.5 * math.pi + tangent
        # ball1.x += math.sin(angle)
        # ball1.y -= math.cos(angle)
        # ball2.x -= math.sin(angle)
        # ball2.y += math.cos(angle)

def test_collision_ball_rectangle(ball, rect):
    r = ball.RADIUS
    ballCenter = (ball.x + r, ball.y + r)
    ball_distance_x = abs(ballCenter[0] - rect.centerx)
    ball_distance_y = abs(ballCenter[1] - rect.centery)
    if ball_distance_x > rect.width / 2 + r or ball_distance_y > rect.height / 2 + r:
        return False
    if ball_distance_x <= rect.width / 2 or ball_distance_y <= rect.height / 2:
        return True
    corner_x = ball_distance_x - rect.width / 2
    corner_y = ball_distance_y - rect.height / 2
    corner_distance = math.hypot(corner_x, corner_y)
    return corner_distance <= r
        
def handle_collision_ball_hole(ball, holeRect):
    """If collide, add GOAL to the event list"""
    if test_collision_ball_rectangle(ball, holeRect):
        print("Collision!")
        pygame.event.post(pygame.event.Event(GOAL))


def handle_boundries(plr):
    """Make sure the ball bounces on the boundries"""
    if plr.x <= 35:
        plr.angle = 180 - plr.angle
        plr.x = 35
        plr.vel_x = abs(plr.vel_x)


    if plr.x >= WIDTH-plr.width - 35:
        plr.angle = 180 - plr.angle
        plr.x = WIDTH-plr.width - 35
        plr.vel_x = - abs(plr.vel_x)

    if plr.y <= plr.height/5 + 30:
        plr.angle = -plr.angle
        plr.y = plr.height/5 + 30
        plr.vel_y = abs(plr.vel_y)


    if plr.y >= HEIGHT - plr.height - 30:
        plr.angle = -plr.angle
        plr.y = HEIGHT - plr.height - 30
        plr.vel_y = - abs(plr.vel_y)


def handle_startScreen():
    """Implement start screen"""
    pass


def handle_gameover():
    """Implement gameover screen"""
    print("Entering gameover screen")
    gameover_text = afont.render( "GOAL!!!", True, (0, 0, 0) )
    # blit the text surface onto the screen
    screen.blit( gameover_text, (WIDTH /2 - 100, HEIGHT / 2 - 50) )
    pygame.display.update()
    pygame.time.wait(2000)
    handle_endScreen()

def handle_endScreen():
    """Implement end screen"""
    screen.blit(STARTSCREEN, (0,0))

    button = pygame.Rect( (180, 80), (280, 80) )
    # pygame.draw.rect( screen, (70, 210, 80), button )
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
    draw_players(player_list, current_player, hole, arrow)

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
                    if nxt_p.get_vel() < 1:
                        arrow.reset(nxt_p)

                draw_players(player_list, current_player, hole, arrow)

        # move to gameover screen when collided
        #handle_collision(goalRect, ballRect)

        # update the screen
        draw_window(force_scale)
        for i in range(len(player_list)):
            player_list[i].move()

            for bound in BOUNDARY:
                if test_collision_ball_rectangle(player_list[i], bound):
                    player_list[i].reflect_x()

            # handle_boundries(player_list[i])
            if i == 0:
                handle_collision_ball_ball(player_list[0], player_list[1])
            else:
                handle_collision_ball_ball(player_list[1], player_list[0])

            handle_collision_ball_hole(player_list[i], hole.get_rect())
        plr = player_list[current_player]

        if plr.get_vel() < 1 and plr.get_vel() != 0:
            arrow.reset(plr)
        elif plr.get_vel() > 1:
            arrow.is_visible = False

        draw_players(player_list, current_player, hole, arrow)


        # set FPS
        gameClock.tick(FPS)

if __name__ == "__main__":
    main()