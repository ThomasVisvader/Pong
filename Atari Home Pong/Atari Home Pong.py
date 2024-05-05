import sys
import os
import pygame.freetype
import pygame
import random
import heapq
import ctypes
import math
import time
from pygame.locals import *


def left_score():
    global left_points, ballMoving, ball_speed, dirchoice, scored, leftMoving, volley
    left_points += 1
    ballMoving = False
    ball_speed = 7.5
    ball.center = (width + 50, 300)
    dirchoice = 1
    scored = True
    leftMoving = False
    volley = 1
    score_sound.play()


def right_score():
    global right_points, ballMoving, ball_speed, dirchoice, scored, leftMoving, volley
    right_points += 1
    ballMoving = False
    ball_speed = 7.5
    ball.center = (-50, 300)
    dirchoice = 0
    score_sound.play()
    scored = True
    volley = 1
    leftMoving = True


def paddle_collision(ball, paddle):
    global vx, vy, ball_speed, direction, leftMoving, volley
    c_point = ball.center[1] - paddle.center[1]
    c_point = c_point / (paddle_height / 2)
    if c_point < -1:
        ball.bottom = paddle.top
        c_point = -1
    elif c_point > 1:
        ball.top = paddle.bottom
        c_point = 1
    volley += 1
    if 1 <= volley <= 4:
        alpha = 30
        inc = 15
    elif 5 <= volley <= 8:
        if paddle == left_paddle:
            vx = -15.0
        else:
            vx = 15.0
        ball_speed = 15.0
        alpha = 25
        inc = 10
    else:
        if paddle == left_paddle:
            vx = -22.5
        else:
            vx = 22.5
        ball_speed = 22.5
        alpha = 10
        inc = 10
    if paddle == left_paddle:
        leftMoving = False
        pygame.mouse.set_pos([width / 2, right_paddle.y])
        straight = 360
    else:
        leftMoving = True
        pygame.mouse.set_pos([width / 2, left_paddle.y])
        straight = 180
        alpha *= -1
        inc *= -1
    if -0.25 < c_point < 0.25:
        direction = straight
    elif -0.5 <= c_point <= -0.25:
        direction = straight - alpha
    elif -0.75 <= c_point < -0.5:
        direction = straight - alpha - inc
    elif -1 <= c_point < -0.75:
        direction = straight - alpha - (2 * inc)
    elif 0.25 <= c_point <= 0.5:
        direction = straight + alpha
    elif 0.5 < c_point <= 0.75:
        direction = straight + alpha + inc
    elif 0.75 < c_point <= 1:
        direction = straight + alpha + (2 * inc)
    vx *= -1
    vy = math.tan(math.radians(direction)) * vx
    ball.x += vx * dt
    ball.y += vy * dt
    hit_sound.play()
    return ball


def ball_movement(ball):
    global vx, vy
    if ball.right >= width:
        left_score()
    elif ball.left <= 0:
        right_score()
    else:
        if ball.top <= 65:
            ball.top = 65
            vy *= -1
            hit_sound.play()
        elif ball.bottom >= height - 65:
            ball.bottom = height - 65
            vy *= -1
            hit_sound.play()
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
    red, green, blue = hsl_to_rgb(192, 0.95, 0.5)
    for i in range(15):
        pygame.draw.rect(screen, (red, green, blue), (623, i * 68, 3, 34))
    pixel = 0
    for h in range(193, 199, 2):
        red, green, blue = hsl_to_rgb(h, 0.95, 0.5)
        for i in range(15):
            pygame.draw.rect(screen, (red, green, blue), (625 + pixel, i * 68, 4, 34))
        pixel += 4
        red, green, blue = hsl_to_rgb(h + 1, 0.95, 0.5)
        for i in range(15):
            pygame.draw.rect(screen, (red, green, blue), (625 + pixel, i * 68, 5, 34))
        pixel += 5


def background():
    count = 0
    pixel = 0
    for h in range(54, 338, 2):
        red, green, blue = hsl_to_rgb(h, 0.13, 0.5)
        pygame.draw.rect(screen, (red, green, blue), (pixel, 0, 4, 65))
        pygame.draw.rect(screen, (red, green, blue), (pixel, height-65, 4, 65))
        pixel += 4
        red, green, blue = hsl_to_rgb(h + 1, 0.13, 0.5)
        pygame.draw.rect(screen, (red, green, blue), (pixel, 0, 5, 65))
        pygame.draw.rect(screen, (red, green, blue), (pixel, height - 65, 5, 65))
        pixel += 5
        count += 2
    red, green, blue = hsl_to_rgb(334, 0.13, 0.5)
    pygame.draw.rect(screen, (red, green, blue), (pixel, 0, 2, 65))
    pygame.draw.rect(screen, (red, green, blue), (pixel, height - 65, 2, 65))
    draw_net()


def rgb_to_hsl(red, green, blue):
    r = red / 255
    g = green / 255
    b = blue / 255
    heap = [r, g, b]
    heapq.heapify(heap)
    min = heap[0]
    max = heap[2]
    delta = max - min
    h = 0
    if delta == 0:
        h = 0
    elif max == r:
        h = (60 * ((g - b) / delta) + 360) % 360
    elif max == g:
        h = (60 * ((b - r) / delta) + 120) % 360
    elif max == b:
        h = (60 * ((r - g) / delta) + 240) % 360
    return h


def hsl_to_rgb(h, s, l):
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c/2
    r, g, b = 0, 0, 0
    if 0 <= h < 60:
        r = c
        g = x
        b = 0
    elif 60 <= h < 120:
        r = x
        g = c
        b = 0
    elif 120 <= h < 180:
        r = 0
        g = c
        b = x
    elif 180 <= h < 240:
        r = 0
        g = x
        b = c
    elif 240 <= h < 300:
        r = x
        g = 0
        b = c
    elif 300 <= h < 360:
        r = c
        g = 0
        b = x
    red = (r + m) * 255
    green = (g + m) * 255
    blue = (b + m) * 255
    return red, green, blue


def color(obj):
    x = obj.x
    y = obj.y
    width = obj.width
    height = obj.height
    block = x // 9
    offset = x % 9
    h = 54 + block * 2
    if offset < 4:
        count = 4 - offset
        width -= count
        red, green, blue = hsl_to_rgb(h, 0.95, 0.5)
        pygame.draw.rect(screen, (red, green, blue), (x, y, count, height))
        x += count
        h += 1
        red, green, blue = hsl_to_rgb(h, 0.95, 0.5)
        pygame.draw.rect(screen, (red, green, blue), (x, y, 5, height))
        x += 5
        width -= 5
    else:
        h += 1
        count = 10 - offset
        red, green, blue = hsl_to_rgb(h, 0.95, 0.5)
        pygame.draw.rect(screen, (red, green, blue), (x, y, count, height))
        x += count
        width -= count
    h += 1
    count = width // 9
    for i in range(count):
        red, green, blue = hsl_to_rgb(h, 0.95, 0.5)
        pygame.draw.rect(screen, (red, green, blue), (x, y, 4, height))
        x += 4
        h += 1
        red, green, blue = hsl_to_rgb(h, 0.95, 0.5)
        pygame.draw.rect(screen, (red, green, blue), (x, y, 5, height))
        x += 5
        h += 1
    rest = width % 9
    if rest == 0:
        return
    elif rest < 4:
        red, green, blue = hsl_to_rgb(h, 0.95, 0.5)
        pygame.draw.rect(screen, (red, green, blue), (x, y, rest, height))
    else:
        red, green, blue = hsl_to_rgb(h, 0.95, 0.5)
        pygame.draw.rect(screen, (red, green, blue), (x, y, 4, height))
        x += 4
        h += 1
        rest -= 4
        red, green, blue = hsl_to_rgb(h, 0.95, 0.5)
        pygame.draw.rect(screen, (red, green, blue), (x, y, rest, height))
        x += 5


def make_score():
    score_screen.fill((0, 0, 0))
    if left_points < 10:
        if left_points == 1:
            scoreFont.render_to(score_screen, (365, 0), str(left_points), fgcolor=(255, 255, 255))
            color_score(365, 0)
        else:
            scoreFont.render_to(score_screen, (260, 0), str(left_points), fgcolor=(255, 255, 255))
            color_score(260, 0)
    else:
        scoreFont.render_to(score_screen, (140, 0), '1', fgcolor=(255, 255, 255))
        color_score(140, 0)
        if left_points - 10 == 1:
            scoreFont.render_to(score_screen, (365, 0), str(left_points - 10), fgcolor=(255, 255, 255))
            color_score(365, 0)
        else:
            scoreFont.render_to(score_screen, (260, 0), str(left_points - 10), fgcolor=(255, 255, 255))
            color_score(260, 0)
    if right_points < 10:
        if right_points == 1:
            scoreFont.render_to(score_screen, (1085, 0), str(right_points), fgcolor=(255, 255, 255))
            color_score(1085, 0)
        else:
            scoreFont.render_to(score_screen, (980, 0), str(right_points), fgcolor=(255, 255, 255))
            color_score(980, 0)
    else:
        scoreFont.render_to(score_screen, (860, 0), '1', fgcolor=(255, 255, 255))
        color_score(860, 0)
        if right_points - 10 == 1:
            scoreFont.render_to(score_screen, (1085, 0), str(right_points - 10), fgcolor=(255, 255, 255))
            color_score(1085, 0)
        else:
            scoreFont.render_to(score_screen, (980, 0), str(right_points - 10), fgcolor=(255, 255, 255))
            color_score(980, 0)
    write_score()


def write_score():
    screen.blit(score_screen, (0, 140))


def color_score(x, y):
    p = pygame.PixelArray(score_screen)
    for j in range(y, y + 253):
        for i in range(x, x + 145):
            if p[i][j] == score_screen.map_rgb((255, 255, 255)):
                red, green, blue = get_pixel_color(i)
                p[i][j] = (red, green, blue)
    del p
    return 0


def get_pixel_color(x):
    block = x // 9
    offset = x % 9
    h = 54 + block * 2
    if offset >= 4:
        h += 1
    red, green, blue = hsl_to_rgb(h, 0.95, 0.5)
    return red, green, blue


def new_game(type):
    screen.fill((0, 0, 0))
    global left_points, right_points, leftMovingUp, leftMovingDown, rightMovingUp, rightMovingDown, \
        gameStarted, ball, ballTimer, ballMoving, leftMoving, dirchoice, volley, ball_speed
    if type == 0:
        gameStarted = False
    ball.center = (ballx, bally)
    ball_speed = 7.5
    volley = 1
    left_points = 0
    right_points = 0
    ballTimer = 0
    leftMovingUp = False
    leftMovingDown = False
    rightMovingUp = False
    rightMovingDown = False
    ballMoving = False
    if leftMoving:
        dirchoice = 0
    else:
        dirchoice = 1


def intro(yspeed):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, 140))
    pygame.draw.rect(screen, (0, 0, 0), (0, 390, width, height - 390))
    background()
    global blockList, introMovingUp
    for blocks in blockList:
        for block in blocks:
            line_animation(block)
            if introMovingUp:
                block.y -= yspeed
            else:
                block.y += yspeed
            block.x += 3
    if (blockList[0][1].y + 110 == height and not introMovingUp) or \
            (blockList[0][1].y == 60 and introMovingUp):
        introMovingUp = bool(random.getrandbits(1))
    screen.blit(score_screen, (0, 140))
    draw_net()


def line_animation(block):
    pygame.draw.rect(screen, (0, 0, 0), block)
    color(block)
    if block.x >= 1650:
        block.x = -60
    if not introMovingUp and block.y >= height + 80:
        block.y = -120
    elif introMovingUp and block.y <= -80:
        block.y = height + 120


pygame.init()
if os.name == 'nt':
    ctypes.windll.user32.SetProcessDPIAware()
height = 960
width = 1280
screen = pygame.display.set_mode((width, height))
score_screen = pygame.Surface((width, 255))
pygame.display.set_caption('Atari Home Pong')
scoreFont = pygame.freetype.Font('text/Cone.ttf', 420)
score_sound = pygame.mixer.Sound('sounds/score.wav')
hit_sound = pygame.mixer.Sound('sounds/hit.wav')
spawn_sound = pygame.mixer.Sound('sounds/spawn.wav')

FPS = 60
fpsClock = pygame.time.Clock()

paddle_height = 70
paddle_width = 30
ballsize = 19
leftx = 100
lefty = height // 2
rightx = width - 100 - paddle_width
righty = height // 2
ballx = width // 2 - 5
bally = height // 2 + 5
paddle_speed = 20.0
ball_speed = 7.5
yspeed = 0
volley = 1

topWall = pygame.Rect(0, 0, width, 65)
bottomWall = pygame.Rect(0, height-65, width, 65)
ball = pygame.Rect(ballx, bally, ballsize, ballsize)
ball.center = (ballx, bally)
left_paddle = pygame.Rect(leftx, lefty, paddle_width, paddle_height)
left_paddle.center = (leftx, lefty)
right_paddle = pygame.Rect(rightx, righty, paddle_width, paddle_height)
right_paddle.center = (rightx, righty)

left_points = 0
right_points = 0
ballTimer = 0
dt = 0

controls = 'Mouse'
leftMovingUp = False
leftMovingDown = False
rightMovingUp = False
rightMovingDown = False
ballMoving = False
gameStarted = False
scored = False

introMovingUp = False
chosen = False

blockList = []
blocks = []
for i in range(14):
    blocks.append(pygame.Rect(i * 120, -60, 60, 60))
    blocks.append(pygame.Rect(i * 120, 80, 60, 110))
    for j in range(6):
        blocks.append(pygame.Rect(i * 120, 270 + (j*140), 60, 60))
    blockList.append(blocks[:])
    blocks.clear()

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
    if not gameStarted:
        if not chosen:
            FPS = random.choice([60, 90, 120, 150])
            yspeed = random.choice([1, 2, 5, 10])
            chosen = True
        else:
            intro(yspeed)
            pygame.draw.rect(screen, (255, 255, 255), left_paddle)
            color(left_paddle)
            pygame.draw.rect(screen, (255, 255, 255), right_paddle)
            color(right_paddle)
            pygame.draw.rect(screen, (255, 255, 255), ball)
            color(ball)
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
    elif gameStarted:
        chosen = False
        FPS = 60
        screen.fill((0, 0, 0))
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
        if not ballMoving and ballTimer >= 2:
            ballMoving = True
            ball.x = ballx
            ball.y = random.randint(66, height-84)
            if dirchoice == 0:
                quadrant = random.choice([2, 3])
                if quadrant == 2:
                    direction = random.randint(125, 180)
                else:
                    direction = random.randint(186, 225)
            else:
                quadrant = random.choice([1, 4])
                if quadrant == 1:
                    direction = random.randint(0, 45)
                else:
                    direction = random.randint(315, 354)
            vx = ball_speed
            if dirchoice == 0:
                vx *= -1
            vy = math.tan(math.radians(direction)) * vx
            spawn_sound.play()
            ballTimer = 0
        if ballMoving:
            ball = ball_movement(ball)
        if controls == 'Key':
            if leftMovingUp and not leftMovingDown:
                left_paddle = move_up(left_paddle)
            elif leftMovingDown and not leftMovingUp:
                left_paddle = move_down(left_paddle)
            if rightMovingUp and not rightMovingDown:
                right_paddle = move_up(right_paddle)
            elif rightMovingDown and not rightMovingUp:
                right_paddle = move_down(right_paddle)
        if ball.colliderect(left_paddle):
            ball = paddle_collision(ball, left_paddle)
        elif ball.colliderect(right_paddle):
            ball = paddle_collision(ball, right_paddle)
        if scored:
            scored = False
            make_score()
            scoreTime = time.time()
            if left_points == 15 or right_points == 15:
                new_game(0)
        if gameStarted and not ballMoving:
            write_score()
            ballTimer = time.time() - scoreTime
        background()
        pygame.draw.rect(screen, (255, 255, 255), left_paddle)
        color(left_paddle)
        pygame.draw.rect(screen, (255, 255, 255), right_paddle)
        color(right_paddle)
        pygame.draw.rect(screen, (255, 255, 255), ball)
        color(ball)
    pygame.display.update()
    fpsClock.tick(FPS)
