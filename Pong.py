import sys
import pygame.freetype
import pygame
import random
import heapq
import ctypes
import math
from pygame.locals import *


def left_score():
    global left_points, ballMoving, ball_speed
    left_points += 1
    ballMoving = False
    ball_speed = 10.0
    ball.center = (width + 50, 300)
    score_sound.play()


def right_score():
    global right_points, ballMoving, ball_speed
    right_points += 1
    ballMoving = False
    ball_speed = 10.0
    ball.center = (-50, 300)
    score_sound.play()


def paddle_collision(ball, paddle):
    global vx, vy, ball_speed, direction
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
    else:
        if c_point != -1 and c_point != 1:
            ball.right = paddle.left
        if angle == 0:
            direction = 180
        else:
            direction = 180 - angle
    if ball_speed < 22.0:
        ball_speed += 1
    vx = ball_speed * math.cos(math.radians(direction))
    vy = ball_speed * math.sin(math.radians(direction))
    ball.x += vx
    ball.y += vy
    hit_sound.play()
    return ball

# alpha = max relative angle
# relative angle = c_point * alpha
# actual angle :
# if left_paddle:
#   if relative angle == 0:
#       actual angle = 0
#   elif relative angle < 0:
#       actual angle = 360 - alpha
#   else:
#       actual angle = relative angle
# elif right_paddle:
#   if relative angle == 0:
#       actual angle = 180
#   elif relative angle < 0:
#       actual angle = 180 - relative angle
#   else:
#       actual angle = 180 - relative angle


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


def write_score():
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


def restart():
    screen.fill((0, 0, 0))
    global left_points, right_points, gameStarted
    left_points = 0
    right_points = 0
    gameStarted = False


def intro(yspeed):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, 140))
    pygame.draw.rect(screen, (0, 0, 0), (0, 390, width, height - 390))
    background()
    global blocks, introMovingUp
    for block in blocks:
        line_animation(block)
        if introMovingUp:
            block.y -= yspeed
        else:
            block.y += yspeed
        block.x += 3
    if (blocks[1].y + 110 == height and not introMovingUp) or \
            (blocks[1].y == 60 and introMovingUp):
        introMovingUp = bool(random.getrandbits(1))
    screen.blit(score_screen, (0, 140))
    draw_net()


def line_animation(block):
    for j in range(12):
        pygame.draw.rect(screen, (0, 0, 0), block)
        color(block)
        block.x += 120
    block.x -= 120 * 12
    if block.x >= 60:
        block.x = -60
    if not introMovingUp and block.y >= height + 80:
        block.y = -120
    elif introMovingUp and block.y <= -80:
        block.y = height + 120


pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
height = 960
width = 1280
screen = pygame.display.set_mode((width, height))
score_screen = pygame.Surface((width, 255))
intro_screen = pygame.Surface((width, height))
pygame.display.set_caption('Pong')
scoreFont = pygame.freetype.Font('text/Cone.ttf', 420)
titleFont = pygame.freetype.Font('text/Cone.ttf', 270)
textFont = pygame.freetype.Font('text/Cone.ttf', 25)
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
ballx = width // 2
bally = height // 2
paddle_speed = 10.0
ball_speed = 10.0

startButton = pygame.Rect(width // 2 - 100, height // 2, 200, 50)
exitButton = pygame.Rect(width // 2 - 100, height // 2 + 100, 200, 50)
topWall = pygame.Rect(0, 0, width, 65)
bottomWall = pygame.Rect(0, height-65, width, 65)
ball = pygame.Rect(ballx, bally, ballsize, ballsize)
ball.center = (ballx, bally)
left_paddle = pygame.Rect(leftx, lefty, paddle_width, paddle_height)
right_paddle = pygame.Rect(rightx, righty, paddle_width, paddle_height)
left_paddle.center = (leftx, lefty)
right_paddle.center = (rightx, righty)

left_points = 0
right_points = 0

leftMovingUp = False
leftMovingDown = False
rightMovingUp = False
rightMovingDown = False
ballMoving = False
gameStarted = False

introMovingUp = False
chosen = False

blocks = []
blocks.append(pygame.Rect(0, -60, 60, 60))
blocks.append(pygame.Rect(0, 80, 60, 110))
for i in range(6):
    blocks.append(pygame.Rect(0, 270 + (i*140), 60, 60))
diffBlock = pygame.Rect(0, -60, 60, 60)

write_score()
dirchoice = random.choice([0, 1])
if dirchoice == 0:
    direction = random.randint(91, 269)
else:
    direction = random.randint(276, 444)
while True:
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
        # longBlock.x += 5
        # longBlock.y += 5
        # titleFont.render_to(screen, (400, 200), 'PONG', fgcolor=(255, 255, 255))
        # mouse = pygame.mouse.get_pos()
        # if startButton.collidepoint(mouse):
        #     pygame.draw.rect(screen, (128, 128, 128), startButton)
        #     textFont.render_to(screen, (startButton.x + 55, startButton.y + 20), 'Start game', fgcolor=(0, 0, 0))
        # else:
        #     pygame.draw.rect(screen, (255, 255, 255), startButton)
        #     textFont.render_to(screen, (startButton.x + 55, startButton.y + 20), 'Start game', fgcolor=(0, 0, 0))
        # if exitButton.collidepoint(mouse):
        #     pygame.draw.rect(screen, (128, 128, 128), exitButton)
        #     textFont.render_to(screen, (exitButton.x + 60, exitButton.y + 20), 'Exit game', fgcolor=(0, 0, 0))
        # else:
        #     pygame.draw.rect(screen, (255, 255, 255), exitButton)
        #     textFont.render_to(screen, (exitButton.x + 60, exitButton.y + 20), 'Exit game', fgcolor=(0, 0, 0))
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_RETURN:
                    gameStarted = True
            # if event.type == MOUSEBUTTONUP:
            #     if startButton.collidepoint(mouse):
            #         gameStarted = True
            #     elif exitButton.collidepoint(mouse):
            #         pygame.quit()
            #         sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
    elif gameStarted:
        chosen = False
        FPS = 60
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), topWall)
        pygame.draw.rect(screen, (255, 255, 255), bottomWall)
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
                    ball.x = ballx
                    ball.y = random.randint(65, height-65)
                    vx = ball_speed * math.cos(math.radians(direction))
                    vy = ball_speed * math.sin(math.radians(direction))
                    spawn_sound.play()
        if ballMoving:
            ball = ball_movement(ball)
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
        if not ballMoving:
            write_score()
            if left_points == 15 or right_points == 15:
                restart()
        background()
        pygame.draw.rect(screen, (255, 255, 255), left_paddle)
        color(left_paddle)
        pygame.draw.rect(screen, (255, 255, 255), right_paddle)
        color(right_paddle)
        pygame.draw.rect(screen, (255, 255, 255), ball)
        color(ball)
    if ballMoving:
        v = math.sqrt(math.pow(vx, 2) + math.pow(vy, 2))
        textFont.render_to(screen, (100, 30), str(ball.x), fgcolor=(255, 255, 255))
        textFont.render_to(screen, (100, 50), str(ball.y), fgcolor=(255, 255, 255))
        textFont.render_to(screen, (100, 90), str(vx), fgcolor=(255, 255, 255))
        textFont.render_to(screen, (100, 110), str(vy), fgcolor=(255, 255, 255))
        textFont.render_to(screen, (100, 130), str(v), fgcolor=(255, 255, 255))
        textFont.render_to(screen, (100, 150), str(direction), fgcolor=(255, 255, 255))
        textFont.render_to(screen, (100, 170), str(dirchoice), fgcolor=(255, 255, 255))
    pygame.display.update()
    fpsClock.tick(FPS)
