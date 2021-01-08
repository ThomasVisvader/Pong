import sys
import pygame.freetype
import pygame
import random
from pygame.locals import *


def left_score():
    global left_points, vx, vy, ballMoving
    left_points += 1
    vx = 758
    vy = 388
    ballMoving = False


def right_score():
    global right_points, vx, vy, ballMoving
    right_points += 1
    vx = 758
    vy = 388
    ballMoving = False


def ball_movement(ball, collision):
    global vx, vy
    if ball.right >= width:
        left_score()
        ball.x = vx
        ball.y = vy
    elif ball.left <= 0:
        right_score()
        ball.x = vx
        ball.y = vy
    else:
        if collision == 0:  # odraz od steny
            if ball.top <= 0:
                ball.y += ball_speed
                vy *= -1
            elif ball.bottom >= height:
                vy *= -1
                ball.y -= ball_speed
        elif collision == 1:  # kolizia s ľavou paddle
            if left_paddle.topright[0] - ball_speed < ball.x < left_paddle.topright[0]:  # biely obdlznik
                if left_paddle.topright[1] + ball_speed < ball.y < left_paddle.bottomright[1] - ball_speed:  # rohy
                    ball.x += ball_speed
                    vx *= -1
                else:  # hore alebo dole
                    if leftMovingUp:
                        # vx *= -1
                        if vy > 0:
                            vy *= -1
                    elif leftMovingDown:
                        # vx *= -1
                        if vy < 0:
                            vy *= -1
                    else:
                        vy *= -1
            else:
                if leftMovingUp:
                    ball.y -= ball_speed
                    # vx *= -1
                    if vy > 0:
                        vy *= -1
                elif leftMovingDown:
                    ball.y += ball_speed
                    # vx *= -1
                    if vy < 0:
                        vy *= -1
        elif collision == 2:  # kolizia s pravou paddle
            if right_paddle.topleft[0] < ball.x < right_paddle.topleft[0] + ball_speed:
                if right_paddle.topleft[1] + ball_speed < ball.y < right_paddle.bottomleft[1] - ball_speed:
                    ball.x -= ball_speed
                    vx *= -1
                else:
                    if rightMovingUp:
                        # vx *= -1
                        if vy > 0:
                            vy *= -1
                    elif rightMovingDown:
                        # vx *= -1
                        if vy < 0:
                            vy *= -1
                    else:
                        vy *= -1
            else:
                if rightMovingUp:
                    ball.y -= ball_speed
                    # vx *= -1
                    if vy > 0:
                        vy *= -1
                elif rightMovingDown:
                    ball.y += ball_speed
                    # vx *= -1
                    if vy < 0:
                        vy *= -1
        ball.x += vx * ball_speed
        ball.y += vy * ball_speed
    return ball


def move_up(paddle):
    if paddle.top <= 0:
        return paddle
    paddle.y -= paddle_speed
    return paddle


def move_down(paddle):
    if paddle.bottom >= height:
        return paddle
    paddle.y += paddle_speed
    return paddle


pygame.init()
height = 795
width = 1535
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')
scoreFont = pygame.freetype.Font('text/pong-score.ttf', 150)
titleFont = pygame.freetype.Font('text/Cone.ttf', 150)
textFont = pygame.freetype.Font('text/Cone.ttf', 25)

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
paddle_speed = 10.0
ball_speed = paddle_speed * 1.5

startButton = pygame.Rect(700, 400, 200, 50)
exitButton = pygame.Rect(700, 500, 200, 50)
pygame.draw.rect(screen, (255, 255, 255), startButton)
pygame.draw.rect(screen, (255, 255, 255), exitButton)
titleFont.render_to(screen, (650, 200), 'PONG', fgcolor=(255, 255, 255))
textFont.render_to(screen, (760, 425), 'Start game', fgcolor=(0, 0, 0))
textFont.render_to(screen, (760, 525), 'Exit game', fgcolor=(0, 0, 0))

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
gameStarted = False

while True:
    if not gameStarted:
        mouse = pygame.mouse.get_pos()
        if startButton.collidepoint(mouse):
            pygame.draw.rect(screen, (128, 128, 128), startButton)
            textFont.render_to(screen, (760, 425), 'Start game', fgcolor=(0, 0, 0))
        else:
            pygame.draw.rect(screen, (255, 255, 255), startButton)
            textFont.render_to(screen, (760, 425), 'Start game', fgcolor=(0, 0, 0))
        if exitButton.collidepoint(mouse):
            pygame.draw.rect(screen, (128, 128, 128), exitButton)
            textFont.render_to(screen, (760, 525), 'Exit game', fgcolor=(0, 0, 0))
        else:
            pygame.draw.rect(screen, (255, 255, 255), exitButton)
            textFont.render_to(screen, (760, 525), 'Exit game', fgcolor=(0, 0, 0))
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if startButton.collidepoint(mouse):
                    gameStarted = True
                elif exitButton.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
    elif gameStarted:
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
                    vx = round(random.uniform(-1.0, 1.0), 2)
                    vy = round(random.uniform(-1.0, 1.0), 2)
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
            ball = ball_movement(ball, 2)
        pygame.draw.rect(screen, (0, 153, 51), left_paddle)
        pygame.draw.rect(screen, (153, 51, 153), right_paddle)
        pygame.draw.rect(screen, (0, 0, 255), ball)
        if not ballMoving:
            scoreFont.render_to(screen, (700, 200), str(left_points), fgcolor=(0, 153, 51))
            scoreFont.render_to(screen, (835, 200), str(right_points), fgcolor=(153, 51, 153))
    if ballMoving:
        textFont.render_to(screen, (100, 30), str(ball.x), fgcolor=(255, 255, 255))
        textFont.render_to(screen, (100, 50), str(ball.y), fgcolor=(255, 255, 255))
        textFont.render_to(screen, (100, 70), str(vx), fgcolor=(255, 255, 255))
        textFont.render_to(screen, (100, 100), str(vy), fgcolor=(255, 255, 255))
    pygame.display.update()
    fpsClock.tick(FPS)
