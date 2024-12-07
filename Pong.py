import sys
import pygame
import random
import math
from pygame.locals import *

def start():
    angle = random.randrange(0, 360)
    return math.radians(angle)

def left_score():
    global left_points, ballx, bally, ballMoving
    left_points += 1
    ballx = width // 2
    bally = height // 2
    ballMoving = False

def right_score():
    global right_points, ballx, bally, ballMoving
    right_points += 1
    ballx = width // 2
    bally = height // 2
    ballMoving = False

def ball_collision(direction):
    return direction + math.pi

def ball_movement(direction):
    global ballx, bally
    if bally >= height - ballsize or bally <= 0:
        direction = ball_collision(direction)
    elif ballx >= width - ballsize:
        left_score()
    elif ballx <= 0:
        right_score()

    ballx += 5 * math.sin(direction)
    bally -= 5 * math.cos(direction)
    return direction

def left_move_up():
    global lefty
    lefty = max(0, lefty - 5)

def left_move_down():
    global lefty
    lefty = min(height - paddle_height, lefty + 5)

def right_move_up():
    global righty
    righty = max(0, righty - 5)

def right_move_down():
    global righty
    righty = min(height - paddle_height, righty + 5)

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
lefty = height // 2 - paddle_height // 2
rightx = width - 140 - paddle_width
righty = height // 2 - paddle_height // 2
ballx = width // 2
bally = height // 2

left_points = 0
right_points = 0

leftMovingUp = False
leftMovingDown = False
rightMovingUp = False
rightMovingDown = False
ballMoving = False
direction = 0

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            print(f'Left: {left_points}, Right: {right_points}')
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
        direction = ball_movement(direction)
    if leftMovingUp:
        left_move_up()
    elif leftMovingDown:
        left_move_down()
    if rightMovingUp:
        right_move_up()
    elif rightMovingDown:
        right_move_down()

    if (leftx < ballx <= leftx + paddle_width and lefty < bally <= lefty + paddle_height) or \
       (rightx < ballx <= rightx + paddle_width and righty < bally <= righty + paddle_height):
        direction = ball_collision(direction)

    screen.blit(ball, (ballx, bally))
    screen.blit(leftpaddle, (leftx, lefty))
    screen.blit(rightpaddle, (rightx, righty))
    pygame.display.update()
    fpsClock.tick(FPS)
