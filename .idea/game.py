#Yiheng Su
#Jan, 10, 2022

####################### Setup #########################
# useful imports
import sys
import random
import math
from turtle import width
import numpy as np
import os.path

# import pygame
import pygame
from pygame.locals import *
from pygame import mixer

import game_objects as go
import sound as s

# initialize pygame
pygame.init()

# initialize bgm
mixer.init()
sound = s.Sound(mixer)

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
massUp_img = pygame.image.load("../pictures/massUp.png").convert_alpha()
powerUp_img = pygame.image.load("../pictures/powerUp.png").convert_alpha()
speedUp_img = pygame.image.load("../pictures/speedUp.png").convert_alpha()
randomAngle_img = pygame.image.load("../pictures/randomAngle.png").convert_alpha()
exchangePosition_img = pygame.image.load("../pictures/exchangePosition.png").convert_alpha()
golfClub_img = pygame.image.load("../pictures/golfClub.png").convert_alpha()

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

# set projectiles
golfClub = go.GolfClub(golfClub_img, 500, 600, 80, 80, arrow)
projectileList = [golfClub]

# set consumables
massUp = go.MassUp(massUp_img, 700, 100, 40, 40)
speedUp = go.SpeedUp(speedUp_img, 400, 400, 40, 40)
powerUp = go.PowerUp(powerUp_img, 500, 500, 120, 120)
randomAngle = go.RandomAngle(randomAngle_img, 650, 300, 40, 40)
exchangePosition = go.ExchangePosition(exchangePosition_img, 800, 250, 40, 40)
consumableList = [speedUp, massUp, powerUp, randomAngle, exchangePosition]

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
accl1 = go.AcclPad(hole_img, 100, 100, 80, 80, 2, (1, 0))
sand1 = go.SandPit(hole_img, 100, 550, 60, 60)
tor1 = go.Tornado(hole_img, 700, 500, 80, 80)
TERRAIN_LIST = [accl1, sand1, tor1]


# testing stuff
test_rect = pygame.Rect((300,300), (100,100))
BOUNDARY.append(test_rect)



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

    for i in range(4, len(BOUNDARY)):
        pygame.draw.rect(screen, BLACK, BOUNDARY[i])

    # update the screen
    # pygame.display.update()

def draw_players(player_list, current_player, hole, arrow):
    # draw consumable on the screen
    for consumable in consumableList:
        screen.blit(consumable.image, (consumable.get_x(), consumable.get_y()))

    for tr in TERRAIN_LIST:
        pygame.draw.rect(screen, tr.color, tr.rect)

    if arrow.is_visible:
        screen.blit(arrow.rot_img, (arrow.rot_rect.x, arrow.rot_rect.y))
    for plr in player_list:
        screen.blit(plr.image, (plr.get_x(), plr.get_y()))
    screen.blit(hole.image, (hole.get_x(), hole.get_y()))

        # draw projectile on the screen
    for projectile in projectileList:
        screen.blit(projectile.image, (projectile.get_x(), projectile.get_y()))
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
        ball1.advance(10)
        ball2.advance(10)


def handle_collision_ball_rect(ball, rect):
    """handles collision between a ball object and a rectangle"""
<<<<<<< HEAD
    # add sound
    sound.collision_ball_wall()
=======
>>>>>>> remotes/origin/Blitzen

    orig_x = ball.x
    orig_y = ball.y
    collisions = []
    ball.x  = orig_x - abs(ball.vel_x)
    collisions.append(check_collision_ball_rect(ball, rect))

    ball.x  = orig_x + abs(ball.vel_x)
    collisions.append(check_collision_ball_rect(ball, rect))

    ball.y  = orig_y + abs(ball.vel_y)
    collisions.append(check_collision_ball_rect(ball, rect))

    ball.y  = orig_y - abs(ball.vel_y)
    collisions.append(check_collision_ball_rect(ball, rect))

    ball.x = orig_x
    ball.y = orig_y

    #0 vertical 1 horizontal 2 corner
    if collisions[0] != collisions[1] and collisions[2] == collisions[3]:
        return 0

    if collisions[0] == collisions[1] and collisions[2] != collisions[3]:
        return 1

    if collisions[0] != collisions[1] and collisions[2] != collisions[3]:
        return 2


def check_collision_v(ball, rect):
    '''check if the next advance of ball will result in a vertical collision'''
    if ball.x + ball.RADIUS > rect.x and ball.x + ball.RADIUS < rect.x + rect.width:
        return True
    elif round(ball.x + 2*ball.RADIUS) < rect.x or ball.x > rect.x + rect.width:
        return False

    elif ball.y + 2*ball.RADIUS > rect.y and ball.y < rect.y + rect.height:
        return ball.x + 2*ball.RADIUS > rect.x and ball.x < rect.x + rect.width
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
    if ball.y + ball.RADIUS > rect.y and ball.y + ball.RADIUS < rect.y + rect.height:
        return True
    elif ball.y + 2*ball.RADIUS < rect.y or ball.y > rect.y + rect.height:
        return False
    elif ball.y + 2*ball.RADIUS > rect.y and ball.y < rect.y + rect.height:
        return ball.y + 2*ball.RADIUS > rect.y and ball.y < rect.y + rect.height
    else:
        return check_corner_collision(ball, rect)


def handle_collision_ball_hole(ball, holeRect):
    """If collide, add GOAL to the event list"""
    if check_collision_ball_rect(ball, holeRect):
        print("Collision!")
        pygame.event.post(pygame.event.Event(GOAL))


def handle_collision_ball_consumables(ball, consumables_list):
    for consumable in consumables_list:
        if check_collision_ball_rect(ball, consumable.get_rect()):
            print("Collide with consumable")
            # activate the consumable
            consumable.activate(ball)
            # remove consumable from the list and screen
            consumables_list.remove(consumable)


def handle_plr_consumables(plr):
    for consumable in plr.consumables:
        if consumable.need_to_deactivate():
            print("Deactivate: " + consumable.id)
            consumable.deactivate(plr)
            plr.consumables.remove(consumable)


def handle_conllision_ball_projectiles(ball, projectiles_list):
    for projectile in projectiles_list:
        if check_collision_ball_rect(ball, projectile.get_rect()):
            print("Collide with projectile")
            projectile.need_arrow = True
            projectiles_list.remove(projectile)
            ball.projectiles.append(projectile)

def handle_golfClub_function(golfClub, ball):
    for wall in BOUNDARY:
        if wall.colliderect(golfClub.get_rect()):
            golfClub.is_moving = False

    if check_collision_ball_rect(ball, golfClub.get_rect()):
        ball.angle = golfClub.angle
        ball.vel_x = golfClub.vel_x * 2
        ball.vel_y = golfClub.vel_y * 2
        golfClub.is_moving = False

def handle_terrain():
    for plr in player_list:
        for tr in TERRAIN_LIST:
            if tr.rect.colliderect(plr.rect):
                if tr.id == "sand":
<<<<<<< HEAD
                    plr.acc = 5
=======
                    plr.acc = 3
>>>>>>> remotes/origin/Blitzen

                if tr.id == "accl":
                    plr.vel_x += tr.orientation[0] * tr.scale
                    plr.vel_y += tr.orientation[1] * tr.scale
                    plr.update_angle()

                if tr.id == "tor":
                    # deal with tornado
                    dx = plr.x - tr.center_x
                    dy = plr.y - tr.center_y
                    
                    angle = math.atan2(dy, dx)
                    if dx > 0:
                        plr.vel_x += tr.scale * math.cos(angle)
                    else:
                        plr.vel_x -= tr.scale * math.cos(angle)
                    if dy > 0:
                        plr.vel_y += tr.scale * math.sin(angle)
                    else:
                        plr.vel_y -= tr.scale * math.sin(angle)
                    plr.update_angle()
                    

                elif plr.acc == 5:
                    plr.acc = 1


def rot_image(rect, image, angle):
    rotated_img = pygame.transform.rotate(image, angle)
    return rotated_img, rect.x + rect.width/2 - (rotated_img.get_width()/2), rect.y + rect.height/2 - (rotated_img.get_height()/2)

####################### Handle Screens #########################

def handle_startScreen():
    """Implement start screen"""
    pass

def check_collision_ball_rect(ball, rect):
    col_v = check_collision_v(ball, rect)
    col_h = check_collision_h(ball, rect)
    return col_v and col_h

def move(plr):
    '''Moves the player and handles collision with obstacles'''

    steps = 10

    for i in range(steps):
        plr.advance(steps)
        for wall in BOUNDARY:
            if check_collision_ball_rect(plr, wall):
                col_type = handle_collision_ball_rect(plr, wall)
                plr.traceback(steps)
                if col_type == 0:
                    plr.reflect_y()

                if col_type == 1:
                    plr.reflect_x()

                if col_type == 2:
                    plr.reflect_x()
                    plr.reflect_y()
        handle_collision_ball_ball(plr, plr.opponent)

    plr.update_pos()



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


def read_level(filename):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'levels', filename))
    with open(path) as f:
        lines = f.readlines()
        for l in lines:
            l = l.split(",")
            if l[0] == "w":
                wall = pygame.Rect((int(l[1]), int(l[2])), (int(l[3]), int(l[4])))
                BOUNDARY.append(wall)

        f.close()

def save_level():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'levels', "new level.txt"))
    lvl = ""
    for i in range(5, len(BOUNDARY)):
        line = "w," + str(BOUNDARY[i].x)+"," + str(BOUNDARY[i].y)+"," + str(BOUNDARY[i].width)+"," + str(BOUNDARY[i].height)+"\n"
        lvl += line
    with open(path, 'w') as f:
        f.write(lvl)
        f.close

def check_button_clicked(button) -> bool:
    """Check if player click the button"""
    mousePos = pygame.mouse.get_pos()
    if button.left < mousePos[0] < button.right and button.top < mousePos[1] < button.bottom:
        return True
    else:
        return False

####################### Main Event Loop #########################

def main():
    global current_player, tracing, rect_preview, projectileList

    draw_window(0)
    draw_players(player_list, current_player, hole, arrow)

    # show the start screen
    handle_startScreen()

    # play bgm
    sound.bgm()

    print("Entering main loop")
    force_scale = 0
    topleft = (0, 0)
    wh = (0, 0)
    editing = False
    tracing = False
    rect_preview = pygame.Rect((0, 0), (0, 0))

    current_projectile = None

    while True:

        if tracing:
            bottomright = pygame.mouse.get_pos()
            wh = (bottomright[0] -  topleft[0], bottomright[1] -  topleft[1])
            rect_preview = pygame.Rect(topleft, wh)

        if current_projectile is None:
            plr = player_list[current_player]
        else:
            if projectile.need_arrow:
                plr = current_projectile
                current_projectile.acc = 0
                projectileList.append(current_projectile)
                projectile.need_arrow = False

        # Check every event in the event list
        for event in pygame.event.get():
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
                    # Add sound
                    if current_projectile is None:
                        sound.normal_hit()
                    else:
                        sound.hard_hit()
                    # check if we need to delet the consumables
                    handle_plr_consumables(player_list[current_player])
                    plr.launch(VELOCITY)
                    arrow.is_visible = False
                    current_player = len(player_list)-1-current_player
                    nxt_p = player_list[current_player]
                    if nxt_p.get_vel() < 1:
                        plr = player_list[current_player]
                        arrow.reset(nxt_p)

                if event.key == pygame.K_e:
                    editing = not editing
                    print("editing: "+ str(editing))

                if event.key == pygame.K_s:
                    #save
                    save_level()

                if event.key == pygame.K_r:
                    #reads level file
                    level_name = input("Please input level file name: ")
                    read_level(level_name)

                if event.key == pygame.K_1:
                    tracing = True
                    topleft = pygame.mouse.get_pos()

                if event.key == pygame.K_2:
                    tracing = False
                    bottomright = pygame.mouse.get_pos()
                    wh = (bottomright[0] -  topleft[0], bottomright[1] -  topleft[1])
                    BOUNDARY.append(pygame.Rect(topleft, wh))

                if event.key == pygame.K_3:
                    for projectile in player_list[current_player].projectiles:
                        # if the player have golfClub projectile
                        if projectile.id == "golfClub":
                            current_projectile = projectile
                            current_projectile.set_x(player_list[current_player].x - 25)
                            current_projectile.set_y(player_list[current_player].y - 25)
                            current_projectile.attack_object = player_list[current_player].opponent
                            current_projectile.is_moving = True
                            arrow.reset(player_list[current_player])
                        else:
                            print(False)

                if event.key == pygame.K_BACKSPACE:
                    mp = pygame.mouse.get_pos()
                    for i in range(4, len(BOUNDARY)):
                        if mp[0] > BOUNDARY[i].x and mp[0] < BOUNDARY[i].right and mp[1] > BOUNDARY[i].y and mp[1] < BOUNDARY[i].bottom:
                            del BOUNDARY[i]
                            break

                draw_players(player_list, current_player, hole, arrow)

        # update the screen
        draw_window(force_scale)
        
        # set movement of projectile
        if current_projectile != None:
            if current_projectile.is_moving:
                handle_golfClub_function(current_projectile, current_projectile.attack_object)
                current_projectile.move()
            else:
                projectileList.remove(current_projectile)
                current_projectile = None

        
        for i in range(len(player_list)):
            handle_collision_ball_consumables(player_list[i], consumableList)
            handle_terrain()
            if current_projectile is None:
                handle_conllision_ball_projectiles(player_list[i], projectileList)
            handle_collision_ball_ball(player_list[0], player_list[1])
            move(player_list[i])
            handle_terrain()
            handle_collision_ball_hole(player_list[i], hole.get_rect())


        if plr.get_vel() < 2 and plr.get_vel() != 0:
            arrow.reset(plr)
        elif plr.get_vel() > 1:
            arrow.is_visible = False

        draw_players(player_list, current_player, hole, arrow)

        # set FPS
        gameClock.tick(FPS)

if __name__ == "__main__":
    main()