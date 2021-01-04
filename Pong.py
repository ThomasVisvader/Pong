import sys
import pygame
import random
import math
from pygame.locals import *


def start():
    direction = random.randrange(45, 325)
    return direction


def left_score():
    global left_points, ballx, bally, ballMoving
    left_points += 1
    ballx = 758
    bally = 388
    ballMoving = False


def right_score():
    global right_points, ballx, bally, ballMoving
    right_points += 1
    ballx = 758
    bally = 388
    ballMoving = False


def change_direction(direction, case):
    if case == 1:  # lopticka prichadza zhora
        if 90 <= direction < 180:  # zlava
            direction = 180 - direction
        elif 180 <= direction < 270:  # zprava
            alpha = direction - 180
            direction = 360 - alpha
    elif case == 2:  # lopticka prichadza zdola
        if 0 <= direction < 90:  # zlava
            direction = 180 - direction
        elif 270 <= direction < 360:  # zprava
            alpha = 360 - direction
            direction = 180 + alpha
    elif case == 3:  # lopticka prichadza k lavej paddle
        if 180 <= direction < 270:  # zhora
            alpha = direction - 180
            direction = 180 - alpha
        elif 270 <= direction < 360:  # zdola
            direction = 360 - direction
    elif case == 4:  # lopticka prichadza k pravej paddle
        if 90 <= direction < 180:  # zhora
            alpha = 180 - direction
            direction = 180 + alpha
        elif 0 <= direction < 90:  # zdola
            direction = 360 - direction
    return direction


def ball_movement(direction, collision):
    global ballx, bally
    if ballx >= width-ballsize:
        left_score()
    elif ballx <= 0:
        right_score()
    else:
        if collision == 0:  # odraz od steny
            if bally >= height - ballsize:  # dolna stena
                direction = change_direction(direction, 1)
            elif bally <= 0:  # horna stena
                direction = change_direction(direction, 2)
        elif collision == 1:
            direction = change_direction(direction, 3)
        elif collision == 2:
            direction = change_direction(direction, 1)
        elif collision == 3:
            direction = change_direction(direction, 2)
        elif collision == 4:
            direction = change_direction(direction, 4)
        elif collision == 5:
            direction = change_direction(direction, 1)
        elif collision == 6:
            direction = change_direction(direction, 2)
        # elif collision == 1:  # odraz od paddle zboku
        #     if ballx <= leftx + paddle_width:  # lava paddle
        #         direction = change_direction(direction, 3)
        #     elif ballx > rightx:  # prava paddle
        #         direction = change_direction(direction, 4)
        # elif collision == 2:  # odraz od paddle zhora/zdola
        #     if (ballx <= leftx + paddle_width and bally == lefty) or \
        #             (ballx > rightx and bally == righty):  # paddle zhora
        #         direction = change_direction(direction, 1)
        #     elif (ballx <= leftx + paddle_width and bally == lefty + paddle_height) or \
        #             (ballx > rightx and bally == righty + paddle_height):  # paddle zdola
        #         direction = change_direction(direction, 2)
        ballx = ballx + (speed * math.sin(math.radians(direction)))
        bally = bally - (speed * math.cos(math.radians(direction)))
    return direction


def left_move_up():
    global lefty
    if lefty <= 0:
        return
    lefty -= speed


def left_move_down():
    global lefty
    if lefty >= 740:
        return
    lefty += speed


def right_move_up():
    global righty
    if righty <= 0:
        return
    righty -= speed


def right_move_down():
    global righty
    if righty >= 740:
        return
    righty += speed


pygame.init()
height = 795
width = 1535
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')

FPS = 60
fpsClock = pygame.time.Clock()

ball = pygame.image.load('Ball.png')
leftpaddle = pygame.image.load('left.png')
rightpaddle = pygame.image.load('right.png')

paddle_height = 55
paddle_width = 41
ballsize = 19
leftx = 140
lefty = 370
rightx = 1354
righty = 370
ballx = 758
bally = 388
speed = 5

left_points = 0
right_points = 0

leftMovingUp = False
leftMovingDown = False
rightMovingUp = False
rightMovingDown = False
ballMoving = False

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            print('Left: {}, Right: {}'.format(left_points, right_points))
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == K_w:
                leftMovingUp = False
            elif event.key == K_s:
                leftMovingDown = False
            elif event.key == K_UP:
                rightMovingUp = False
            elif event.key == K_DOWN:
                rightMovingDown = False
        elif event.type == KEYDOWN:
            if event.key == K_w:
                leftMovingUp = True
            elif event.key == K_s:
                leftMovingDown = True
            elif event.key == K_UP:
                rightMovingUp = True
            elif event.key == K_DOWN:
                rightMovingDown = True
            elif event.key == K_RETURN:
                if not ballMoving:
                    ballMoving = True
                    direction = start()
    if ballMoving:
        direction = ball_movement(direction, 0)
    if leftMovingUp:
        left_move_up()
    elif leftMovingDown:
        left_move_down()
    if rightMovingUp:
        right_move_up()
    elif rightMovingDown:
        right_move_down()
    if leftx <= ballx <= leftx + paddle_width and lefty <= bally <= lefty + paddle_height:  # kolizia s lavou paddle
        print('left')
        if leftx + paddle_width - speed < ballx: # lava paddle zprava
            direction = ball_movement(direction, 1)
            print('left 1')
        elif bally < lefty + speed:  # lava paddle zhora
            direction = ball_movement(direction, 2)
            print('left 2')
        elif lefty + paddle_height - speed < bally:  # lava paddle zdola
                # and leftx <= ballx - speed:
            direction = ball_movement(direction, 3)
            print('left 3')
    elif rightx <= ballx <= rightx + paddle_width and righty <= bally <= righty + paddle_height: # kolizia s pravou paddle
        print('right')
        if ballx < rightx + speed:  # prava paddle zlava
            direction = ball_movement(direction, 4)
            print('right 4')
        elif bally < righty + speed:  # prava paddle zhora
            direction = ball_movement(direction, 5)
            print('right 5')
        elif righty + paddle_height - speed < bally:  # prava paddle zdola
            # and ballx <= rightx + paddle_width:
            direction = ball_movement(direction, 6)
            print('right 6')
    screen.blit(ball, (ballx, bally))
    screen.blit(leftpaddle, (leftx, lefty))
    screen.blit(rightpaddle, (rightx, righty))
    pygame.display.update()
    fpsClock.tick(FPS)
