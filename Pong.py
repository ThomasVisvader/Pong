import sys
import pygame
import random
import math
from pygame.locals import *


def start():
    angle = random.randrange(0, 360)
    dir = math.radians(angle)
    return dir


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


def ball_collision(direction):
    direction += math.radians(90)
    return direction


def ball_movement(direction, collision):
    global ballx, bally
    if collision or bally >= height-ballsize or bally <= 0:
        direction = ball_collision(direction)
        ballx = ballx + (5 * math.sin(direction))
        bally = bally - (5 * math.cos(direction))
    elif ballx >= width-ballsize:
        left_score()
    elif ballx <= 0:
        right_score()
    else:
        ballx = ballx + (5 * math.sin(direction))
        bally = bally - (5 * math.cos(direction))
    return direction


def left_move_up():
    global lefty
    if lefty <= 0:
        return
    lefty -= 5


def left_move_down():
    global lefty
    if lefty >= 740:
        return
    lefty += 5


def right_move_up():
    global righty
    if righty <= 0:
        return
    righty -= 5


def right_move_down():
    global righty
    if righty >= 740:
        return
    righty += 5


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
    if leftx < ballx <= leftx+paddle_width and lefty < bally <= lefty+paddle_height or \
            rightx < ballx <= rightx+paddle_width and righty < bally <= righty+paddle_height:
        direction = ball_movement(direction, 1)
    screen.blit(ball, (ballx, bally))
    screen.blit(leftpaddle, (leftx, lefty))
    screen.blit(rightpaddle, (rightx, righty))
    pygame.display.update()
    fpsClock.tick(FPS)
