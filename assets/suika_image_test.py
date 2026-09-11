import pygame
import sys
import math
import pymunk
import pymunk.pygame_util
import time, random
from collections import deque

random.seed(time.time())
start_time = pygame.time.get_ticks()
hoge = 0

# 初期化
pygame.init()
WIDTH, HEIGHT = 900, 600
counter = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 60)

# 画面サイズと設定
WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("スイカゲーム")
image1 = pygame.transform.scale(pygame.image.load("game_over.png"), (WIDTH, HEIGHT))

# 画像読み込み
ball_img_B = pygame.image.load("吹き出し用フェリス.png")
ball_img_R = pygame.image.load("流月立ち絵進捗③-仮完成-.png")
ball_img_G = pygame.image.load("無題の図形描画 (2).png")
ball_img_Y = pygame.image.load("無題の図形描画.png")
ball_img_P = pygame.image.load("game_over.png")
ball_img_O = pygame.image.load("Y:\\部活など\\文化祭\\スイカ画像\\OS.png")
ball_img_M = pygame.image.load("無題の図形描画 (1).png")
ball_img_BR = pygame.image.load("OIP.jpg")

# ★ 正方形トリミング → 円形マスク → 回転しても崩れない画像生成
def make_circle_image(img, radius):
    size = radius * 2

    # --- 正方形に中央トリミング（ここが重要） ---
    w, h = img.get_size()
    min_side = min(w, h)
    crop_rect = pygame.Rect(
        (w - min_side) // 2,
        (h - min_side) // 2,
        min_side,
        min_side
    )
    img = img.subsurface(crop_rect)

    # 正方形を円のサイズにリサイズ
    img = pygame.transform.smoothscale(img, (size, size)).convert_alpha()

    # 完全透明のサーフェス
    circle_surface = pygame.Surface((size, size), pygame.SRCALPHA)

    # 円形マスク
    mask = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(mask, (255, 255, 255, 255), (radius, radius), radius)

    # マスク適用
    circle_surface.blit(img, (0, 0))
    circle_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return circle_surface

# サイズから画像取得（NEXT・プレビュー用）
def get_ball_image_by_size(size):
    if size == 10:
        return ball_img_B
    elif size == 15:
        return ball_img_R
    elif size == 20:
        return ball_img_G
    elif size == 25:
        return ball_img_Y
    elif size == 35:
        return ball_img_P
    elif size == 40:
        return ball_img_O
    elif size == 50:
        return ball_img_M
    elif size == 60:
        return ball_img_BR
    return None

# 色
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)

L = 5
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 1000)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# ボール定義（待機用）
B = ({"pos_x": 400, "pos_y": 150, "ball_size": 10, "color": BLUE})
R = ({"pos_x": 400, "pos_y": 150, "ball_size": 15, "color": RED})
G = ({"pos_x": 400, "pos_y": 150, "ball_size": 20, "color": green})
Y = ({"pos_x": 400, "pos_y": 150, "ball_size": 25, "color": yellow})
N = ({"pos_x": 700, "pos_y": 150, "ball_size": 0, "color": WHITE})

drop_ball = [B, R, G, Y]
range_B = 400

# 壁
def create_box(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    under = pymunk.Segment(body, (250, 550), (550, 550), 3)
    under.friction = 0.8
    space.add(body, under)

def create_right(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    right = pymunk.Segment(body, (550, 250), (550, 550), 3)
    space.add(body, right)

def create_left(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    left = pymunk.Segment(body, (250, 250), (250, 550), 3)
    space.add(body, left)

# ボール生成（物理用）
def create_ball(space, position, radius, color_type):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, radius))
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.friction = 0.2
    shape.elasticity = 0
    shape.collision_type = color_type
    space.add(body, shape)
    return shape

# 衝突処理
def merge_ball(arbiter, space, data, new_radius, new_type, score):
    global counter
    shape_a, shape_b = arbiter.shapes
    pos = shape_b.body.position
    space.remove(shape_a, shape_b)
    create_ball(space, pos, new_radius, new_type)
    counter += score
    return True

# 衝突ハンドラ
space.add_collision_handler(1, 1).post_solve = lambda a, s, d: merge_ball(a, s, d, 15, 2, 1)
space.add_collision_handler(2, 2).post_solve = lambda a, s, d: merge_ball(a, s, d, 20, 3, 10)
space.add_collision_handler(3, 3).post_solve = lambda a, s, d: merge_ball(a, s, d, 25, 4, 30)
space.add_collision_handler(4, 4).post_solve = lambda a, s, d: merge_ball(a, s, d, 35, 5, 50)
space.add_collision_handler(5, 5).post_solve = lambda a, s, d: merge_ball(a, s, d, 40, 6, 100)
space.add_collision_handler(6, 6).post_solve = lambda a, s, d: merge_ball(a, s, d, 50, 7, 150)
space.add_collision_handler(7, 7).post_solve = lambda a, s, d: merge_ball(a, s, d, 60, 8, 160)

create_box(space)
create_right(space)
create_left(space)

ball = []
next_ball = deque([])
next_circle = []

over = False
game_over_time = None
last_circle = None
new_circle = None
next_b = None

def check_game_over(space):
    for shape in space.shapes:
        if isinstance(shape, pymunk.Circle):
            if shape.body.position.y <= 250:
                return True
    return False

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN and not over:

            # スペース：次のボールをキューに追加
            if event.key == pygame.K_SPACE:
                next_b = random.choice(drop_ball)
                next_ball.append(next_b)
                hoge += 1

                if hoge >= 2:
                    next_circle.append(next_b)
                    new_circle = next_ball.popleft()
                    ball.append(new_circle)
                    last_circle = len(ball) - 1
                    range_B = 400

            # ↓：現在の待機ボールを落とす
            if event.key == pygame.K_DOWN:
                if last_circle is None or new_circle is None:
                    continue

                cx = ball[last_circle]["pos_x"]
                size = ball[last_circle]["ball_size"]

                if size == 10:
                    create_ball(space, (cx, 150), 10, 1)
                elif size == 15:
                    create_ball(space, (cx, 150), 15, 2)
                elif size == 20:
                    create_ball(space, (cx, 150), 20, 3)
                elif size == 25:
                    create_ball(space, (cx, 150), 25, 4)

                if new_circle in ball:
                    ball.remove(new_circle)

                if len(ball) > 0:
                    last_circle = len(ball) - 1
                else:
                    last_circle = None

                if next_b in next_circle:
                    next_circle.remove(next_b)

    # キー入力で待機ボールを左右に動かす
    keys = pygame.key.get_pressed()
    if last_circle is not None and new_circle is not None:
        if keys[pygame.K_LEFT] and range_B <= 530:
            ball[last_circle]["pos_x"] -= L
            range_B += L
        if keys[pygame.K_RIGHT] and range_B >= 268:
            ball[last_circle]["pos_x"] += L
            range_B -= L

    # GAME OVER 判定
    if not over:
        if check_game_over(space):
            if game_over_time is None:
                game_over_time = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - game_over_time >= 2000:
                over = True
        else:
            game_over_time = None

    screen.fill((255, 200, 150))
    space.step(1 / 60.0)

    # NEXT の円形画像描画
    for circle in next_circle:
        size = circle["ball_size"]
        img = get_ball_image_by_size(size)
        if img is not None:
            next_img = make_circle_image(img, size)
            screen.blit(next_img, (700 - size, 120 - size))

    # 待機中のボール（キーで動かすボール）を画像で描画
    if last_circle is not None and new_circle is not None:
        preview = ball[last_circle]
        size = preview["ball_size"]
        img = get_ball_image_by_size(size)
        if img is not None:
            preview_img = make_circle_image(img, size)
            screen.blit(preview_img, (preview["pos_x"] - size, preview["pos_y"] - size))

    # Pymunk のデバッグ描画
    space.debug_draw(draw_options)

    # 物理ボール（落下中）の円形画像＋回転描画
    for shape in space.shapes:
        if isinstance(shape, pymunk.Circle):
            x = int(shape.body.position.x)
            y = int(shape.body.position.y)
            r = int(shape.radius)

            if shape.collision_type == 1:
                img = ball_img_B
            elif shape.collision_type == 2:
                img = ball_img_R
            elif shape.collision_type == 3:
                img = ball_img_G
            elif shape.collision_type == 4:
                img = ball_img_Y
            elif shape.collision_type == 5:
                img = ball_img_P
            elif shape.collision_type == 6:
                img = ball_img_O
            elif shape.collision_type == 7:
                img = ball_img_M
            elif shape.collision_type == 8:
                img = ball_img_BR
            else:
                continue

            # 円形画像を作成（正方形トリミング済み）
            circle_img = make_circle_image(img, r)

            # 物理角度で回転
            angle_deg = -math.degrees(shape.body.angle)
            rotated = pygame.transform.rotate(circle_img, angle_deg)

            # 中心補正
            rect = rotated.get_rect(center=(x, y))
            screen.blit(rotated, rect.topleft)

    # スコア表示
    text_surface = font.render(f"Count: {counter}", True, (255, 255, 255))
    screen.blit(text_surface, (650, 500))

    text_next = font.render("NEXT", True, (255, 255, 255))
    screen.blit(text_next, (680, 70))

    if over:
        screen.blit(image1, (0, 0))
        gameover_text = font.render(f"Score : {counter}", True, (255, 255, 255))
        screen.blit(gameover_text, (350, 500))

    pygame.display.flip()
    clock.tick(30)
