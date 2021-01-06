import sys
import pygame.freetype
import pygame
import random
from pygame.locals import *


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


def ball_movement(ball, collision):
    global ballx, bally
    if ball.right >= width:
        left_score()
        ball.x = ballx
        ball.y = bally
    elif ball.left <= 0:
        right_score()
        ball.x = ballx
        ball.y = bally
    else:
        if collision == 0:  # odraz od steny
            if ball.top <= 0 or ball.bottom >= height:
                bally *= -1
        elif collision == 1:  # kolizia s paddle zboku
            ballx *= -1
        ball.x += ballx * speed
        ball.y -= bally * speed
    return ball


def move_up(paddle):
    if paddle.top <= 0:
        return paddle
    paddle.y -= 5
    return paddle


def move_down(paddle):
    if paddle.bottom >= height:
        return paddle
    paddle.y += 5
    return paddle


pygame.init()
height = 795
width = 1535
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')
font = pygame.freetype.Font('text/Cone.ttf', 150)

FPS = 60
fpsClock = pygame.time.Clock()

paddle_height = 55
paddle_width = 41
ballsize = 19
leftx = 140
lefty = 370
rightx = 1354
righty = 370
ballx = 758
bally = 388
speed = 10

ball = pygame.Rect(ballx, bally, ballsize, ballsize)
left_paddle = pygame.Rect(leftx, lefty, paddle_width, paddle_height)
right_paddle = pygame.Rect(rightx, righty, paddle_width, paddle_height)

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
            if not ballMoving:
                ballMoving = True
                ballx = random.uniform(-1.0, 1.0)
                bally = random.uniform(-1.0, 1.0)
    if ballMoving:
        ball = ball_movement(ball, 0)
    if leftMovingUp and not leftMovingDown:
        left_paddle = move_up(left_paddle)
    elif leftMovingDown and not leftMovingUp:
        left_paddle = move_down(left_paddle)
    if rightMovingUp and not rightMovingDown:
        right_paddle = move_up(right_paddle)
    elif rightMovingDown and not rightMovingUp:
        right_paddle = move_down(right_paddle)
    if ball.colliderect(left_paddle):
        ball = ball_movement(ball, 1)
    elif ball.colliderect(right_paddle):
        ball = ball_movement(ball, 1)
    pygame.draw.rect(screen, (0, 153, 51), left_paddle)
    pygame.draw.rect(screen, (153, 51, 153), right_paddle)
    pygame.draw.rect(screen, (0, 0, 255), ball)
    if not ballMoving:
        font.render_to(screen, (700, 200), str(left_points), fgcolor=(0, 153, 51))
        font.render_to(screen, (835, 200), str(right_points), fgcolor=(153, 51, 153))
    pygame.display.update()
    fpsClock.tick(FPS)
