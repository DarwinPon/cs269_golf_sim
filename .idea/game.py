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
import game_objects as go

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
VELOCITY = 8

tracing = False
rect_preview = pygame.Rect((0, 0), (0, 0))

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
massUp_img = pygame.image.load("../pictures/crown.png").convert_alpha()
powerUp_img = pygame.image.load("../pictures/massUp.png").convert_alpha()
speedUp_img = pygame.image.load("../pictures/golfClub.png").convert_alpha()
randomAngle_img = pygame.image.load("../pictures/broom.png").convert_alpha()

# background scenes
BACKGROUND = pygame.transform.scale(pygame.image.load("../pictures/background.png").convert_alpha(), (WIDTH, HEIGHT))
STARTSCREEN = pygame.transform.scale(pygame.image.load("../pictures/startScreen.png").convert_alpha(), (WIDTH, HEIGHT))

# set up arrow and hole
arrow = go.Arrow(arrow_img, 0, 0, BALL_WIDTH*3, BALL_HEIGHT*3)
hole = go.Ball(hole_img, WIDTH - 75, HEIGHT / 2 - BALL_WIDTH / 2, BALL_WIDTH, BALL_HEIGHT, arrow)

# set up players
player1 = go.Ball(ball_img1, 75, HEIGHT / 2 - 50 - BALL_WIDTH / 2, BALL_WIDTH, BALL_HEIGHT, arrow)
player2 = go.Ball(ball_img2, 75, HEIGHT / 2 + 50 + BALL_WIDTH / 2, BALL_WIDTH, BALL_HEIGHT, arrow)
player1.set_opponent(player2)
player2.set_opponent(player1)

arrow.reset(player1)
player_list = [player1, player2]

# set consumables
massUp = go.MassUp(massUp_img, 700, 100, 120, 120)
speedUp = go.SpeedUp(speedUp_img, 400, 400, 120, 120)
powerUp = go.PowerUp(powerUp_img, 500, 500, 120, 120)
randomAngle = go.RandomAngle(randomAngle_img, 650, 300, 40, 40)
consumableList = [speedUp, massUp, powerUp, randomAngle]

# create a font
afont = pygame.font.SysFont( "Helvetica", 32, bold=True )
# render a surface with some text
text = afont.render( "Clean up time", True, (0, 0, 0) )

# put rectangles on the boundaries
UPPERBOUND_RECT = pygame.Rect( (0, -35), (WIDTH, 60) )
LOWERBOUND_RECT = pygame.Rect( (0, HEIGHT - 25), (WIDTH, 60) )
LEFTBOUND_RECT = pygame.Rect( (-30, 0), (60, HEIGHT) )
RIGHTBOUND_RECT = pygame.Rect( (WIDTH - 30, 0), (60, HEIGHT) )

BOUNDARY = [UPPERBOUND_RECT, LOWERBOUND_RECT, LEFTBOUND_RECT, RIGHTBOUND_RECT]


# adding terrain
accl1 = go.AcclPad(hole_img, 100, 100, 80, 80, 3, (1, 0))
sand1 = go.SandPit(hole_img, 100, 550, 60, 60)
TERRAIN_LIST = []

# testing stuff
test_rect = pygame.Rect((300,300), (100,100))
BOUNDARY.append(test_rect)

# adding walls
WALLS = []
'''
WALLS.append(pygame.Rect( (100, 240), (220, 60) )) #1

WALLS.append(pygame.Rect( (0, 540), (40, 100) )) #3
WALLS.append(pygame.Rect( (90, 480), (140, 30) ))
WALLS.append(pygame.Rect( (280, 540), (40, 120) ))
WALLS.append(pygame.Rect( (90, 690), (140, 30) ))
'''




####################### Filling the Screen #########################
def draw_window(scale):
    global tracing, rect_preview
    # clear the screen with background
    screen.blit(BACKGROUND, (0,0))

    # now draw the surfaces to the screen using the blit function

    # display debug info
    force_text = INFO_FONT.render("Launch force: " + str(scale), 1, BLACK)
    screen.blit(force_text, (10, HEIGHT-force_text.get_height()-5))
    pygame.draw.rect(screen, BLACK, test_rect)
    if tracing:
        pygame.draw.rect(screen, BLACK, rect_preview)

    for wall in WALLS:
        pygame.draw.rect(screen, BLACK, wall)

    # update the screen
    # pygame.display.update()

def draw_players(player_list, current_player, hole, arrow):
    for consumable in consumableList:
        screen.blit(consumable.image, (consumable.get_x(), consumable.get_y()))

    for tr in TERRAIN_LIST:
        pygame.draw.rect(screen, tr.color, tr.rect)

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
        print("Ball Ball Collision!")
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


def test_collision_ball_rectangle(ball, rect):
    r = ball.get_radius()
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


def handle_collision_ball_rect(ball, rect):
    """handles collision between a ball object and a rectangle"""

    current_col_v = check_collision_v(ball, rect)
    current_col_h = check_collision_h(ball, rect)
    ball.advance()

    new_col_v = check_collision_v(ball, rect)
    new_col_h = check_collision_h(ball, rect)
    ball.trace_back()


    if current_col_h and new_col_h and current_col_v != new_col_v:
        print("vertical")
        ball.reflect_y()

    elif current_col_h != new_col_h and current_col_v and new_col_v:
        print("horizontal")
        ball.reflect_x()

    elif current_col_h != new_col_h and current_col_v != new_col_v:
        print("corner")
        ball.reflect_x()
        ball.reflect_y()
        ball.move()


def check_collision_v(ball, rect):
    '''check if the next advance of ball will result in a vertical collision'''
    if ball.x + ball.RADIUS >= rect.x and ball.x + ball.RADIUS <= rect.x + rect.width:
        return True
    elif round(ball.x + 2*ball.RADIUS) < rect.x or ball.x > rect.x + rect.width:
        return False

    elif ball.y + 2*ball.RADIUS >= rect.y and ball.y <= rect.y + rect.height:
        return ball.x + 2*ball.RADIUS >= rect.x and ball.x <= rect.x + rect.width
    else:
        return check_corner_collision(ball, rect)


def check_corner_collision(ball, rect):
    x = ball.x + ball.RADIUS
    y = ball.y + ball.RADIUS
    if math.hypot(abs(x-rect.topleft[0]), abs(y-rect.topleft[1])) <= ball.RADIUS:
        return True
    elif math.hypot(abs(x-rect.bottomleft[0]), abs(y-rect.bottomleft[1])) <= ball.RADIUS:
        return True
    elif math.hypot(abs(x-rect.bottomright[0]), abs(y-rect.bottomright[1])) <= ball.RADIUS:
        return True
    elif math.hypot(abs(x-rect.topright[0]), abs(y-rect.topright[1])) <= ball.RADIUS:
        return True
    else:
        return False


def check_collision_h(ball, rect):
    '''check if the next advance of ball will result in a horizontal collision'''
    if ball.y + ball.RADIUS >= rect.y and ball.y + ball.RADIUS <= rect.y + rect.height:
        return True
    elif ball.y + 2*ball.RADIUS < rect.y or ball.y > rect.y + rect.height:
        return False
    elif ball.y + 2*ball.RADIUS >= rect.y and ball.y <= rect.y + rect.height:
        return ball.y + 2*ball.RADIUS >= rect.y and ball.y <= rect.y + rect.height
    else:
        return check_corner_collision(ball, rect)


def handle_collision_ball_hole(ball, holeRect):
    """If collide, add GOAL to the event list"""
    if test_collision_ball_rectangle(ball, holeRect):
        print("Collision!")
        pygame.event.post(pygame.event.Event(GOAL))


def handle_collision_ball_consumables(ball, consumables_list):
    for consumable in consumables_list:
        if test_collision_ball_rectangle(ball, consumable.get_rect()):
            print("Collide with consumable")
            # set the plr to the consumable
            consumable.activate(ball)
            # remove consumable from the list and screen
            consumables_list.remove(consumable)
            # add current consumable into the plr's consumables list
            ball.consumables.append(consumable)


def handle_boundries(plr):
    """Make sure the ball bounces on the boundries"""
    for wall in BOUNDARY:
        handle_collision_ball_rect(plr, wall)

    for wall in WALLS:
        handle_collision_ball_rect(plr, wall)



def handle_plr_consumables(plr):
    for consumable in plr.consumables:
        if consumable.need_to_deactivate():
            print("deactivate")
            consumable.deactivate(plr)
            plr.consumables.remove(consumable)


def handle_terrain(plr):
    for tr in TERRAIN_LIST:
        if tr.rect.colliderect(plr.rect):
            if tr.id is "sand":
                plr.acc = 3
            else:
                plr.acc = 1
            if tr.id is "accl":
                plr.vel_x += tr.orientation[0] * tr.scale
                plr.vel_y += tr.orientation[1] * tr.scale
                plr.update_angle()
        else:
            plr.acc = 1


def rot_image(rect, image, angle):
    rotated_img = pygame.transform.rotate(image, angle)
    return rotated_img, rect.x + rect.width/2 - (rotated_img.get_width()/2), rect.y + rect.height/2 - (rotated_img.get_height()/2)

####################### Handle Screens #########################

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

####################### Main Event Loop #########################

def main():
    global current_player, tracing, rect_preview
    draw_window(0)
    draw_players(player_list, current_player, hole, arrow)

    # show the start screen
    handle_startScreen()

    print("Entering main loop")
    force_scale = 0
    topleft = (0, 0)
    wh = (0, 0)
    editing = False
    tracing = False
    rect_preview = pygame.Rect((0, 0), (0, 0))



    while True:

        if tracing:
            bottomright = pygame.mouse.get_pos()
            wh = (bottomright[0] -  topleft[0], bottomright[1] -  topleft[1])
            rect_preview = pygame.Rect(topleft, wh)

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
                    plr.left(player_list[current_player].turn_angle)
                    rot_img, rot_x, rot_y = rot_image(arrow.rect, arrow.image, -plr.get_angle())
                    arrow.set_rot(rot_img, rot_x, rot_y)

                if event.key == pygame.K_RIGHT:
                    plr.right(player_list[current_player].turn_angle)
                    rot_img, rot_x, rot_y = rot_image(arrow.rect, arrow.image, -plr.get_angle())
                    arrow.set_rot(rot_img, rot_x, rot_y)

                if event.key == pygame.K_SPACE:
                    # check if we need to delet the consumables
                    handle_plr_consumables(player_list[current_player])
                    plr.launch(VELOCITY)
                    arrow.is_visible = False
                    current_player = len(player_list)-1-current_player
                    nxt_p = player_list[current_player]
                    if nxt_p.get_vel() < 1:
                        arrow.reset(nxt_p)

                if event.key == pygame.K_e:
                    editing = not editing
                    print("editing: "+ str(editing))

                if event.key == pygame.K_1:
                    tracing = True
                    topleft = pygame.mouse.get_pos()


                if event.key == pygame.K_2:
                    tracing = False
                    bottomright = pygame.mouse.get_pos()
                    wh = (bottomright[0] -  topleft[0], bottomright[1] -  topleft[1])
                    WALLS.append(pygame.Rect(topleft, wh))


                if event.key == pygame.K_BACKSPACE:
                    mp = pygame.mouse.get_pos()
                    for i in range(len(WALLS)):
                        if mp[0] > WALLS[i].x and mp[0] < WALLS[i].right and mp[1] > WALLS[i].y and mp[1] < WALLS[i].bottom:
                            del WALLS[i]
                            break


                    

                draw_players(player_list, current_player, hole, arrow)

        # update the screen
        draw_window(force_scale)

        for i in range(len(player_list)):
            handle_terrain(player_list[i])
            handle_collision_ball_ball(player_list[0], player_list[1])
            handle_boundries(player_list[i])
            player_list[i].move()
            handle_collision_ball_hole(player_list[i], hole.get_rect())
            handle_collision_ball_consumables(player_list[i], consumableList)

        plr = player_list[current_player]

        if plr.get_vel() < 2 and plr.get_vel() != 0:
            arrow.reset(plr)
        elif plr.get_vel() > 1:
            arrow.is_visible = False

        draw_players(player_list, current_player, hole, arrow)

        # set FPS
        gameClock.tick(FPS)

if __name__ == "__main__":
    main()