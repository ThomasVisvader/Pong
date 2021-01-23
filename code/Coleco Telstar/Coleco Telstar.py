import sys
import pygame.freetype
import pygame
import random
import ctypes
import math
import time
from pygame.locals import *


def left_score():
    global left_points, ballMoving, ball_speed, dirchoice, scored
    left_points += 1
    ballMoving = False
    ball_speed = 10.0
    ball.center = (width + 50, 300)
    dirchoice = 1
    scored = True
    score_sound.play()


def right_score():
    global right_points, ballMoving, ball_speed, dirchoice, scored
    right_points += 1
    ballMoving = False
    ball_speed = 10.0
    ball.center = (-50, 300)
    dirchoice = 0
    score_sound.play()
    scored = True


def paddle_collision(ball, paddle):
    global vx, vy, ball_speed, direction, leftMoving
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
    if paddle == left_paddle:
        if c_point != -1 and c_point != 1:
            ball.left = paddle.right
        if angle < 0:
            direction = 360 + angle
        else:
            direction = angle
        leftMoving = False
        pygame.mouse.set_pos([width / 2, right_paddle.y])
    else:
        if c_point != -1 and c_point != 1:
            ball.right = paddle.left
        if angle == 0:
            direction = 180
        else:
            direction = 180 - angle
        leftMoving = True
        pygame.mouse.set_pos([width / 2, left_paddle.y])
    if ball_speed < 22.0:
        ball_speed += 1
    if 181 <= direction <= 185:
        direction = 180
    elif 355 <= direction <= 359:
        direction = 0
    vx = ball_speed * math.cos(math.radians(direction))
    vy = ball_speed * math.sin(math.radians(direction))
    ball.x += vx
    ball.y += vy
    hit_sound.play()
    return ball


def ball_movement(ball):
    global vx, vy
    if ball.right >= width:
        left_score()
    elif ball.left <= 0:
        right_score()
    else:
        if ball.top <= 12:
            ball.top = 12
            vy *= -1
            hit_sound.play()
        elif ball.bottom >= height - 12:
            ball.bottom = height - 12
            vy *= -1
            hit_sound.play()
        ball.x += vx
        ball.y += vy
    return ball


def move_up(paddle):
    if paddle.top <= -70:
        paddle.top = -70
        return paddle
    paddle.y -= paddle_speed
    return paddle


def move_down(paddle):
    if paddle.bottom >= height + 70:
        paddle.bottom = height + 70
        return paddle
    paddle.y += paddle_speed
    return paddle


# def draw_net():
#     red, green, blue = hsl_to_rgb(192, 0.95, 0.5)
#     for i in range(15):
#         pygame.draw.rect(screen, (red, green, blue), (623, i * 68, 3, 34))
#     pixel = 0
#     for h in range(193, 199, 2):
#         red, green, blue = hsl_to_rgb(h, 0.95, 0.5)
#         for i in range(15):
#             pygame.draw.rect(screen, (red, green, blue), (625 + pixel, i * 68, 4, 34))
#         pixel += 4
#         red, green, blue = hsl_to_rgb(h + 1, 0.95, 0.5)
#         for i in range(15):
#             pygame.draw.rect(screen, (red, green, blue), (625 + pixel, i * 68, 5, 34))
#         pixel += 5

def draw_walls():
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 20, 12))
    pygame.draw.rect(screen, (255, 255, 255), (0, height - 12, 20, 12))
    for i in range(36):
        pygame.draw.rect(screen, (255, 255, 255), (30 + i * 35, 0, 25, 12))
        pygame.draw.rect(screen, (255, 255, 255), (30 + i * 35, height - 12, 25, 12))


def make_score():
    score_screen.fill((0, 0, 0))
    if left_points < 10:
        if left_points == 1:
            scoreFont.render_to(score_screen, (548, 0), str(left_points), fgcolor=(255, 255, 255))
        else:
            scoreFont.render_to(score_screen, (478, 0), str(left_points), fgcolor=(255, 255, 255))
    #TODO
    else:
        scoreFont.render_to(score_screen, (140, 0), '1', fgcolor=(255, 255, 255))
        if left_points - 10 == 1:
            scoreFont.render_to(score_screen, (365, 0), str(left_points - 10), fgcolor=(255, 255, 255))
        else:
            scoreFont.render_to(score_screen, (260, 0), str(left_points - 10), fgcolor=(255, 255, 255))
    if right_points < 10:
        if right_points == 1:
            scoreFont.render_to(score_screen, (864, 0), str(right_points), fgcolor=(255, 255, 255))
        else:
            scoreFont.render_to(score_screen, (794, 0), str(right_points), fgcolor=(255, 255, 255))
    #TODO
    else:
        scoreFont.render_to(score_screen, (860, 0), '1', fgcolor=(255, 255, 255))
        if right_points - 10 == 1:
            scoreFont.render_to(score_screen, (1085, 0), str(right_points - 10), fgcolor=(255, 255, 255))
        else:
            scoreFont.render_to(score_screen, (980, 0), str(right_points - 10), fgcolor=(255, 255, 255))
    write_score()


def write_score():
    screen.blit(score_screen, (0, 32))


def new_game(type):
    screen.fill((0, 0, 0))
    global left_points, right_points, leftMovingUp, leftMovingDown, rightMovingUp, rightMovingDown, \
        gameStarted, ball, ballTimer, ballMoving
    if type == 0:
        gameStarted = False
    ball.center = (ballx, bally)
    left_points = 0
    right_points = 0
    ballTimer = 0
    leftMovingUp = False
    leftMovingDown = False
    rightMovingUp = False
    rightMovingDown = False
    ballMoving = False


pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
height = 960
width = 1280
screen = pygame.display.set_mode((width, height))
score_screen = pygame.Surface((width, 255))
pygame.display.set_caption('Coleco Telstar')
scoreFont = pygame.freetype.Font('text/Cone.ttf', 200)
score_sound = pygame.mixer.Sound('sounds/score.wav')
hit_sound = pygame.mixer.Sound('sounds/hit.wav')
spawn_sound = pygame.mixer.Sound('sounds/spawn.wav')

FPS = 60
fpsClock = pygame.time.Clock()

paddle_height = 150
paddle_width = 30
ball_height = 27
ball_width = 33
leftx = 32
lefty = height // 2
rightx = width - 32 - paddle_width
righty = height // 2
ballx = width // 2 - 5
bally = height // 2 + 5
paddle_speed = 10.0
ball_speed = 10.0

topWall = pygame.Rect(0, 0, width, 12)
bottomWall = pygame.Rect(0, height-12, width, 12)
net = pygame.Rect(633, 0, paddle_width, height)
ball = pygame.Rect(ballx, bally, ball_width, ball_height)
ball.center = (ballx, bally)
left_paddle = pygame.Rect(leftx, lefty, paddle_width, paddle_height)
right_paddle = pygame.Rect(rightx, righty, paddle_width, paddle_height)

left_points = 0
right_points = 0
ballTimer = 0

controls = 'Mouse'
leftMovingUp = False
leftMovingDown = False
rightMovingUp = False
rightMovingDown = False
ballMoving = False
scored = False

make_score()
dirchoice = random.choice([0, 1])
if dirchoice == 0:
    leftMoving = True
else:
    leftMoving = False

pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.mouse.set_pos([0, 0])
scoreTime = time.time()
while True:
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
                direction = random.randint(91, 180)
            else:
                direction = random.randint(186, 269)
        else:
            quadrant = random.choice([1, 4])
            if quadrant == 1:
                direction = random.randint(0, 84)
            else:
                direction = random.randint(276, 354)
        vx = ball_speed * math.cos(math.radians(direction))
        vy = ball_speed * math.sin(math.radians(direction))
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
    if not ballMoving:
        write_score()
        ballTimer = time.time() - scoreTime
    draw_walls()
    pygame.draw.rect(screen, (255, 255, 255), net)
    pygame.draw.rect(screen, (255, 255, 255), left_paddle)
    pygame.draw.rect(screen, (255, 255, 255), right_paddle)
    pygame.draw.rect(screen, (255, 255, 255), ball)
    pygame.display.update()
    fpsClock.tick(FPS)
