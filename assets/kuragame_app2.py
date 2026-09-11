#main.py
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
start = pygame.time.get_ticks()
clock = pygame.time.Clock()
#font_time = pygame.font.Font(None,48)
time_limit = 180
random.seed(time.time())
start_time = pygame.time.get_ticks()
hoge =0
# 初期化
pygame.init()
WIDTH, HEIGHT = 1300, 800
counter = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))#スクリーンを設定
font = pygame.font.Font(None, 60)#フォント定義


# 画面サイズと設定
WIDTH, HEIGHT = 800, 600

pygame.display.set_caption("スイカゲーム")
image1 = pygame.transform.scale(pygame.image.load("C:\Users\mmym0\OneDrive\ドキュメント\瑛大\ゲーム作成\瑛大個人用\dist\スイカ画像\game over 筆記体.png"), (WIDTH, HEIGHT))#画像ロード
#image_e = pygame.transform.scale(pygame.image.load("Y:\部活など\文化祭\スイカ画像\進化の輪.png"), (400, 350))#画像ロード

# 色の定義
# 色の定義
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
puple = 	(128, 0, 128)
orenge = (255, 165, 0)
magenta = (255, 0, 255)
fall = False
gravity = 9
color = (255,255,0)
L = 5
r =5
R1=5
L1=5
roll = False
angle = 5
clock = pygame.time.Clock()
list =[10,20,30,40]
space = 0
#fallen_ball = []
#next_ball = False
last_circle = None

space = pymunk.Space()
space.gravity = (0, 1000)  # 重力設定
space_key = False
def resource_path(relative_path):
    """ 開発環境とPyInstallerで固めた環境の両方で、正しいファイルパスを返す関数 """
    try:
        # PyInstallerで一時フォルダに解凍されたパスを取得
        base_path = sys._MEIPASS
    except Exception:
        # 開発時の通常のパス
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
draw_options = pymunk.pygame_util.DrawOptions(screen)
img_blue   = pygame.image.load("C:\Users\mmym0\OneDrive\ドキュメント\瑛大\ゲーム作成\瑛大個人用\dist\スイカ画像\クラゲ：卵.png")#os
img_red    = pygame.image.load("C:\Users\mmym0\OneDrive\ドキュメント\瑛大\ゲーム作成\瑛大個人用\dist\スイカ画像\クラゲ：プラヌラ.png")#CPU
img_green  = pygame.image.load("C:\Users\mmym0\OneDrive\ドキュメント\瑛大\ゲーム作成\瑛大個人用\dist\スイカ画像\クラゲ：ポリプ.png")#メモリ
img_yellow = pygame.image.load("C:\Users\mmym0\OneDrive\ドキュメント\瑛大\ゲーム作成\瑛大個人用\dist\スイカ画像\ストロビラ.png")#マザーボード
img_pink = pygame.image.load("C:\Users\mmym0\OneDrive\ドキュメント\瑛大\ゲーム作成\瑛大個人用\dist\スイカ画像\スクリーンショット_21-8-2026_12443_www.bing.com-Photoroom.png")
img_orange = pygame.image.load("C:\Users\mmym0\OneDrive\ドキュメント\瑛大\ゲーム作成\瑛大個人用\dist\スイカ画像\クラゲ.png")


img_blue = img_blue.convert_alpha()
img_blue = img_blue.subsurface(img_blue.get_bounding_rect()).copy()
img_red = img_red.convert_alpha()
img_red = img_red.subsurface(img_red.get_bounding_rect()).copy()
img_green = img_green.convert_alpha()
img_green = img_green.subsurface(img_green.get_bounding_rect()).copy()
img_yellow = img_yellow.convert_alpha()
img_yellow = img_yellow.subsurface(img_yellow.get_bounding_rect()).copy()
img_pink = img_pink.convert_alpha()
img_pink = img_pink.subsurface(img_pink.get_bounding_rect()).copy()
img_orange = img_orange.convert_alpha()
img_orange = img_orange.subsurface(img_orange.get_bounding_rect()).copy()
#img_magenta = img_magenta.subsurface(img_magenta.get_bounding_rect()).copy()








b_size = (50,50)
r_size = (60,60)
g_size = (70,70)
y_size = (80,80)
p_size = (100,100)
o_size = (200,200)
#m_size = (110,110)





img_blue = pygame.transform.scale(img_blue, b_size)
img_red = pygame.transform.scale(img_red, r_size)
img_green = pygame.transform.scale(img_green, g_size)
img_yellow = pygame.transform.scale(img_yellow, y_size)
img_pink = pygame.transform.scale(img_pink, p_size)
img_orange = pygame.transform.scale(img_orange, o_size)
#img_magenta = pygame.transform.scale(img_magenta, m_size)

falling_shape = None
fall = False













B =  ({"pos_x": 400,"pos_y" :150,"ball_size":10,"color":BLUE,"image":img_blue})
R = ({"pos_x": 400,"pos_y" :150,"ball_size":15,"color":RED,"image":img_red})
G =  ({"pos_x": 400,"pos_y" :150,"ball_size":20,"color":green,"image":img_green})
Y = ({"pos_x": 400,"pos_y" :150,"ball_size":25,"color":yellow,"image":img_yellow})
N = ({"pos_x": 700,"pos_y" :150,"ball_size":0,"color":WHITE})

# NB =  ({"pos_x": 700,"pos_y" :100,"ball_size":10,"color":BLUE})
# NR = ({"pos_x": 700,"pos_y" :100,"ball_size":15,"color":RED})
# NG =  ({"pos_x": 700,"pos_y" :100,"ball_size":20,"color":green})
# NY = ({"pos_x": 700,"pos_y" :100,"ball_size":25,"color":yellow})
drop_ball =[B,R,G]
range_B = 400

def create_poly_from_image(space, image, position, scale=1.0):
    mask = pygame.mask.from_surface(image)
    w, h = mask.get_size()
    img_w, img_h = image.get_size()
    cx = img_w / 2#画像の中心を得る
    cy = img_h / 2#画像の中心を得る

    def sample_func(point):
        x, y = point
        x = int(x)
        y = int(y)
        if 0 <= x < w and 0 <= y < h:
            return float(mask.get_at((x, y)))#0か1をリターン　xとyはピクセルの座標
        return 0.0

    bb = pymunk.BB(0, 0, w, h)#範囲内で輪郭を探す（今回はw,h）

    # march_hard は PolylineSet を返す
    polyline_set = autogeometry.march_hard(bb, 200, 200, 0.7, sample_func)#march_hardは輪郭抽出 200,200は細かさ　0.7は線の境界の曖昧さ　
    #sample_funcは1ピクセルごとにそれが内側にあるかないか判断（色があるかないか）　
    shape = None
    #  各 Polyline に対して simplify_curves() を個別に呼び出す
    for polyline in polyline_set:
        simplified = autogeometry.simplify_curves(polyline, 1.0)#輪郭簡略化（輪郭点が多すぎるため）simplify_curvesは簡略化する
        vertices = [(v.x - cx, v.y - cy) for v in simplified]#座標の中心を原点にする　pygameは左上が基準、今回は中心を基準にしたい、だから頂点からの相対座標にする
        vertices = [Vec2d(v[0], v[1]) * scale for v in vertices]#スケールはサイズ変更のときにも比率が合うようにする

        if len(vertices) < 3:
            continue

        body = pymunk.Body(1, pymunk.moment_for_poly(1, vertices))#（質量1の物体を作る）　pymunk.moment_for_polyは慣性モーメント　頂点から判断
        body.position = position

        shape = pymunk.Poly(body, vertices)
        shape.friction = 0.8
        shape.elasticity = 0.8

        space.add(body, shape)

    if shape is None:
        return None
    return shape









def extract_polygon_from_image(path):
    # 画像読み込み
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    # 透明部分がある場合はアルファチャンネルを使う
    if img.shape[2] == 4:
        alpha = img[:, :, 3]
        gray = alpha
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 二値化
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

    # 輪郭を太らせて閉じる
    kernel = np.ones((10, 10), np.uint8)
    closed = cv2.dilate(thresh, kernel, iterations=1)

    # 輪郭抽出
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return None

    # 最大の輪郭を使う
    cnt = max(contours, key=cv2.contourArea)

    # 輪郭を簡略化（頂点数を減らす）
    epsilon = 0.01 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    # pymunk用に変換
    vertices = [(p[0][0], p[0][1]) for p in approx]
    # 画像の縮小率を計算
    scale_x = g_size[0] / img.shape[1]
    scale_y = g_size[1] / img.shape[0]

    # 頂点を縮小
    vertices = [(int(x * scale_x), int(y * scale_y)) for (x, y) in vertices]


    return vertices


# def create_hydra_polygon(space, position, vertices):
#     # 中心を画像の中心に合わせる
#     cx = sum(v[0] for v in vertices) / len(vertices)
#     cy = sum(v[1] for v in vertices) / len(vertices)
#     centered = [(v[0] - cx, v[1] - cy) for v in vertices]

#     body = pymunk.Body(1, pymunk.moment_for_poly(1, centered))
#     body.position = position

#     shape = pymunk.Poly(body, centered)
#     shape.friction = 0.5
#     shape.elasticity = 0.0

#     space.add(body, shape)
   
#     return shape


def pygame_surface_to_cv2(surface):
    data = pygame.image.tostring(surface, "RGBA")#RGBAファイルに変換
    w, h = surface.get_size()#画像の幅、高さを取り出す
    img = np.frombuffer(data, dtype=np.uint8).reshape((h, w, 4))#RGBAをcv2が扱える高さ、幅、4チャンネルの画像に変換
    return img

def extract_polygon_from_image_cv2(img):
    if img.shape[2] == 4:#透明度ありの判定（RGBA）
        gray = img[:, :, 3]#すべての列、行、3（透明度）を取り出す
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#RGB（色）を白黒画像に変換する

    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)#10を境界にして白か黒か分ける、閾値は使用しないので1つ目は消去
    kernel = np.ones((10, 10), np.uint8)#10×10のスタンプ　
    closed = cv2.dilate(thresh, kernel, iterations=1) #白を膨張させる（interationsは1回太くする）

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#closedから輪郭のリストを取り出す

    if len(contours) == 0:
        return None

    cnt = max(contours, key=cv2.contourArea)

    epsilon = 0.01 * cv2.arcLength(cnt, True)#輪郭の長さ × 1% を誤差
    approx = cv2.approxPolyDP(cnt, epsilon, True)#点を

    vertices = [(p[0][0], p[0][1]) for p in approx]#リストの中のリストから情報を取り出す、リストは輪郭の点の座標
    return vertices



hydra_img_cv2 = pygame_surface_to_cv2(img_green)
hydra_vertices = extract_polygon_from_image_cv2(hydra_img_cv2)
yellow_vertices = extract_polygon_from_image_cv2(pygame_surface_to_cv2(img_yellow))
pink_vertices = extract_polygon_from_image_cv2(pygame_surface_to_cv2(img_pink))
orenge_vertices = extract_polygon_from_image_cv2(pygame_surface_to_cv2(img_orange))

# 衝突タイプを設定
def check_collision(new_circle, ball):
    for circle in ball:
        dx = new_circle["pos_x"] - circle["pos_x"]
        dy = new_circle["pos_y"] - circle["pos_y"]
        distance =  (dx**2 + dy**2)**0.5
        if distance < 40:
            return True
    return False
    #distance = math.sqrt((new_circle["pos_x"] - last_circle["pos_x"])**2 + (new_circle["pos_y"] - last_circle["pos_y"])**2)
    #return distance < (new_circle["ball_size"] + last_circle["ball_size"])
def create_box(space):
    
    body_under = pymunk.Body(body_type=pymunk.Body.STATIC)
    #body.position = (250, 100)
    under = pymunk.Segment(body_under, (250, 550), (550, 550), 3)
    under.friction = 0.2
    under.elasticity = 0.8
    space.add(body_under,under)
def create_right(space):
    
    body_under = pymunk.Body(body_type=pymunk.Body.STATIC)
    #body.position = (250, 100)
    right = pymunk.Segment(body_under, (550, 250), (550, 550), 3)
    right.friction = 0
    right.elasticity=1.0
    space.add(body_under,right)
def create_left(space):
    
    body_under = pymunk.Body(body_type=pymunk.Body.STATIC)
    #body.position = (250, 100)
    left = pymunk.Segment(body_under, (250, 250), (250, 550), 3)
    left.friction = 0
    left.elasticity=1.0
    space.add(body_under,left)
def create_ballB(space, position):
    shape = create_poly_from_image(space, img_blue, position, scale=1.0)
    shape.collision_type = 1
    shape.image = img_blue
    return shape


def create_ballR(space, position):
    shape = create_poly_from_image(space, img_red, position, scale=1.0)
    shape.collision_type = 2
    shape.image = img_red
    return shape


def create_ballG(space, position):
    vertices = hydra_vertices

    if vertices is None or len(vertices) < 3:
        return create_ballP(space, position)

    cx = sum(v[0] for v in vertices) / len(vertices) #頂点を原点にする　演算がずれるため　ポリゴンの中心を（0,0）にしたい
    cy = sum(v[1] for v in vertices) / len(vertices)#len(vertices)は頂点の数
    centered = [(v[0] - cx, v[1] - cy) for v in vertices]#すべての座標を

    body = pymunk.Body(1, pymunk.moment_for_poly(1, centered))
    body.position = position

    shape = pymunk.Poly(body, centered)
    shape.friction = 0.5
    shape.elasticity = 1.0

    # 画像の中心をポリゴンの中心に合わせる
    shape.image = img_green
    shape.image_rect = img_green.get_rect()

    shape.collision_type = 3

    space.add(body, shape)
    return shape



def create_ballY(space, position):
    vertices = yellow_vertices
    if vertices is None or len(vertices) < 3:
        return create_ballY(space, position)  # 無限再帰防止

    # --- 画像の中心を基準にポリゴンを中央揃えする ---
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
        return create_ballP(space, position)  # 無限再帰防止

    # --- 画像の中心を基準にポリゴンを中央揃えする ---
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
        return create_ballO(space, position)  # 無限再帰防止

    # --- 画像の中心を基準にポリゴンを中央揃えする ---
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



#def create_ballM(space, position, radius=90):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, radius))
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.friction = 0.2
    shape.elasticity = 0
    shape.color = (0, 0,255, 255)

    # 画像を読み込んで shape に持たせる
    shape.image = img_magenta
    shape.image_rect = img_magenta.get_rect()

    space.add(body, shape)
    shape.collision_type = 7
    return shape


#def create_ballBR(space, position, radius=60):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, radius))
    body.position = (400,150)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.friction = 0.2
    shape.elasticity = 0
    shape.color = (0,0,0,255)
    space.add(body, shape)
    shape.collision_type = 8
    return shape








def draw_objects(screen, space):
    for shape in space.shapes:
        if hasattr(shape, "image"):
            angle = -math.degrees(shape.body.angle)
            image = pygame.transform.rotate(shape.image, angle)
            rect = image.get_rect(center=shape.body.position)
            screen.blit(image, rect)

    
def on_collision1(arbiter, space, data):#青から赤
    global counter
    shape_a, shape_b = arbiter.shapes
    pos_b = shape_b.body.position
    for shape in (shape_a, shape_b):
        
        space.remove(shape_a,shape_b)
        shape_b = create_ballR(space,(pos_b))   
        counter +=1
        return True
    
def on_collision2(arbiter, space, data):#赤から緑
    global counter

    shape_a, shape_b = arbiter.shapes
    pos_b = shape_b.body.position
    for shape in (shape_a, shape_b):
        space.remove(shape_a,shape_b)
        shape_b = create_ballG(space,(pos_b))   
        counter +=10
def on_collision3(arbiter, space, data):#緑から黄
    global counter
    shape_a, shape_b = arbiter.shapes
    pos_b = shape_b.body.position
    for shape in (shape_a, shape_b):
        space.remove(shape_a,shape_b)
        shape_b = create_ballY(space,(pos_b))   
        counter += 30
def on_collision4(arbiter, space, data):#黄から紫
    global counter
    shape_a, shape_b = arbiter.shapes
    pos_b = shape_b.body.position
    for shape in (shape_a, shape_b):
        space.remove(shape_a,shape_b)
        shape_b = create_ballP(space,(pos_b))   
        counter +=50
        
def on_collision5(arbiter, space, data):#紫からオレンジ
    global counter
    shape_a, shape_b = arbiter.shapes
    pos_b = shape_b.body.position
    for shape in (shape_a, shape_b):
        space.remove(shape_a,shape_b)
        shape_b = create_ballO(space,(pos_b))   
        counter +=100
        return
#def on_collision6(arbiter, space, data):#オレンジから紫
    #global counter
    #shape_a, shape_b = arbiter.shapes
    #pos_b = shape_b.body.position
    #for shape in (shape_a, shape_b):
     #   space.remove(shape_a,shape_b)
      #  shape_b = create_ballM(space,(pos_b))   
       # counter += 150

def on_collision6(arbiter, space, data):#オレンジから紫
    global counter
    shape_a, shape_b = arbiter.shapes  
    space.remove(shape_a, shape_b)
    counter +=150
    return
GAME_OVER_LINE = 250
GAME_OVER_LINE_x1 = 550
GAME_OVER_LINE_x2 = 250
GAME_OVER_DELAY = 1000
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




handler =space.add_collision_handler(1, 1)
handler.post_solve = on_collision1
handler = space.add_collision_handler(2, 2)
handler.post_solve = on_collision2 
handler = space.add_collision_handler(3, 3)
handler.post_solve = on_collision3
handler = space.add_collision_handler(4, 4)
handler.post_solve = on_collision4
handler = space.add_collision_handler(5, 5)
handler.post_solve = on_collision5
handler = space.add_collision_handler(6, 6)
handler.post_solve = on_collision6
#handler = space.add_collision_handler(7, 7)
#handler.post_solve = on_collision7

create_box(space)
create_right(space)
create_left(space)

    


# 円のリスト（位置と速度を保持）
ball = []
next_ball=deque([])
next_circle = []
# フレームレート設定
clock = pygame.time.Clock()
over = False
game_over_time = None
time_flag = 0
while True:
    # イベント処理
    current_time = pygame.time.get_ticks()
    
    if hoge < 2:
        elapsed_second = 0
    else:
        elapsed_second = (current_time - start_time) / 1000
    remain = max(0, int(time_limit - elapsed_second))
    
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.KEYDOWN and not over:
            if event.key == pygame.K_LSHIFT :
                ball.append(N)
            if event.key == pygame.K_SPACE and space_key == False :
                
                elapsed = pygame.time.get_ticks() - start_time
                next =random.choice(drop_ball)
                next_ball.append(next)
                
                
                hoge+=1
   
                if hoge >=2:
                    start_time = pygame.time.get_ticks()
                    next_circle.append(next)
                    new_circle= next_ball.popleft()
                    ball.append(new_circle)
                    last_circle = len(ball) - 1
                    range_B = 400
                    space_key = True
                

            if event.key == pygame.K_DOWN and last_circle is not None and not fall:

                fall = True

                # 今操作しているボールのX座標を保存
                x = ball[last_circle]["pos_x"]

                # 実際にPymunkへ落とす
                if new_circle == B:
                    falling_shape = create_ballB(space, (x, 150))

                elif new_circle == R:
                    falling_shape = create_ballR(space, (x, 150))

                elif new_circle == G:
                    falling_shape = create_ballG(space, (x, 150))

                # 操作用のボールをballから削除
                ball.pop(last_circle)

                last_circle = None

                range_B = 400


               
                circle["pos_x"] = 400
                #next_circle.remove(next)
                #next =random.choice(drop_ball)
                # next_ball.append(next)
                # next_circle.append(next)
                # new_circle= next_ball.popleft()
                # ball.append(new_circle)
                # last_circle = len(ball) - 1
                range_B = 400

            # スペースキーで円を追加
            
                
            
                    
                

    # キー入力の取得
    keys = pygame.key.get_pressed()
    if last_circle is not None:
        

        if keys[pygame.K_LEFT]:
            if new_circle == B and range_B<=513:
                ball[last_circle]["pos_x"] -= L
                range_B +=L
            if new_circle == R and range_B<=510:
                ball[last_circle]["pos_x"] -= L
                range_B +=L
            if new_circle == G and range_B<=509.5:
                ball[last_circle]["pos_x"] -= L
                range_B +=L
            #if new_circle == Y and range_B<=502:
                ball[last_circle]["pos_x"] -= L
                range_B +=L
            
            

            

        elif keys[pygame.K_RIGHT]:
            if new_circle == B and range_B>=283:
                ball[last_circle]["pos_x"] += L
                range_B -=L
                
            if new_circle == R and range_B>=290:
                ball[last_circle]["pos_x"] += L
                range_B -=L
            if new_circle == G and range_B>=285:
                ball[last_circle]["pos_x"] += L
                range_B -=L
            #if new_circle == Y and range_B>=296:
                ball[last_circle]["pos_x"] += L
                range_B -=L

        



    
    
    
    # GAME OVER 画像表示
    
    if not over:
        if check_game_over(space):

            if game_over_time is None:
                game_over_time = pygame.time.get_ticks()

            elif pygame.time.get_ticks() - game_over_time >= GAME_OVER_DELAY:
                over = True

        else:
            game_over_time = None

    screen.fill((135, 206, 235))

            
        
        
        #ball[last_circle]["pos_x"] = max(254+ball[last_circle]["ball_size"], min(546-ball[last_circle]["ball_size"], ball[last_circle]["pos_x"]))
        #ball[last_circle]["pos_y"] = max(0, min(550-ball[last_circle]["ball_size"]-5, ball[last_circle]["pos_y"]))
# 2/07 : 312行目と313行目をどうにかする


    # 画面を白でクリア
    
    space.step(1 / 60.0)
    space.step(1 / 60.0)

# 落としたボールが250より下に行ったら次のボールを出す
    if fall and falling_shape is not None:

        if falling_shape.body.position.y > GAME_OVER_LINE:

            # 次のボールを作る
            #new_circle = random.choice(drop_ball)

            #ball.append(new_circle)
            # NEXTを操作ボールにする
            new_circle = next_circle[0]

            ball.append(new_circle)
            last_circle = len(ball) - 1

# 新しいNEXTを作る
            next_circle[0] = random.choice(drop_ball)

            falling_shape = None
            fall = False
            range_B = 400









    # 壁を描画
    for shape in space.shapes:
        if isinstance(shape, pymunk.Segment):
            a = shape.body.local_to_world(shape.a)
            b = shape.body.local_to_world(shape.b)
            pygame.draw.line(
                screen,
                WHITE,
                (int(a.x), int(a.y)),
                (int(b.x), int(b.y)),
                4
            )




    
    for circle in ball:
        img = circle["image"]
        rect = img.get_rect(center=(circle["pos_x"], circle["pos_y"]))
        screen.blit(img, rect)
    draw_objects(screen, space)

    for circle in next_circle:
        img = circle["image"]
        rect = img.get_rect(center=(700, 120))
        screen.blit(img, rect)


    

        
    
    #space.debug_draw(draw_options)
    
    text_surface = font.render(f"SCOER: {counter}", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(700, 500))
    text_next = font.render(f"NEXT", True, (255, 255, 255))
    text_rect_n = text_surface.get_rect(center=(725, 70))
    if over or remain <=0:

        
        screen.fill((0, 0, 0))
        gameover_text = font.render(
            f"SCORE : {counter}",
            True,
            (255, 255, 255)
        )

        gameover_rect = gameover_text.get_rect(center=(400, 500))
        screen.fill((0, 0, 0))
        screen.blit(gameover_text, gameover_rect)
        screen.blit(image1, (0, 0))
    if not over and remain >= 0:
        screen.blit(text_surface, text_rect)
        screen.blit(text_next, text_rect_n)

        text_time = font.render(f"TIME : {remain}",
                    True,
                    (255, 255, 255))
        screen.blit(text_time,(100,100))
        #screen.blit(image_e,(900,200))


    # 画面更新
    
    

    # フレームレート制御
    #if over == True:
        
    pygame.display.flip()
    
    clock.tick(30)
    






   








