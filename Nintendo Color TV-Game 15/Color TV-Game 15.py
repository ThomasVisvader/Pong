import sys
import pygame.freetype
import pygame
import random
import ctypes
import math
import time
from pygame.locals import *


def left_score():
    global left_points, ballMoving, ball_speed, dirchoice, scored, leftMoving, ballSpawning, scoreSound, bounceCount
    left_points += 1
    ballMoving = False
    ball.center = (width + 50, 300)
    dirchoice = 1
    scored = True
    leftMoving = False
    ballSpawning = True
    scoreSound = False
    bounceCount = 0


def right_score():
    global right_points, ballMoving, ball_speed, dirchoice, scored, leftMoving, ballSpawning, scoreSound, bounceCount
    right_points += 1
    ballMoving = False
    ball.center = (-50, 300)
    dirchoice = 0
    leftMoving = True
    ballSpawning = True
    scored = True
    scoreSound = False
    bounceCount = 0


def paddle_collision(ball, paddle, color):
    global vx, vy, ball_speed, direction, leftMoving, game, bounceCount
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
    if paddle == left_paddle or paddle == left_paddle2 or (game == 5 and color == 0):
        if color == 2 or (color == 0 and vx < 0 and bounceCount < 10):
            if c_point != -1 and c_point != 1:
                ball.left = paddle.right
            if angle < 0:
                direction = 360 + angle
            else:
                direction = angle
        else:
            ball.left = paddle.right
            if direction == 0:
                direction = random.choice([direction - 45, direction, direction + 45])
            else:
                direction = random.choice([direction, 0])
        leftMoving = False
        pygame.mouse.set_pos([width / 2, right_paddle.y])
        if paddle != left_paddle and paddle != left_paddle2:
            bounceCount += 1
        else:
            bounceCount = 0
    else:
        if color == 2 or (color == 1 and vx > 0 and bounceCount < 10):
            if c_point != -1 and c_point != 1:
                ball.right = paddle.left
            if angle == 0:
                direction = 180
            else:
                direction = 180 - angle
        else:
            ball.right = paddle.left
            if direction == 180:
                direction = random.choice([direction - 45, direction, direction + 45])
            else:
                direction = random.choice([direction, 180])
        leftMoving = True
        pygame.mouse.set_pos([width / 2, left_paddle.y])
        if paddle != right_paddle and paddle != right_paddle2:
            bounceCount += 1
        else:
            bounceCount = 0
    if 181 <= direction <= 185:
        direction = 180
    elif 355 <= direction <= 359:
        direction = 0
    vx = ball_speed * math.cos(math.radians(direction))
    vy = ball_speed * math.sin(math.radians(direction))
    paddle_hit_sound.play()
    return ball


def ball_movement(ball):
    global vx, vy, ballSpawning, game, scoreSound, hockeynet, lastCollision, collisionSpeed, leftMoving
    if ball.right >= 1280 or ball.top <= ball.height or ball.bottom >= 960:
        left_score()
    elif ball.left <= 0 or ball.top <= ball.height or ball.bottom >= 960:
        right_score()
    elif ballSpawning and 300 <= ball.centerx <= 800:
        ballSpawning = False
    else:
        if game == 1 and (ball.right >= 410 or ball.left <= 555):
            for i in range(2):
                for j in range(12):
                    if ball.colliderect(net[i][j]):
                        if lastCollision != net[i][j] or lastCollision == 0 or \
                                (lastCollision == net[i][j] and collisionSpeed != vy):
                            lastCollision = net[i][j]
                            collisionSpeed = vy
                            wall_hit_sound.play()
                        if vy > 0:
                            if i == 0:
                                vy *= -1
                                ball.bottom = net[i][j].top
                        elif vy < 0:
                            if i == 1:
                                vy *= -1
                                ball.top = net[i][j].bottom
        elif game == 6 and 635 <= ball.centerx <= 645:
            wall_hit_sound.play()
            bounce = random.random()
            if bounce > 0.9:
                vy *= 1
            else:
                vy *= -1
        elif game == 7 and (625 <= ball.right <= 655 or 625 <= ball.left <= 655):
            if 620 <= ball.bottom <= 875:
                vx *= -1
                if 625 <= ball.right <= 655:
                    wall_hit_sound.play()
                    ball.right = 625
                    leftMoving = True
                    pygame.mouse.set_pos([width / 2, left_paddle.y])
                elif 625 <= ball.left <= 655:
                    wall_hit_sound.play()
                    ball.left = 655
                    leftMoving = False
                    pygame.mouse.set_pos([width / 2, right_paddle.y])
            elif 633 <= ball.centerx <= 647:
                vy = abs(vy)
                wall_hit_sound.play()
        if ball.right >= 1140 or ball.left <= 140:
            if not scoreSound:
                score_sound.play()
                scoreSound = True
        if ball.top <= 85 and not scoreSound:
            ball.top = 85
            vy *= -1
            wall_hit_sound.play()
        elif ball.bottom >= 855 and not scoreSound:
            ball.bottom = 855
            vy *= -1
            wall_hit_sound.play()
        elif game == 3 or game == 4:
            if not scoreSound:
                if ball.left <= 170 and not 325 <= ball.top <= 615 - ball_height:
                    if game == 3:
                        hockeynet = True
                    ball.left = 170
                    vx *= -1
                    wall_hit_sound.play()
                elif ball.right >= 1110 and not 325 <= ball.top <= 615 - ball_height:
                    if game == 3:
                        hockeynet = True
                    ball.right = 1110
                    vx *= -1
                    wall_hit_sound.play()
        if game == 3:
            if hockeynet or ((not hockeynet) and (85 <= ball.top <= 275 or 620 <= ball.bottom <= 875)):
                if 625 <= ball.right <= 655 and vx > 0:
                    wall_hit_sound.play()
                    vx *= -1
                    ball.right = 625
                    hockeynet = False
                elif 625 <= ball.left <= 655 and vx < 0:
                    wall_hit_sound.play()
                    vx *= -1
                    ball.left = 655
                    hockeynet = False
        ball.x += vx * dt
        ball.y += vy * dt
    return ball


def move_up(paddle):
    if paddle.top <= -65:
        paddle.top = -65
        return paddle
    paddle.y -= paddle_speed * dt
    return paddle


def move_down(paddle):
    if paddle.bottom >= 1005:
        paddle.bottom = 1005
        return paddle
    paddle.y += paddle_speed * dt
    return paddle


def draw_net():
    for i in range(6):
        if game == 3 and not hockeynet and (i == 2 or i == 3):
            continue
        elif game == 7 and i != 4 and i!=5:
            continue
        pygame.draw.rect(screen, color_list[game-1][2], (485, 35 + (i * 130), 30, 65))


def draw_walls():
    pygame.draw.rect(screen, (255, 255, 255), (0, height-20, width, 20))
    if game != 7:
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, width, 20))
        color_walls(color_list[game-1][9])
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, 2))
    pygame.draw.rect(screen, (0, 0, 0), (0, height - 2, width, 2))


def draw_goals():
    pygame.draw.rect(screen, color_list[game - 1][4], (0, 20, 8, height - 40))
    pygame.draw.rect(screen, color_list[game - 1][5], (width - 8, 20, 8, height - 40))


def color_walls(rgb):
    pixel = 0
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    for i in range(100):
        if game == 5 or game == 6:
            if i % 4 == 0 and r < 255:
                r += 1
            if g % 3 == 0:
                g += 1
        elif game == 1 or game == 2:
            if i % 3 == 0:
                g += 1
            if i % 5 == 0:
                b += 1
        elif game == 3 or game == 4:
            if i % 4 == 0:
                r += 1
            if i % 2 == 0:
                b += 1
        if i < 30 and (game == 3 or game == 4):
            pygame.draw.rect(screen, (r, g, b), (pixel, 0, 1, 258))
            pygame.draw.rect(screen, (r, g, b), (pixel, 550, 1, 258))
        else:
            pygame.draw.rect(screen, (r, g, b), (pixel, 0, 1, 20))
            pygame.draw.rect(screen, (r, g, b), (pixel, height - 20, 1, 20))
        pixel += 1
    for i in range(900):
        if i >= 870 and (game == 3 or game == 4):
            pygame.draw.rect(screen, (r, g, b), (pixel, 0, 1, 258))
            pygame.draw.rect(screen, (r, g, b), (pixel, 550, 1, 258))
        else:
            pygame.draw.rect(screen, (r, g, b), (pixel, 0, 1, 20))
            pygame.draw.rect(screen, (r, g, b), (pixel, height - 20, 1, 20))
        pixel += 1


def draw_volleyball_net():
    for i in range(2):
        for j in range(12):
            if i == 0:
                pygame.draw.rect(display, (204, 75, 73), net[i][j])
            else:
                pygame.draw.rect(display, (48, 174, 24), net[i][j])


def color_change(object, case):
    p = pygame.PixelArray(display)
    if case == 1:
        if object.top >= 0:
            p[object.x:object.x + object.width, object.top:65] = color_list[game-1][7]
        else:
            p[object.x:object.x + object.width, 0:65] = color_list[game-1][7]
    elif case == 2:
        if object.bottom <= 960:
            p[object.x:object.x + object.width, 875:object.bottom] = color_list[game-1][7]
        else:
            p[object.x:object.x + object.width, 875:960] = color_list[game-1][7]
    elif case == 3:
        if object.left >= 0:
            if object.right >= 140:
                p[object.left:140, object.top:object.bottom] = color_list[game-1][8]
            else:
                p[object.left:object.right, object.top:object.bottom] = color_list[game-1][8]
        else:
            p[0:object.right, object.top:object.bottom] = color_list[game-1][8]
    elif case == 4:
        if object.right <= 1280:
            if object.left <= 1140:
                p[1140:object.right, object.top:object.bottom] = color_list[game-1][8]
            else:
                p[object.left:object.right, object.top:object.bottom] = color_list[game-1][8]
        else:
            p[object.left:1280, object.top:object.bottom] = color_list[game-1][8]
    del p


def make_score():
    score_screen.fill(color_list[game-1][0])
    if left_points < 10:
        if left_points == 1:
            scoreFont.render_to(score_screen, (144, 0), str(left_points), fgcolor=color_list[game-1][3])
        else:
            scoreFont.render_to(score_screen, (70, 0), str(left_points), fgcolor=color_list[game-1][3])
    else:
        scoreFont.render_to(score_screen, (30, 0), 'l', fgcolor=color_list[game-1][3])
        if left_points - 10 == 1:
            scoreFont.render_to(score_screen, (144, 0), str(left_points - 10), fgcolor=color_list[game-1][3])
        else:
            scoreFont.render_to(score_screen, (70, 0), str(left_points - 10), fgcolor=color_list[game-1][3])
    if right_points < 10:
        if right_points == 1:
            scoreFont.render_to(score_screen, (844, 0), str(right_points), fgcolor=color_list[game-1][3])
        else:
            scoreFont.render_to(score_screen, (770, 0), str(right_points), fgcolor=color_list[game-1][3])
    else:
        scoreFont.render_to(score_screen, (728, 0), 'l', fgcolor=color_list[game-1][3])
        if right_points - 10 == 1:
            scoreFont.render_to(score_screen, (844, 0), str(right_points - 10), fgcolor=color_list[game-1][3])
        else:
            scoreFont.render_to(score_screen, (770, 0), str(right_points - 10), fgcolor=color_list[game-1][3])
    write_score()


def write_score():
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


def pong():
    global scored, gameStarted, scoreTime, ball, controls, left_paddle, right_paddle, left_paddle2, right_paddle2, \
        ballTimer
    display.fill(color_list[game - 1][1])
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
        ball = paddle_collision(ball, left_paddle, 2)
    elif gameStarted and not ballSpawning and ball.colliderect(right_paddle):
        ball = paddle_collision(ball, right_paddle, 2)
    if doubles:
        if gameStarted and not ballSpawning and ball.colliderect(left_paddle2):
            ball = paddle_collision(ball, left_paddle2, 2)
        elif gameStarted and not ballSpawning and ball.colliderect(right_paddle2):
            ball = paddle_collision(ball, right_paddle2, 2)
    if game == 5 and (ball.right >= 410 or ball.left <= 555):
        for i in range(2):
            for j in range(12):
                if ball.colliderect(net[i][j]):
                    ball = paddle_collision(ball, net[i][j], i)
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


def doubles_check():
    pygame.draw.rect(display, color_list[game - 1][6], left_paddle)
    pygame.draw.rect(display, color_list[game - 1][6], right_paddle)
    if doubles:
        pygame.draw.rect(display, color_list[game - 1][6], left_paddle2)
        pygame.draw.rect(display, color_list[game - 1][6], right_paddle2)
    if left_paddle.top <= 65:
        color_change(left_paddle, 1)
        if doubles:
            color_change(left_paddle2, 1)
    elif left_paddle.bottom >= 875:
        color_change(left_paddle, 2)
        if doubles:
            color_change(left_paddle2, 2)
    if right_paddle.top <= 65:
        color_change(right_paddle, 1)
        if doubles:
            color_change(right_paddle2, 1)
    elif right_paddle.bottom >= 875:
        color_change(right_paddle, 2)
        if doubles:
            color_change(right_paddle2, 2)


def tennis_a():
    pong()
    draw_walls()
    draw_goals()
    display.blit(screen, (140, 65))
    draw_volleyball_net()
    doubles_check()


def tennis_b():
    pong()
    draw_walls()
    draw_net()
    draw_goals()
    display.blit(screen, (140, 65))
    doubles_check()


def hockey_a():
    global controls
    controls = 'Key'
    pong()
    draw_goals()
    draw_walls()
    draw_net()
    display.blit(screen, (140, 65))
    doubles_check()


def hockey_b():
    global controls
    controls = 'Key'
    pong()
    draw_goals()
    draw_walls()
    display.blit(screen, (140, 65))
    doubles_check()


def volleyball_a():
    pong()
    draw_walls()
    draw_goals()
    display.blit(screen, (140, 65))
    draw_volleyball_net()
    doubles_check()


def volleyball_b():
    pong()
    draw_walls()
    draw_goals()
    draw_net()
    display.blit(screen, (140, 65))
    doubles_check()


def ping_pong():
    pong()
    draw_walls()
    draw_net()
    display.blit(screen, (140, 65))
    doubles_check()


pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
height = 810
width = 1000
display = pygame.display.set_mode((1280, 960))
display.fill((45, 97, 121))
screen = pygame.Surface((width, height))
score_screen = pygame.Surface((900, 255))
handball_screen = pygame.Surface((width, 255))
pygame.display.set_caption('Color TV-Game 15')
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
paddle_speed = 11.0
ball_speed = 15.0

# 0-court, 1-background, 2-net/ball, 3-score, 4-left goal, 5-right goal, 6-paddles, 7-alt paddles, 8-alt ball, 9-walls

color_list = [[(129, 102, 0), (45, 97, 121), (203, 173, 35), (199, 180, 198), (61, 211, 0), (138, 18, 66),
               (163, 192, 68), (45, 97, 121), (77, 129, 160), (215, 175, 59)],
              [(129, 102, 0), (45, 97, 121), (203, 173, 35), (199, 180, 198), (61, 211, 0), (138, 18, 66),
               (163, 192, 68), (45, 97, 121), (77, 129, 160), (215, 175, 59)],
              [(24, 182, 44), (127, 110, 107), (94, 240, 109), (174, 251, 255), (75, 86, 95), (81, 188, 41),
               (255, 159, 255), (127, 110, 107), (187, 164, 181), (152, 255, 141)],
              [(24, 182, 44), (127, 110, 107), (94, 240, 109), (174, 251, 255), (75, 86, 95), (81, 188, 41),
               (255, 159, 255), (127, 110, 107), (187, 164, 181), (152, 255, 141)],
              [(161, 61, 236), (25, 181, 55), (211, 101, 255), (237, 253, 132), (132, 104, 106), (64, 140, 175),
               (188, 199, 255), (25, 181, 55), (89, 239, 113), (231, 155, 255)],
              [(161, 61, 236), (25, 181, 55), (211, 101, 255), (237, 253, 132), (132, 104, 106), (64, 140, 175),
               (188, 199, 255), (25, 181, 55), (89, 239, 113), (231, 155, 255)],
              [(0, 0, 0), (0, 0, 0), (255, 255, 255), (138, 255, 161), (0, 0, 0), (0, 0, 0), (155, 140, 255),
               (0, 0, 0), (255, 255, 255), (255, 255, 255)]]

topWall = pygame.Rect(0, 0, width, 12)
bottomWall = pygame.Rect(0, height-12, width, 12)
ball = pygame.Rect(ballx, bally, ball_width, ball_height)
left_paddle = pygame.Rect(leftx, lefty, paddle_width, paddle_height)
left_paddle2 = pygame.Rect(leftx + 285, lefty, paddle_width, left_paddle.height)
right_paddle = pygame.Rect(rightx, righty, paddle_width, paddle_height)
right_paddle2 = pygame.Rect(rightx - 285, righty, paddle_width, right_paddle.height)


left_points = 0
right_points = 0
ballTimer = 0
scoreTimer = 0
dt = 0
game = 1
blinkTime = time.time()
bounceCount = 0
lastCollision = 0
collisionSpeed = 0

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
scoreSound = False
hockeynet = False

make_score()
dirchoice = random.choice([0, 1])
if dirchoice == 0:
    leftMoving = True
else:
    leftMoving = False

# 0 - red, 1 - green
net = [[], []]
for i in range(6):
    net[0].append(pygame.Rect(555, 160 + (i * 129), 32, 25))
    net[0].append(pygame.Rect(651, 160 + (i * 129), 32, 25))
    net[1].append(pygame.Rect(597, 95 + (i * 129), 32, 25))
    net[1].append(pygame.Rect(693, 95 + (i * 129), 32, 25))

pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.mouse.set_pos([0, 0])
scoreTime = time.time()
lastTime = time.time()
while True:
    dt = time.time() - lastTime
    dt *= FPS
    lastTime = time.time()
    screen.fill(color_list[game-1][0])
    if not gameStarted:
        draw_goals()
        if scoreTimer >= (32/60):
            blink = not blink
            blinkTime = time.time()
        if blink:
            write_score()
        if game == 2 or game == 3 or game == 6 or game == 7:
            draw_net()
        draw_walls()
        display.blit(screen, (140, 65))
        if game == 1 or game == 5:
            draw_volleyball_net()
        pygame.draw.rect(display, color_list[game-1][6], left_paddle)
        pygame.draw.rect(display, color_list[game-1][6], right_paddle)
        doubles_check()
        # if doubles:
        #     pygame.draw.rect(display, color_list[game - 1][6], left_paddle2)
        #     pygame.draw.rect(display, color_list[game - 1][6], right_paddle2)
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
                left_paddle2.x = left_paddle.x + 285
                right_paddle2.x = right_paddle.x - 285
                make_score()
            elif event.type == KEYUP and event.key == K_KP2:
                game = 2
                left_paddle2.x = left_paddle.x + 285
                right_paddle2.x = right_paddle.x - 285
                make_score()
            elif event.type == KEYUP and event.key == K_KP3:
                game = 3
                left_paddle2.x = right_paddle.x - 285
                right_paddle2.x = left_paddle.x + 285
                make_score()
            elif event.type == KEYUP and event.key == K_KP4:
                game = 4
                left_paddle2.x = right_paddle.x - 285
                right_paddle2.x = left_paddle.x + 285
                make_score()
            elif event.type == KEYUP and event.key == K_KP5:
                game = 5
                left_paddle2.x = left_paddle.x + 285
                right_paddle2.x = right_paddle.x - 285
                make_score()
            elif event.type == KEYUP and event.key == K_KP6:
                game = 6
                left_paddle2.x = left_paddle.x + 285
                right_paddle2.x = right_paddle.x - 285
                make_score()
            elif event.type == KEYUP and event.key == K_KP7:
                game = 7
                left_paddle2.x = left_paddle.x + 285
                right_paddle2.x = right_paddle.x - 285
                make_score()
            elif event.type == KEYUP and event.key == K_LALT:
                if ball_speed == 15.0:
                    ball_speed = 25.0
                else:
                    ball_speed = 15.0
            elif event.type == KEYUP and event.key == K_TAB:
                doubles = not doubles
            elif event.type == KEYUP and event.key == K_LCTRL:
                if left_paddle.height == 130:
                    left_paddle = pygame.Rect(leftx, pygame.mouse.get_pos()[1] + 65, paddle_width, 65)
                else:
                    left_paddle = pygame.Rect(leftx, pygame.mouse.get_pos()[1] - 65, paddle_width, 130)
                left_paddle2.height = left_paddle.height
                if controls == 'Mouse':
                    pygame.mouse.set_pos([width / 2, left_paddle.y])
            elif event.type == KEYUP and event.key == K_RCTRL:
                if right_paddle.height == 130:
                    right_paddle = pygame.Rect(rightx, pygame.mouse.get_pos()[1] + 65, paddle_width, 65)
                else:
                    right_paddle = pygame.Rect(rightx, pygame.mouse.get_pos()[1] - 65, paddle_width, 130)
                right_paddle2.height = right_paddle.height
                if controls == 'Mouse':
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
            tennis_a()
        elif game == 2:
            tennis_b()
        elif game == 3:
            hockey_a()
        elif game == 4:
            hockey_b()
        elif game == 5:
            volleyball_a()
        elif game == 6:
            volleyball_b()
        elif game == 7:
            ping_pong()
        if not ballMoving:
            ballTimer = time.time() - scoreTime
        else:
            pygame.draw.rect(display, (color_list[game-1][2]), ball)
            if ball.left <= 140:
                color_change(ball, 3)
            elif ball.right >= 1140:
                color_change(ball, 4)
    pygame.display.update()
    fpsClock.tick(FPS)
