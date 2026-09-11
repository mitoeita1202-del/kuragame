import pygame
import os
import sys
import math
import pymunk
import pymunk.pygame_util
import time, random
from collections import deque
import pymunk.autogeometry as autogeometry
from pymunk.vec2d import Vec2d
import cv2
import numpy as np
import asyncio

counter = 0
space = None
hoge = 0
start_time = 0
over = False
game_over_time = None
fall = False
falling_shape = None
space_key = False
range_B = 400
last_circle = None
new_circle = None
ball = []
next_ball = deque([])
next_circle = []
drop_ball = []


img_blue = img_red = img_green = img_yellow = img_pink = img_orange = None
hydra_vertices = yellow_vertices = pink_vertices = orenge_vertices = None

B = R = G = Y = N = None
GAME_OVER_LINE = 250
GAME_OVER_LINE_x1 = 550
GAME_OVER_LINE_x2 = 250
GAME_OVER_DELAY = 1000


def create_poly_from_image(space, image, position, scale=1.0):
    mask = pygame.mask.from_surface(image)
    w, h = mask.get_size()
    img_w, img_h = image.get_size()
    cx = img_w / 2
    cy = img_h / 2

    def sample_func(point):
        x, y = point
        x = int(x)
        y = int(y)
        if 0 <= x < w and 0 <= y < h:
            return float(mask.get_at((x, y)))
        return 0.0

    bb = pymunk.BB(0, 0, w, h)
    polyline_set = autogeometry.march_hard(bb, 200, 200, 0.7, sample_func)
    shape = None
    for polyline in polyline_set:
        simplified = autogeometry.simplify_curves(polyline, 1.0)
        vertices = [(v.x - cx, v.y - cy) for v in simplified]
        vertices = [Vec2d(v[0], v[1]) * scale for v in vertices]

        if len(vertices) < 3:
            continue

        body = pymunk.Body(1, pymunk.moment_for_poly(1, vertices))
        body.position = position
        shape = pymunk.Poly(body, vertices)
        shape.friction = 0.8
        shape.elasticity = 0.8
        space.add(body, shape)

    return shape

def pygame_surface_to_cv2(surface):
    data = pygame.image.tostring(surface, "RGBA")
    w, h = surface.get_size()
    img = np.frombuffer(data, dtype=np.uint8).reshape((h, w, 4))
    return img

def extract_polygon_from_image_cv2(img):
    if img.shape[2] == 4:
        gray = img[:, :, 3]
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    kernel = np.ones((10, 10), np.uint8)
    closed = cv2.dilate(thresh, kernel, iterations=1)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return None

    cnt = max(contours, key=cv2.contourArea)
    epsilon = 0.01 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    vertices = [(p[0][0], p[0][1]) for p in approx]
    return vertices

def create_ballB(space, position):
    shape = create_poly_from_image(space, img_blue, position, scale=1.0)
    if shape:
        shape.collision_type = 1
        shape.image = img_blue
    return shape

def create_ballR(space, position):
    shape = create_poly_from_image(space, img_red, position, scale=1.0)
    if shape:
        shape.collision_type = 2
        shape.image = img_red
    return shape

def create_ballG(space, position):
    vertices = hydra_vertices
    if vertices is None or len(vertices) < 3:
        return create_ballB(space, position)
    cx = sum(v[0] for v in vertices) / len(vertices)
    cy = sum(v[1] for v in vertices) / len(vertices)
    centered = [(v[0] - cx, v[1] - cy) for v in vertices]
    body = pymunk.Body(1, pymunk.moment_for_poly(1, centered))
    body.position = position
    shape = pymunk.Poly(body, centered)
    shape.friction = 0.5
    shape.elasticity = 1.0
    shape.image = img_green
    shape.image_rect = img_green.get_rect()
    shape.collision_type = 3
    space.add(body, shape)
    return shape

def create_ballY(space, position):
    vertices = yellow_vertices
    if vertices is None or len(vertices) < 3:
        return create_ballB(space, position)
    img_w, img_h = img_yellow.get_size()
    cx = img_w / 2
    cy = img_h / 2
    centered = [(v[0] - cx, v[1] - cy) for v in vertices]
    body = pymunk.Body(1, pymunk.moment_for_poly(1, centered))
    body.position = position
    shape = pymunk.Poly(body, centered)
    shape.friction = 0.2
    shape.elasticity = 1.0
    shape.image = img_yellow
    shape.image_rect = img_yellow.get_rect()
    shape.collision_type = 4
    space.add(body, shape)
    return shape

def create_ballP(space, position):
    vertices = pink_vertices
    if vertices is None or len(vertices) < 3:
        return create_ballB(space, position)
    img_w, img_h = img_pink.get_size()
    cx = img_w / 2
    cy = img_h / 2
    centered = [(v[0] - cx, v[1] - cy) for v in vertices]
    body = pymunk.Body(1, pymunk.moment_for_poly(1, centered))
    body.position = position
    shape = pymunk.Poly(body, centered)
    shape.friction = 0.2
    shape.elasticity = 1.0
    shape.image = img_pink
    shape.image_rect = img_pink.get_rect()
    shape.collision_type = 5
    space.add(body, shape)
    return shape

def create_ballO(space, position):
    vertices = orenge_vertices
    if vertices is None or len(vertices) < 3:
        return create_ballB(space, position)
    img_w, img_h = img_orange.get_size()
    cx = img_w / 2
    cy = img_h / 2
    centered = [(v[0] - cx, v[1] - cy) for v in vertices]
    body = pymunk.Body(1, pymunk.moment_for_poly(1, centered))
    body.position = position
    shape = pymunk.Poly(body, centered)
    shape.friction = 0.2
    shape.elasticity = 1.0
    shape.image = img_orange
    shape.image_rect = img_orange.get_rect()
    shape.collision_type = 6
    space.add(body, shape)
    return shape

def create_box(space):
    body_under = pymunk.Body(body_type=pymunk.Body.STATIC)
    under = pymunk.Segment(body_under, (250, 550), (550, 550), 3)
    under.friction = 0.2
    under.elasticity = 0.8
    space.add(body_under, under)

def create_right(space):
    body_under = pymunk.Body(body_type=pymunk.Body.STATIC)
    right = pymunk.Segment(body_under, (550, 250), (550, 550), 3)
    right.friction = 0
    right.elasticity = 1.0
    space.add(body_under, right)

def create_left(space):
    body_under = pymunk.Body(body_type=pymunk.Body.STATIC)
    left = pymunk.Segment(body_under, (250, 250), (250, 550), 3)
    left.friction = 0
    left.elasticity = 1.0
    space.add(body_under, left)

def draw_objects(screen, space):
    for shape in space.shapes:
        if hasattr(shape, "image"):
            angle = -math.degrees(shape.body.angle)
            image = pygame.transform.rotate(shape.image, angle)
            rect = image.get_rect(center=shape.body.position)
            screen.blit(image, rect)

def on_collision1(arbiter, space, data):
    global counter
    shape_a, shape_b = arbiter.shapes
    pos_b = shape_b.body.position
    space.remove(shape_a, shape_b)
    create_ballR(space, pos_b)   
    counter += 1
    return True
    
def on_collision2(arbiter, space, data):
    global counter
    shape_a, shape_b = arbiter.shapes
    pos_b = shape_b.body.position
    space.remove(shape_a, shape_b)
    create_ballG(space, pos_b)   
    counter += 10
    return True

def on_collision3(arbiter, space, data):
    global counter
    shape_a, shape_b = arbiter.shapes
    pos_b = shape_b.body.position
    space.remove(shape_a, shape_b)
    create_ballY(space, pos_b)   
    counter += 30
    return True

def on_collision4(arbiter, space, data):
    global counter
    shape_a, shape_b = arbiter.shapes
    pos_b = shape_b.body.position
    space.remove(shape_a, shape_b)
    create_ballP(space, pos_b)   
    counter += 50
    return True
        
def on_collision5(arbiter, space, data):
    global counter
    shape_a, shape_b = arbiter.shapes
    pos_b = shape_b.body.position
    space.remove(shape_a, shape_b)
    create_ballO(space, pos_b)   
    counter += 100
    return True

def on_collision6(arbiter, space, data):
    global counter
    shape_a, shape_b = arbiter.shapes  
    space.remove(shape_a, shape_b)
    counter += 150
    return True

def check_game_over(space):
    for shape in space.shapes:
        if shape.collision_type in (1, 2, 3, 4, 5, 6):
            if shape.body.position.y < GAME_OVER_LINE:
                return True
            if shape.body.position.x > GAME_OVER_LINE_x1:
                return True
            if shape.body.position.x < GAME_OVER_LINE_x2:
                return True   
    return False

def reset_game():
    global space, counter, hoge, start_time, over, game_over_time, fall, falling_shape
    global ball, next_ball, next_circle, last_circle, space_key, range_B, new_circle

    space = pymunk.Space()
    space.gravity = (0, 1000)

    for i, func in enumerate([on_collision1, on_collision2, on_collision3, on_collision4, on_collision5, on_collision6], 1):
        handler = space.add_collision_handler(i, i)
        handler.post_solve = func

    create_box(space)
    create_right(space)
    create_left(space)

    counter = 0
    hoge = 0
    start_time = pygame.time.get_ticks()
    over = False
    game_over_time = None
    fall = False
    falling_shape = None
    space_key = False
    range_B = 400
    last_circle = None
    new_circle = None

    ball = []
    next_ball = deque([])
    next_circle = []

async def main():
    global img_blue, img_red, img_green, img_yellow, img_pink, img_orange
    global hydra_vertices, yellow_vertices, pink_vertices, orenge_vertices
    global B, R, G, Y, N, drop_ball, range_B, last_circle, fall, falling_shape, space_key, hoge, start_time, new_circle, over, game_over_time
    global ball, next_ball, next_circle

    pygame.init()
    WIDTH, HEIGHT = 1300, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 60)

    
    pygame.display.set_caption("suika_game")
    
    image1 = pygame.transform.scale(pygame.image.load("assets/game_over.png"), (WIDTH, HEIGHT))
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    L = 5
    time_limit = 180
    clock = pygame.time.Clock()

    img_blue   = pygame.image.load("assets/kurage_egg.png").convert_alpha()
    img_red    = pygame.image.load("assets/kurage_planula.png").convert_alpha()
    img_green  = pygame.image.load("assets/kurage_polyp.png").convert_alpha()
    img_yellow = pygame.image.load("assets/strobila.png").convert_alpha()
    img_pink   = pygame.image.load("assets/screenshot_bing.png").convert_alpha()
    img_orange = pygame.image.load("assets/kurage.png").convert_alpha()

    img_blue = img_blue.subsurface(img_blue.get_bounding_rect()).copy()
    img_red = img_red.subsurface(img_red.get_bounding_rect()).copy()
    img_green = img_green.subsurface(img_green.get_bounding_rect()).copy()
    img_yellow = img_yellow.subsurface(img_yellow.get_bounding_rect()).copy()
    img_pink = img_pink.subsurface(img_pink.get_bounding_rect()).copy()
    img_orange = img_orange.subsurface(img_orange.get_bounding_rect()).copy()

    b_size = (50, 50)
    r_size = (60, 60)
    g_size = (70, 70)
    y_size = (80, 80)
    p_size = (100, 100)
    o_size = (200, 200)

    img_blue = pygame.transform.scale(img_blue, b_size)
    img_red = pygame.transform.scale(img_red, r_size)
    img_green = pygame.transform.scale(img_green, g_size)
    img_yellow = pygame.transform.scale(img_yellow, y_size)
    img_pink = pygame.transform.scale(img_pink, p_size)
    img_orange = pygame.transform.scale(img_orange, o_size)

    B = {"pos_x": 400, "pos_y": 150, "ball_size": 10, "color": BLUE, "image": img_blue}
    R = {"pos_x": 400, "pos_y": 150, "ball_size": 15, "color": RED, "image": img_red}
    G = {"pos_x": 400, "pos_y": 150, "ball_size": 20, "color": green, "image": img_green}
    Y = {"pos_x": 400, "pos_y": 150, "ball_size": 25, "color": yellow, "image": img_yellow}
    N = {"pos_x": 700, "pos_y": 150, "ball_size": 0, "color": WHITE}

    drop_ball = [B, R, G]

    hydra_vertices = extract_polygon_from_image_cv2(pygame_surface_to_cv2(img_green))
    yellow_vertices = extract_polygon_from_image_cv2(pygame_surface_to_cv2(img_yellow))
    pink_vertices = extract_polygon_from_image_cv2(pygame_surface_to_cv2(img_pink))
    orenge_vertices = extract_polygon_from_image_cv2(pygame_surface_to_cv2(img_orange))

    reset_game()

    new_circle = random.choice(drop_ball)
    ball.append(new_circle)
    last_circle = len(ball) - 1
    next_circle = [random.choice(drop_ball)]
    start_time = pygame.time.get_ticks()
    hoge = 2

    while True:
        current_time = pygame.time.get_ticks()
        elapsed_second = (current_time - start_time) / 1000
        remain = max(0, int(time_limit - elapsed_second))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif (over or remain <= 0) and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    # リセット時も即時セット
                    new_circle = random.choice(drop_ball)
                    ball.append(new_circle)
                    last_circle = len(ball) - 1
                    next_circle = [random.choice(drop_ball)]
                    start_time = pygame.time.get_ticks()
                    hoge = 2
            elif event.type == pygame.KEYDOWN and not over:
                if event.key == pygame.K_LSHIFT:
                    ball.append(N)
                
                # 🛠️ 下矢印キー（DOWN）を押したときに落とす処理
                if event.key == pygame.K_DOWN and last_circle is not None and not fall:
                    fall = True
                    x = ball[last_circle]["pos_x"]
                    if new_circle == B:
                        falling_shape = create_ballB(space, (x, 150))
                    elif new_circle == R:
                        falling_shape = create_ballR(space, (x, 150))
                    elif new_circle == G:
                        falling_shape = create_ballG(space, (x, 150))
                    ball.pop(last_circle)
                    last_circle = None
                    range_B = 400

        keys = pygame.key.get_pressed()
        if last_circle is not None:
            if keys[pygame.K_LEFT]:
                if new_circle == B and range_B <= 513:
                    ball[last_circle]["pos_x"] -= L
                    range_B += L
                if new_circle == R and range_B <= 510:
                    ball[last_circle]["pos_x"] -= L
                    range_B += L
                if new_circle == G and range_B <= 509.5:
                    ball[last_circle]["pos_x"] -= L
                    range_B += L
            elif keys[pygame.K_RIGHT]:
                if new_circle == B and range_B >= 283:
                    ball[last_circle]["pos_x"] += L
                    range_B -= L
                if new_circle == R and range_B >= 290:
                    ball[last_circle]["pos_x"] += L
                    range_B -= L
                if new_circle == G and range_B >= 285:
                    ball[last_circle]["pos_x"] += L
                    range_B -= L

        if not over:
            if check_game_over(space):
                if game_over_time is None:
                    game_over_time = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - game_over_time >= GAME_OVER_DELAY:
                    over = True
            else:
                game_over_time = None

        screen.fill((135, 206, 235))

        if space:
            space.step(1 / 60.0)
            space.step(1 / 60.0)

        if fall and falling_shape is not None:
            if falling_shape.body.position.y > GAME_OVER_LINE:
                new_circle = next_circle[0] # 🛠️ 修正：リストから安全に取得
                ball.append(new_circle)
                last_circle = len(ball) - 1
                next_circle = [random.choice(drop_ball)]
                falling_shape = None
                fall = False
                range_B = 400

        if space:
            for shape in space.shapes:
                if isinstance(shape, pymunk.Segment):
                    a = shape.body.local_to_world(shape.a)
                    b = shape.body.local_to_world(shape.b)
                    pygame.draw.line(screen, WHITE, (int(a.x), int(a.y)), (int(b.x), int(b.y)), 4)

        for circle in ball:
            img = circle["image"]
            rect = img.get_rect(center=(circle["pos_x"], circle["pos_y"]))
            screen.blit(img, rect)

        if space:
            draw_objects(screen, space)

        for circle in next_circle:
            img = circle["image"]
            rect = img.get_rect(center=(700, 120))
            screen.blit(img, rect)

        text_surface = font.render(f"SCORE: {counter}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(700, 500))
        text_next = font.render("NEXT", True, (255, 255, 255))
        text_rect_n = text_next.get_rect(center=(725, 70))

        if over or remain <= 0:
            screen.fill((0, 0, 0))
            gameover_text = font.render(f"SCORE : {counter}", True, (255, 255, 255))
            gameover_rect = gameover_text.get_rect(center=(400, 500))
            screen.blit(gameover_text, gameover_rect)
            screen.blit(image1, (0, 0))

        if not over and remain >= 0:
            screen.blit(text_surface, text_rect)
            screen.blit(text_next, text_rect_n)
            text_time = font.render(f"TIME : {remain}", True, (255, 255, 255))
            screen.blit(text_time, (100, 100))

        pygame.display.flip()
        clock.tick(30)
        await asyncio.sleep(0)

if __name__ == '__main__':
    asyncio.run(main())

