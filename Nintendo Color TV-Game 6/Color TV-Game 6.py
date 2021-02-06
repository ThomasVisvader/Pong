import sys
import pygame.freetype
import pygame
import random
import ctypes
import math
import time
from pygame.locals import *


def left_score():
    global left_points, ballMoving, ball_speed, dirchoice, scored, leftMoving, ballSpawning
    left_points += 1
    ballMoving = False
    ball.center = (width + 50, 300)
    dirchoice = 1
    scored = True
    leftMoving = False
    ballSpawning = True
    score_sound.play()


def right_score():
    global right_points, ballMoving, ball_speed, dirchoice, scored, leftMoving, ballSpawning
    right_points += 1
    ballMoving = False
    ball.center = (-50, 300)
    dirchoice = 0
    score_sound.play()
    leftMoving = True
    ballSpawning = True
    scored = True


def paddle_collision(ball, paddle):
    global vx, vy, ball_speed, direction, leftMoving, game
    alpha = 50
    c_point = ball.center[1] - paddle.center[1]
    c_point = c_point / (paddle_height / 2)
    if c_point < -1:
        ball.bottom = paddle.top
        c_point = -1
    elif c_point > 1:
        ball.top = paddle.bottom
        c_point = 1
    angle = c_point * alpha
    if paddle == left_paddle or paddle == left_paddle2:
        if c_point != -1 and c_point != 1:
            ball.left = paddle.right
        if angle < 0:
            direction = 360 + angle
        else:
            direction = angle
        leftMoving = False
        if game != 3:
            pygame.mouse.set_pos([width / 2, right_paddle.y])
    else:
        if c_point != -1 and c_point != 1:
            ball.right = paddle.left
        if angle == 0:
            direction = 180
        else:
            direction = 180 - angle
        leftMoving = True
        if game != 3:
            pygame.mouse.set_pos([width / 2, left_paddle.y])
    if 181 <= direction <= 185:
        direction = 180
    elif 355 <= direction <= 359:
        direction = 0
    vx = ball_speed * math.cos(math.radians(direction))
    vy = ball_speed * math.sin(math.radians(direction))
    ball.x += vx
    ball.y += vy
    paddle_hit_sound.play()
    return ball


def ball_movement(ball):
    global vx, vy, ballSpawning, game
    if ball.right >= 1280:
        left_score()
    elif ball.left <= 0:
        right_score()
    elif ballSpawning and 300 <= ball.centerx <= 800:
        ballSpawning = False
    else:
        if ball.top <= 85:
            ball.top = 85
            vy *= -1
            wall_hit_sound.play()
        elif ball.bottom >= 855:
            ball.bottom = 855
            vy *= -1
            wall_hit_sound.play()
        elif game == 2:
            if ball.left <= 30 and not 210 <= ball.top <= 750 - ball_height:
                ball.left = 30
                vx *= -1
                wall_hit_sound.play()
            elif ball.right >= width - 30 and not 210 <= ball.top <= 750 - ball_height:
                ball.right = width - 30
                vx *= -1
                wall_hit_sound.play()
        elif game == 3 and ball.left <= 30:
            ball.left = 30
            vx *= -1
            wall_hit_sound.play()
        ball.x += vx * dt
        ball.y += vy * dt
    return ball


def move_up(paddle):
    if paddle.top <= -70:
        paddle.top = -70
        return paddle
    paddle.y -= paddle_speed * dt
    return paddle


def move_down(paddle):
    if paddle.bottom >= height + 70:
        paddle.bottom = height + 70
        return paddle
    paddle.y += paddle_speed * dt
    return paddle


def draw_net():
    for i in range(6):
        pygame.draw.rect(screen, TENNISNET, (485, 35 + (i * 130), 30, 65))


def draw_walls():
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, width, 20))
    pygame.draw.rect(screen, (255, 255, 255), (0, height-20, width, 20))
    color_walls(215, 175, 59)
    pygame.draw.rect(screen, TENNISGREEN, (0, 20, 8, height - 40))
    pygame.draw.rect(screen, TENNISRED, (width - 8, 20, 8, height - 40))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, 2))
    pygame.draw.rect(screen, (0, 0, 0), (0, height - 2, width, 2))


def color_walls(r, g, b):
    pixel = 0
    for i in range(100):
        if i % 3 == 0:
            g += 1
        if i % 5 == 0:
            b += 1
        pygame.draw.rect(screen, (r, g, b), (pixel, 0, 1, 20))
        pygame.draw.rect(screen, (r, g, b), (pixel, height - 20, 1, 20))
        pixel += 1
    for i in range(900):
        pygame.draw.rect(screen, (r, g, b), (pixel, 0, 1, 20))
        pygame.draw.rect(screen, (r, g, b), (pixel, height - 20, 1, 20))
        pixel += 1


def draw_hockey_walls():
    for i in range(96):
        if 21 <= i < 75:
            continue
        pygame.draw.rect(screen, (255, 255, 255), (0, i*10, 30, 8))
        pygame.draw.rect(screen, (0, 0, 0), (0, (i * 10) + 8, 30, 2))
        pygame.draw.rect(screen, (255, 255, 255), (width - 30, i * 10, 30, 8))
        pygame.draw.rect(screen, (0, 0, 0), (width - 30, (i * 10) + 8, 30, 2))


def draw_handball_wall():
    for i in range(96):
        pygame.draw.rect(screen, (255, 255, 255), (0, i*10, 30, 8))
        pygame.draw.rect(screen, (0, 0, 0), (0, (i * 10) + 8, 30, 2))


def make_score():
    score_screen.fill(TENNISORANGE)
    if left_points < 10:
        if left_points == 1:
            scoreFont.render_to(score_screen, (144, 0), str(left_points), fgcolor=TENNISSCORE)
        else:
            scoreFont.render_to(score_screen, (70, 0), str(left_points), fgcolor=TENNISSCORE)
    else:
        scoreFont.render_to(score_screen, (30, 0), 'l', fgcolor=TENNISSCORE)
        if left_points - 10 == 1:
            scoreFont.render_to(score_screen, (144, 0), str(left_points - 10), fgcolor=TENNISSCORE)
        else:
            scoreFont.render_to(score_screen, (70, 0), str(left_points - 10), fgcolor=TENNISSCORE)
    if right_points < 10:
        if right_points == 1:
            scoreFont.render_to(score_screen, (844, 0), str(right_points), fgcolor=TENNISSCORE)
        else:
            scoreFont.render_to(score_screen, (770, 0), str(right_points), fgcolor=TENNISSCORE)
    else:
        scoreFont.render_to(score_screen, (728, 0), 'l', fgcolor=TENNISSCORE)
        if right_points - 10 == 1:
            scoreFont.render_to(score_screen, (844, 0), str(right_points - 10), fgcolor=TENNISSCORE)
        else:
            scoreFont.render_to(score_screen, (770, 0), str(right_points - 10), fgcolor=TENNISSCORE)
    write_score()


def write_score():
    global game
    if game == 3:
        handball_screen.blit(score_screen, (0, 0))
        pygame.draw.rect(handball_screen, (0, 0, 0), (724, 0, 200, 200))
        screen.blit(handball_screen, (50, 32))
    else:
        screen.blit(score_screen, (50, 100))


def new_game(type):
    screen.fill((0, 0, 0))
    global left_points, right_points, leftMovingUp, leftMovingDown, rightMovingUp, rightMovingDown, \
        gameStarted, ball, ballTimer, ballMoving, dirchoice, leftMoving
    if type == 0:
        gameStarted = False
    dirchoice = random.choice([0, 1])
    if dirchoice == 0:
        leftMoving = True
    else:
        leftMoving = False
    ball.center = (ballx, bally)
    left_points = 0
    right_points = 0
    ballTimer = 0
    leftMovingUp = False
    leftMovingDown = False
    rightMovingUp = False
    rightMovingDown = False
    ballMoving = False
    if type == 1:
        gameStarted = True


def tennis():
    display.fill(TENNISBLUE)
    global scored, scoreTime, ballMoving, ballTimer, ball, vx, vy, left_paddle, right_paddle, controls, \
        leftMovingUp, leftMovingDown, rightMovingUp, rightMovingDown, gameStarted, ballSpawning, rightx, \
        left_paddle2, right_paddle2
    right_paddle.x = rightx
    if controls == 'Key':
        if leftMovingUp and not leftMovingDown:
            left_paddle = move_up(left_paddle)
        elif leftMovingDown and not leftMovingUp:
            left_paddle = move_down(left_paddle)
        if rightMovingUp and not rightMovingDown:
            right_paddle = move_up(right_paddle)
        elif rightMovingDown and not rightMovingUp:
            right_paddle = move_down(right_paddle)
    left_paddle2.y = left_paddle.y
    right_paddle2.y = right_paddle.y
    if gameStarted and not ballSpawning and ball.colliderect(left_paddle):
        ball = paddle_collision(ball, left_paddle)
    elif gameStarted and not ballSpawning and ball.colliderect(right_paddle):
        ball = paddle_collision(ball, right_paddle)
    if doubles:
        if gameStarted and not ballSpawning and ball.colliderect(left_paddle2):
            ball = paddle_collision(ball, left_paddle2)
        elif gameStarted and not ballSpawning and ball.colliderect(right_paddle2):
            ball = paddle_collision(ball, right_paddle2)
    if scored:
        scored = False
        if gameStarted:
            make_score()
        scoreTime = time.time()
        if left_points == 15 or right_points == 15:
            new_game(0)
    if gameStarted and not ballMoving:
        write_score()
        ballTimer = time.time() - scoreTime
    draw_walls()
    draw_net()
    display.blit(screen, (140, 65))
    pygame.draw.rect(display, TENNISPADDLES, left_paddle)
    pygame.draw.rect(display, TENNISPADDLES, right_paddle)
    if doubles:
        pygame.draw.rect(display, TENNISPADDLES, left_paddle2)
        pygame.draw.rect(display, TENNISPADDLES, right_paddle2)


def hockey():
    global scored, gameStarted, scoreTime, ball, controls, left_paddle, right_paddle, left_paddle2, right_paddle2
    display.fill((0, 255, 0))
    controls = 'Key'
    left_paddle2.y = left_paddle.y
    right_paddle2.y = right_paddle.y
    right_paddle.x = rightx
    if controls == 'Key':
        if leftMovingUp and not leftMovingDown:
            left_paddle = move_up(left_paddle)
            left_paddle2 = move_up(left_paddle2)
        elif leftMovingDown and not leftMovingUp:
            left_paddle = move_down(left_paddle)
            left_paddle2 = move_down(left_paddle2)
        if rightMovingUp and not rightMovingDown:
            right_paddle = move_up(right_paddle)
            right_paddle2 = move_up(right_paddle2)
        elif rightMovingDown and not rightMovingUp:
            right_paddle = move_down(right_paddle)
            right_paddle2 = move_down(right_paddle2)
    if gameStarted and not ballSpawning:
        if ball.colliderect(left_paddle):
            ball = paddle_collision(ball, left_paddle)
        elif ball.colliderect(left_paddle2):
            ball = paddle_collision(ball, left_paddle2)
        elif ball.colliderect(right_paddle):
            ball = paddle_collision(ball, right_paddle)
        elif ball.colliderect(right_paddle2):
            ball = paddle_collision(ball, right_paddle2)
    if scored:
        scored = False
        if gameStarted:
            make_score()
        scoreTime = time.time()
        if left_points == 15 or right_points == 15:
            new_game(0)
    draw_walls()
    draw_hockey_walls()
    draw_net()
    pygame.draw.rect(screen, (255, 255, 255), left_paddle)
    pygame.draw.rect(screen, (255, 255, 255), right_paddle)
    pygame.draw.rect(screen, (255, 255, 255), left_paddle2)
    pygame.draw.rect(screen, (255, 255, 255), right_paddle2)


def handball():
    global controls, rightMovingUp, rightMovingDown, right_paddle, scored, gameStarted, scoreTime, leftMoving, ball
    right_paddle.x = 925
    leftMoving = False
    if controls == 'Key':
        if rightMovingUp and not rightMovingDown:
            right_paddle = move_up(right_paddle)
        elif rightMovingDown and not rightMovingUp:
            right_paddle = move_down(right_paddle)
    if gameStarted and not ballSpawning and ball.colliderect(right_paddle):
        ball = paddle_collision(ball, right_paddle)
    if scored:
        scored = False
        if gameStarted:
            make_score()
        scoreTime = time.time()
        if left_points == 15 or right_points == 15:
            new_game(0)
    # write_score()
    draw_handball_wall()
    draw_walls()
    pygame.draw.rect(screen, (255, 255, 255), right_paddle)


pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
height = 810
width = 1000
display = pygame.display.set_mode((1280, 960))
display.fill((45, 97, 121))
screen = pygame.Surface((width, height))
score_screen = pygame.Surface((900, 255))
handball_screen = pygame.Surface((width, 255))
pygame.display.set_caption('Color TV-Game 6')
scoreFont = pygame.freetype.Font('text/nintendo.ttf', 132)
wall_hit_sound = pygame.mixer.Sound('sounds/wallhit.wav')
score_sound = pygame.mixer.Sound('sounds/score.wav')
paddle_hit_sound = pygame.mixer.Sound('sounds/paddlehit.wav')

FPS = 60
fpsClock = pygame.time.Clock()

paddle_height = 130
paddle_width = 30
ball_height = 20
ball_width = 26
leftx = 190
lefty = height // 2
rightx = 1090 - paddle_width
righty = height // 2
ballx = -50
bally = -50
paddle_speed = 20.0
ball_speed = 15.0

TENNISORANGE = (129, 102, 0)
TENNISBLUE = (45, 97, 121)
TENNISNET = (203, 173, 35)
TENNISSCORE = (199, 180, 198)
TENNISGREEN = (61, 211, 0)
TENNISRED = (138, 18, 66)
TENNISPADDLES = (163, 192, 68)

topWall = pygame.Rect(0, 0, width, 12)
bottomWall = pygame.Rect(0, height-12, width, 12)
ball = pygame.Rect(ballx, bally, ball_width, ball_height)
left_paddle = pygame.Rect(leftx, lefty, paddle_width, paddle_height)
left_paddle2 = pygame.Rect(leftx + 285, lefty, paddle_width, left_paddle.height)
right_paddle = pygame.Rect(rightx, righty, paddle_width, paddle_height)
right_paddle2 = pygame.Rect(rightx - 285, righty, paddle_width, right_paddle.height)


left_points = 10
right_points = 10
ballTimer = 0
scoreTimer = 0
dt = 0
game = 1
blinkTime = time.time()

controls = 'Mouse'
leftMovingUp = False
leftMovingDown = False
rightMovingUp = False
rightMovingDown = False
ballMoving = False
scored = False
gameStarted = False
ballSpawning = False
doubles = False
blink = True

make_score()
dirchoice = random.choice([0, 1])
if dirchoice == 0:
    leftMoving = True
else:
    leftMoving = False

pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.mouse.set_pos([0, 0])
scoreTime = time.time()
lastTime = time.time()
while True:
    dt = time.time() - lastTime
    dt *= FPS
    lastTime = time.time()
    screen.fill(TENNISORANGE)
    if not gameStarted:
        draw_walls()
        if scoreTimer >= (32/60):
            blink = not blink
            blinkTime = time.time()
        if blink:
            write_score()
        draw_net()
        display.blit(screen, (140, 65))
        pygame.draw.rect(display, TENNISPADDLES, left_paddle)
        pygame.draw.rect(display, TENNISPADDLES, right_paddle)
        scoreTimer = time.time() - blinkTime
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    gameStarted = True
                    make_score()
                    scoreTime = time.time()
                elif event.key == K_LSHIFT:
                    if controls == 'Mouse':
                        controls = 'Key'
                    else:
                        controls = 'Mouse'
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_LSHIFT:
                if controls == 'Mouse':
                    controls = 'Key'
                else:
                    controls = 'Mouse'
            elif event.type == KEYUP and event.key == K_SPACE:
                new_game(1)
                scoreTime = time.time()
                make_score()
            elif event.type == KEYUP and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_KP1:
                game = 1
            elif event.type == KEYUP and event.key == K_KP2:
                game = 2
            elif event.type == KEYUP and event.key == K_KP3:
                game = 3
            elif event.type == KEYUP and event.key == K_LALT:
                if ball_speed == 15.0:
                    ball_speed = 25.0
                else:
                    ball_speed = 15.0
            elif event.type == KEYUP and event.key == K_RALT:
                doubles = not doubles
            elif event.type == KEYUP and event.key == K_LCTRL:
                if left_paddle.height == 130:
                    left_paddle = pygame.Rect(leftx, pygame.mouse.get_pos()[1] + 65, paddle_width, 65)
                else:
                    left_paddle = pygame.Rect(leftx, pygame.mouse.get_pos()[1] - 65, paddle_width, 130)
                if doubles:
                    left_paddle2.height = left_paddle.height
                pygame.mouse.set_pos([width / 2, left_paddle.y])
            elif event.type == KEYUP and event.key == K_RCTRL:
                if right_paddle.height == 130:
                    right_paddle = pygame.Rect(rightx, pygame.mouse.get_pos()[1] + 65, paddle_width, 65)
                else:
                    right_paddle = pygame.Rect(rightx, pygame.mouse.get_pos()[1] - 65, paddle_width, 130)
                if doubles:
                    right_paddle2.height = right_paddle.height
                pygame.mouse.set_pos([width / 2, right_paddle.y])
            if controls == 'Mouse':
                if event.type == MOUSEMOTION:
                    position = pygame.mouse.get_pos()
                    pygame.mouse.set_pos(width / 2, position[1])
                    if leftMoving:
                        left_paddle.y = position[1]
                    else:
                        right_paddle.y = position[1]
            elif controls == 'Key':
                if event.type == KEYUP:
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
        if not ballMoving and ballTimer >= (130/60):
            ballMoving = True
            ball.y = random.randint(66, height-84)
            if dirchoice == 0:
                ball.x = rightx
                quadrant = random.choice([2, 3])
                if quadrant == 2:
                    direction = random.randint(91, 180)
                else:
                    direction = random.randint(186, 269)
            else:
                ball.x = leftx
                quadrant = random.choice([1, 4])
                if quadrant == 1:
                    direction = random.randint(0, 84)
                else:
                    direction = random.randint(276, 354)
            vx = ball_speed * math.cos(math.radians(direction))
            vy = ball_speed * math.sin(math.radians(direction))
            ballTimer = 0
        if ballMoving:
            ball = ball_movement(ball)
        if game == 1:
            tennis()
        elif game == 2:
            hockey()
        else:
            handball()
        if not ballMoving:
            ballTimer = time.time() - scoreTime
        else:
            pygame.draw.rect(display, (203, 173, 35), ball)
    pygame.display.update()
    fpsClock.tick(FPS)
