""" tennis.py """

#【メモ】
#3D座標は x = 0, z = 0が画面の中心で、y = 0が画面の手前。キャラクターのx, z座標はキャラクターの中心。
#大きさ調整は、自分のy座標を-10、スクリーンのy座標を0(自分とスクリーンの距離10)とした場合、キャラクターのy座標が20の場合には3((20+10)÷10)で割り、30の場合には4((30+10)÷10)で割る計算。
#キャラクターの座標は、自分とスクリーンの距離を10とした場合、キャラクターのy座標が30の場合には、画面の中心の座標から、xを4((30+10)÷10)で割ったものを足し、キャラクターの大きさの半分を4((30+10)÷10)で割ったものをxから引く。zも同様。
#視点の調整は「係数 * y」を x や z に足す(その x や z をさらに上記の通りy座標の奥行きに合わせて割り算する)。

import math
import pygame
import random
import sys
import os
from pygame.locals import *

print(os.getcwd())
pygame.init()
pygame.key.set_repeat(5, 5)
#SURFACE = pygame.display.set_mode((1200, 600))
SURFACE = pygame.display.set_mode((600+600, 300+600)) #1000x900
FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption("AI Tennis")
sysfont = pygame.font.SysFont(None, 24)

baseline2 = 2377
baseline1 = 0
servieline2 = 1828.5
servieline1 = 548.5

court_data = (-548.5,0,543.5,2377)
fieldxl=-548.5-652
fieldxr=548.5+652
fieldy1= -612
fieldy2=2377+612
netline=1188.5
field_data = (fieldxl,fieldy1,fieldxr,fieldy2)

adjust_x = 0.1
adjust_y = 0.1
adjust_z = 0.1
mex = 0
mey = 0
mez = 0


#イメージ設定
image_court = pygame.image.load("court.png")

image_background = pygame.image.load("background.jpg")
image_title = pygame.image.load("title.png")
image_start = pygame.image.load("start.png")
image_final_bonus = pygame.image.load("final_bonus.png")
image_gameover = pygame.image.load("gameover.png")
image_shadow = pygame.image.load("shadow.gif")

#効果音
sound_frog_jump = pygame.mixer.Sound("frog_jump.wav")
sound_frog_jump.set_volume(0.2)
sound_bird_fly = pygame.mixer.Sound("bird_fly.wav")
sound_bird_fly.set_volume(0.25)
sound_jump = pygame.mixer.Sound("jump.wav")
sound_jump.set_volume(0.25)
sound_eat = pygame.mixer.Sound("eat.wav")
sound_eat.set_volume(0.3)
sound_omusubi = pygame.mixer.Sound("omusubi.wav")
sound_omusubi.set_volume(0.6)
sound_crash = pygame.mixer.Sound("crash.wav")
sound_crash.set_volume(0.4)
sound_miss = pygame.mixer.Sound("miss.wav")
sound_miss.set_volume(0.6)
sound_finish = pygame.mixer.Sound("finish.wav")
sound_finish.set_volume(0.6)

#BGM
pygame.mixer.music.load("bgm.wav")

class Character:
    """キャラクターーオブジェクト"""
    def __init__(self):
        self.status = 0
        self.jump_status = 0
        self.image_type = 0 #
        self.x = 0
        self.y = 0
        self.z = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.rotx = 0
        self.roty = 0
        self.rotz = 0
        self.width = 0
        self.height = 0
        self.mag = 1 #サイズと表示の倍率(ボールを大きく見せるため)
        self.color = (255,255,255)
        self.image_man = pygame.image.load("man.png")
        self.image_man2 = pygame.image.load("man.png")
        self.image_man3 = pygame.image.load("man3.png")
        self.image_man4 = pygame.image.load("man4.png")
        self.image_ball = pygame.image.load("TennisBall.png")

        self.image_net = pygame.image.load("net.png")
        self.image_omusubi = pygame.image.load("omusubi.gif")
        self.image_trophy = pygame.image.load("trophy.png")

    #表示オン
    def on(self, image_type):
        self.status = 1
        self.image_type = image_type
        if self.image_type == 0: #私
            self.jump_status = 1
            self.x = 0
            self.y = 0
            self.z = 0
            self.vx = 0
            self.vy = 0
            self.vz = 0
            self.width = 100
            self.height = 170
            self.image = self.image_man
        if self.image_type == 1: #ペア
            self.x = -200
            self.y = servieline1
            self.z = 0
            self.vx = 0
            self.vy = 0
            self.vz = 0
            self.color = (0,0,0)
            self.width = 100
            self.height = 170
            self.image = self.image_man
        if self.image_type == 2: #ネット
            self.x = 0
            self.y = netline
            self.z = 0
            self.vx = 0
            self.vy = 0
            self.vz = 0
            self.width = 548+548+91.4+91.4
            self.height = 91.4
            self.image = self.image_net
        if self.image_type == 3: #ボール
            self.x = -200
            self.y = baseline2
            self.z = 100
            self.vx = 0
            self.vy = -70
            self.vz = +18.0
            self.width = 30
            self.height = 30
            self.color = (255,255,0)
            self.mag = 30
            self.image = self.image_ball
        if self.image_type == 4: #相手プレーヤー
            self.x = -400
            self.y = baseline2
            self.z = 0
            self.vx = 0
            self.vy = -2
            self.vz = (random.randint(0, 1) * 2 - 1) * 5
            self.width = 100
            self.height = 100
            self.color = (26,97,167)
            self.image = self.image_man3
        if self.image_type == 5: #相手プレーヤー2
            self.x = 400
            self.y = servieline2
            self.z = 0
            self.vx = 0
            self.vy = -2
            self.vz = (random.randint(0, 1) * 2 - 1) * 5
            self.width = 100
            self.height = 100
            self.color =(255,0,0)
            self.image = self.image_man4
        if self.image_type == 10: #おむすび
            self.x = random.randint(-500, 500)
            self.y = baseline2
            self.z = 0
            self.vx = 0
            self.vy = -50
            self.vz = +20
            self.width = 60
            self.height = 40
            self.image = self.image_omusubi
        if self.image_type == 20: #トロフィ
            self.x = 0
            self.y = baseline2
            self.z = 0
            self.vx = 0
            self.vy = -10
            self.vz = 0
            self.width = 360
            self.height = 310
            self.image = self.image_omusubi

    #移動
    def move(self, x, y, z, status):
        if self.image_type == 20 : #トロファ
            selfy_old = self.y
            self.y += self.vy
            self.z += self.vz
        elif self.image_type == 10: #おむすび
            selfy_old = self.y
            self.y += self.vy
            self.z += self.vz
            self.vz -= 1
            if self.z < 0 :
                self.vy = -20
                self.vz = -self.vz *0.1
                self.z = 0

        elif self.image_type == 3: #ボール
            self.status += 1
            self.x += self.vx
            selfy_old = self.y
            self.y += self.vy
            self.z += self.vz
            self.vz -= 1
            self.vy = self.vy * 0.98
            if self.z < 0 :
                self.vz = -self.vz *0.7
                self.z = 0
            if (self.y < y and self.vy < 0):
                self.vy = 80
                self.vz = +20
            if (self.y > baseline2 and self.vy > 0):
                self.vy = -80
                self.vz = +20
#            if self.y  character[1].y and self.vz > 0
#                self.vz = -80
#                self.vz = -20
        elif (self.image_type == 4 or self.image_type == 5): #相手プレーヤー
            self.x += self.vx
            selfy_old = self.y
            self.y += self.vy
            self.z += self.vz
            if self.x > x:
                self.vx -= 1
            elif self.x < x:
                self.vx += 1
            if (self.x >= 100 and self.vx > 0) or (self.x <= -100 and self.vx < 0):
                self.vx = int(self.vx / 2)
            if self.z > +110:
                self.z = +110
                self.vz = -self.vz
            elif self.z < 0:
                self.z = 0
                self.vz = -self.vz
            if self.y <= netline + 10 and self.vy < 0 :
                self.vy = -self.vy
                self.y = netline + 10
            if self.y >= baseline2 and self.vy > 0:
                self.vy = -self.vy
                self.y = baseline2

        #スクリーンより前面(y < 0)の場合には消去
        if self.y < fieldy1 - 20:
            self.status = 0
            self.y = 0
            if self.image_type == 10:
                return(3, self.x)
            else:
                return(0, self.x)

        #衝突判定
#        if status == 1 and self.image_type <= 9: #敵衝突ミス
#            if self.status > 0 and self.y <= 1 and abs(self.x - x) < self.width / 2  + 10 and abs(self.z - z) < self.height / 2 + 40:
#                self.y = 0
#                return(1, self.x)
#            else:
#                 return(0, self.x)
        if status < 200 and self.image_type == 10: #おむすび取得
            if self.status > 0 and self.y <= y and selfy_old > y and abs(self.x - x) < self.width / 2  + 100 and abs(self.z - z) < self.height / 2 + 100:
                self.status = 0
                self.y = 0
                return(2, self.x)
            else:
                return(0, self.x)
        else:
            return(0, self.x)

    def position(self):
        return(self.x,self.y,self.z)

    #とび職男ミス
    def failure(self):
        if self.image_type == 0:
            self.image = self.image_man_failed
            self.status += 1
            if self.status >= 260:
                self.status = 10
                self.image = self.image_man

    #とび職男ミス復帰(点滅表示)
    def blink(self):
        if self.image_type == 0:
            self.status += 1
            if self.status % 10 < 5:
                self.image = self.image_man_bright
            else:
                self.image = self.image_man
            if self.status >= 70:
                self.status = 1
                self.image = self.image_man

    #とび職男フィニシュ
    def finish(self):
        if self.image_type == 0:
            self.image = self.image_man_smile

def location_in_view(x1, y1, z1):
    """ 3D座標から2D上の座標算出 """
#    x2 = int((x1 + adj_x * y1) / (y1/10 + 1)) + 200 - int(size_x * 0.5 / (y1/10 + 1))
#    z2 = int((z1 + adj_z * y1) / (y1/10 + 1)) + 150 - int(size_z * 0.5 / (y1/10 + 1))

    #カメラの位置は0,0
    #フイルムの位置は0,-10m後ろ　600x600
#    az = 0.063
#    z1 = z1 +150
#view は　0,-10m,150cm
    #レンズは0,0,0
    xl = mex
    yl = mey-1000
    zl = mez+150

    #フイルムはレンズの -1000
    yf = 1000

    x1 = x1 - xl
    y1 = y1 - yl
    z1 = z1 - zl

    if y1 <= 0 :
        y1 = 0

    x2 = int((x1+adjust_x * y1) / (y1/yf + 1))
    z2 = int((z1+adjust_z*y1) / (y1/yf + 1))

    x3 = (x2) + 300
    z3 = 600-zl - (z2)*2
#    z3 = 300 - (z2)/4
#    x1=x1/®2
#    y1=(y1+1000-adj_y)/100 #10m後ろからの視点
#    if(y1 <= 0):
#        y1 = 0
#    x2 = int((x1 + adj_x * y1) / (y1/10 + 1)) + 200 - int(size_x * 0.5 / (y1/10 + 1))
#    z2 = int((z1 + adj_z * y1) / (y1/10 + 1)) + 150 - int(size_z * 0.5 / (y1/10 + 1))
    return (x3, z3)

def size_in_view(x1,y1,z1, size_x, size_z):
    """ 3D座標から2D上のサイズ算出 """
#    az = 0
    (x2,z2) = location_in_view(x1-size_x/2,y1,z1)
    (x3,z3) = location_in_view(x1+size_x/2,y1,z1+size_z)
    return (abs(x3-x2), abs(z3-z2))

def size_in_view2(x1,y1,z1, size_x, size_y):
    """ 3D座標から2D上のサイズ算出 """
#    az = 0
    (x2,z2) = location_in_view(x1-size_x/2,y1-size_y/2,z1)
    (x3,z3) = location_in_view(x1+size_x/2,y1+size_y/2,z1)
    return (abs(x3-x2), abs(z3-z2))

def draw_character(image, x,  y, z, width, height):
    """ キャラクター描写 """
    #影表示
    if width < 300: #幅の狭いキャラクターのみ影表示
        c, d = size_in_view2(x,y,0, width, width)
        s_image = pygame.transform.scale(image_shadow, (c, d))
        s_image.set_alpha(80)
        a, b = location_in_view(x-width/2, y+width/2, 0)
        SURFACE.blit(s_image, (a, b))

    #キャラクター表示
    c, d = size_in_view(x,y,z,width, height)
#    if width >= 300 and width <= 350: #ロゴのみスムース縮小
#        image = pygame.transform.smoothscale(image, (c, d))
#    else:
    image = pygame.transform.scale(image, (c, d))
    a, b = location_in_view(x-width/2, y, z+height)
    SURFACE.blit(image, (a, b))

def location_in_view2(x1, y1, z1):
    """ 3D座標から2D上の座標算出 """
    #y1 = y1 + 10
    y1 = y1 - adjust_y
    if y1 <= 0 :
        y1 = 0

    z1 = z1 - 150

    x2 = int((x1 + adjust_x * y1) / (y1/1000 + 1)) + 300
    z2 = int((z1 + adjust_z * y1) / (y1/1000 + 1)) + 300
    return (x2, z2)


def draw_foreground(chara):
    #右のコート表示
    SURFACE.blit(image_court, (600, 0))

    #ポジションのまるを書く
    for i in chara:
        pos =(i.x/4+900,900-i.y/4-612/4)
        col=i.color
        pygame.draw.circle(SURFACE, col, pos, 10, width=0)

    pygame.draw.rect(SURFACE, (254,254,254), (0, 600, 600, 900))
#    pygame.draw.polygon(SURFACE, (189,104,86), ((0, b),(600,b),(600,600),(0,600)))

def draw_background():
    """ 背景描写 """
    line_data = [(-548.5,0,-543.5,2377),(-411.5,0,-406.5,2377),
                (-2.5,548.5,2.5,1828.5),(543.5,0,548.5,2377),
                (406.5,0,411.5,2377),(-548.5,2367,548.5,2377),
                (-2.5,2357,2.5,2377),(-411.5,1823.5,411.5,1828.5),
                (-411.5,548.5,411.5,553.5),(-2.5,0,2.5,20),
                (-548.5,0,548.5,10)]

    a, b = location_in_view(0, 4000,0) #遠景
    SURFACE.blit(image_background,(a - 300, b - 320))

    #フィールドのサイズ
    x1,y1,x2,y2 = field_data
    a, b = location_in_view(x2, y2 ,0) #地面

#    pygame.draw.rect(SURFACE, (189,104,86), (0, b, 400, 10))
    pygame.draw.polygon(SURFACE, (189,104,86), ((0, b),(600,b),(600,600),(0,600)))


    #テニスコートのサイズ　ネットの位置は1188.5
#   court_data = (-548.5,2377,543.5,0)®
    x1,y1,x2,y2 = court_data

    pygame.draw.polygon(SURFACE,(0, 128, 0), #テニスコート
                        (location_in_view(x1, y1, 0),
                         location_in_view(x2, y1, 0),
                         location_in_view(x2, y2, 0),
                         location_in_view(x1, y2, 0)))


    for i in range(len(line_data)): #ライン
        x1,y1,x2,y2 = line_data[i]
        pygame.draw.polygon(SURFACE,(255, 255, 255), #ライン描画
                        (location_in_view(x1, y1, 0),
                         location_in_view(x2, y1, 0),
                         location_in_view(x2, y2, 0),
                         location_in_view(x1, y2, 0)))


def score_indication(seta,setb,gamea,gameb,pointa,pointb):
    image = sysfont.render( #セット
        "Sets", True, (255, 255, 255))
    SURFACE.blit(image, (120, 2))
    image = sysfont.render(
        "{:0>5}-{:0>5}".format(seta,setb), True, (255, 255, 255))
    SURFACE.blit(image, (120, 17))
    image = sysfont.render( #ゲーム
        "Game", True, (255, 255, 255))
    SURFACE.blit(image, (230, 2))
    image = sysfont.render(
        "{:0>1}-{:0>1}".format(gamea,gameb), True, (255, 255, 255))
    SURFACE.blit(image, (230, 17))
    image = sysfont.render( #ポイント
        "Points", True, (255, 255, 255)) #sysfontで"Damage"と表示,ならめらかにする、色
    SURFACE.blit(image, (322, 2))
    image = sysfont.render(
        "{:>2}-{:>2}".format(pointa,pointb), True, (255, 255, 255))
    SURFACE.blit(image, (322, 17))

def main():
    """ メインルーチン """
    #変数初期設定(基本)
    global adjust_x,adjust_y,adjust_z,mex,mey,mez
    a, b, c, d = 0, 0, 0, 0
    character = [Character() for i in range(50)]
    character_copy = []
    counter = 0
    score = 0
    point_x = 0
    fullscreen_flag = 0
    doubles = 1

    #マウスカーソル非表示
    pygame.mouse.set_visible(False)

    while True:

        #変数初期設定(タイトル)
        a = 0
        title_y = 1500
        gameover_flag = 3
        damage = 0
        counter_character = 1
        counter_point = 0
        combo = 0
        seta = 0
        setb = 0
        gamea = 0
        gameb = 0
        pointa = 0
        pointb = 0

        #すべてのキャラクターを消す
        for i in range(len(character)):
            character[i].status = 0

        #自分を表示する
        character[0].on(0)

        adjust_x = character[0].x /1000
        adjust_y = character[0].y
        adjust_z = 0.1+character[0].z /1000
        mex = character[0].x
        mey = character[0].y
        mez = character[0].z

        #背景描写
        draw_background()

        #相手プレーヤー表示オン1
        character[counter_character].on(4)
        counter_character += 1

        #ボール表示オン2
        character[counter_character].on(3)
        counter_character += 1

        #ネット表示オン3
        character[counter_character].on(2)
        counter_character += 1

        #ペア表示オン4
        if doubles == 1:
            character[counter_character].on(1)
            counter_character += 1

        #相手プレーヤー2表示オン5
        if doubles == 1 :
            character[counter_character].on(5)
            counter_character += 1

        #キャラクター初期描写
        character_copy = character
        for i in range(1, len(character_copy)):
            if character_copy[i].status > 0:
                draw_character(character_copy[i].image, character_copy[i].x, character_copy[i].y, character_copy[i].z,
                               character_copy[i].width, character_copy[i].height)

        #スコア表示
        score_indication(seta,setb,gamea,gameb,pointa,pointb)

        #クレジット表示
        image = sysfont.render(
            "© 2020 KAZUOU", True, (255, 255, 255))
        SURFACE.blit(image, (125,  270))

        #画面コピー
        filler = SURFACE.copy()

        #ループ1(タイトル画面)
        while gameover_flag == 3:

            #ウィンドウ閉じるボタン
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_F11:
                    #F11でフルスクリーンモードへの切り替え
                    fullscreen_flag = not fullscreen_flag
                    if fullscreen_flag:
                        screen = pygame.display.set_mode((400, 300), FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((400, 300), 0)

            #キー入力判定
            pressed = pygame.key.get_pressed()
            if pressed[K_SPACE]:
                a = 1
            elif pressed[K_SPACE] == 0 and a == 1:
                a = 0
                gameover_flag = 0

            #画面再描写(フルスクリーン対応)
            SURFACE.blit(filler, (0,0))

            #タイトル3D表示
            title_y -= 50 if title_y > 0 else 0
            draw_character(image_title, 0, title_y,-52,  350, 103 )
            draw_character(image_start, 0, title_y, 52,  300, 35)

            if doubles == 1:
                chara=(character[0],character[1],character[4],character[5])
            else:
                chara=(character[0],character[1])

            draw_foreground(chara)

            #画面アップデート
            pygame.display.update()
            FPSCLOCK.tick(30)

        #変数初期設定(ゲーム)
        seta = 2
        setb = 1
        gamea = 5
        gameb = 3
        pointa = 15
        pointb = 0
        score = 0
        damage = 0
        counter = 0

        #BGM再生
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play()

        #ループ2(ゲームメインループ)
        while gameover_flag == 0:

            #ラウンドデータ読み込み
            #カウンター
            if character[0].status < 200 and counter < 6000:
                counter += 1
                score += 10

            #ウィンドウ閉じるボタン
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_F11:
                    #F11でフルスクリーンモードへの切り替え
                    fullscreen_flag = not fullscreen_flag
                    if fullscreen_flag:
                        screen = pygame.display.set_mode((400, 300), FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((400, 300), 0)

            #キー入力判定＆とび職人移動
            if character[0].status < 200 and counter <= 5970:
                pressed = pygame.key.get_pressed()
                if pressed[K_LEFT] and character[0].x > fieldxl+50:
                    character[0].x -= 20
                if pressed[K_RIGHT] and character[0].x < fieldxr-50:
                    character[0].x += 20
                if pressed[K_UP] and character[0].y < netline-50:
                    character[0].y += 20
                if pressed[K_DOWN] and character[0].y > fieldy1+50:
                    character[0].y -= 20
                if pressed[K_SPACE] and character[0].jump_status == 1:
                    sound_jump.play()
                    character[0].jump_status = 2
                    character[0].vz = +26
            if character[0].jump_status == 2:
                character[0].z += character[0].vz
                character[0].vz -= 2
                if character[0].z <= 0:
                    character[0].z = 0
                    character[0].jump_status = 1
            #adjust_x = character[0].x / 30
            #adjust_z = character[0].z / 20
            adjust_x = character[0].x /1000
            adjust_y = character[0].y
            adjust_z = 0.1+character[0].z /1000
            mex = character[0].x
            mey = character[0].y
            mez = character[0].z

            if counter > 5970:
                if character[0].x > 0:
                    character[0].x -= 10
                elif character[0].x < 0:
                    character[0].x += 10

            #キャラクター表示追加オン
            if character[0].status < 200:

                #おむすび表示オン
                if counter > 300 and counter < 5900 and counter % 600 == 150:
                    if character[counter_character].status == 0:
                        character[counter_character].on(10)
                    counter_character += 1
                    if counter_character >= len(character):
                        counter_character = 1

                #家表示オン
                if counter == 5802:
                    character[counter_character].on(20)
                    if counter_character >= len(character):
                        counter_character = 1

            #背景描写
            draw_background()

            #キャラクター移動
            if character[0].status < 200 and counter < 6000:
                for i in range(1, len(character)):
                    if character[i].status > 0:
                        a, b = character[i].move(character[0].x, character[0].y, character[0].z, character[0].status)
                        if a == 1: #ミス処理開始
                            character[0].status = 200
                            character[0].jump_status = 2
                            character[0].vx = 0
                            character[0].vz = -24
                            damage += 25
                            sound_crash.play()
                            sound_miss.play()
                        if a == 2: #得点処理
                            combo += 1
                            score += 1000 * combo
                            counter_point = 1
                            point_x = b - 40
                            sound_eat.play()
                            sound_omusubi.play()
                        if a == 3: #おむすび取り逃し(コンボ消滅)
                            combo = 0

            #ミス処理
            if character[0].status >= 200:
                character[0].failure()
                if damage == 100 and character[0].status == 259:
                    gameover_flag = 2
            elif character[0].status >= 10:
                character[0].blink()

            #フィニッシュ処理
            if counter == 6000:
                character[0].finish()
                score += 30000
                gameover_flag = 1
                sound_finish.play()

            #キャラクター描写順番調整(キャラクターオブジェクトをコピーしてy座標を降順で並び替え)
            character_copy = character
            #character_copy[0].y = -100 #とび職人を強制的に一番手前に
            character_copy = sorted(character_copy, key=lambda i: i.y, reverse=True)
            #character_copy[len(character_copy)-1].y = 0 #とび職人のy座標を0に戻す

            #キャラクター描写
            for i in range(len(character_copy)):
                if character_copy[i].status > 0:
                    draw_character(character_copy[i].image, character_copy[i].x, character_copy[i].y, character_copy[i].z,character_copy[i].width, character_copy[i].height)

            #ポイント表示
            if counter_point > 0:
                counter_point += 1
                a, b = location_in_view(point_x, character[0].y,0)
                image = sysfont.render(
                    "{:^10}".format("1000 x " + str(combo)), True, (255, 0, 0))
                SURFACE.blit(image, (a, b))
                if counter_point > 30:
                    counter_point = 0

            #スコア表示
            score_indication(seta,setb,gamea,gameb,pointa,pointb)

            #右のコート表示
            if doubles == 1:
                chara=(character[0],character[1],character[2],character[4],character[5])
            else:
                chara=(character[0],character[1],character[2])

            draw_foreground(chara)


            #画面アップデート
            pygame.display.update()
            FPSCLOCK.tick(30)

            #BGM再生確認&リピート
            if pygame.mixer.music.get_busy() == 0:
                pygame.mixer.music.play()

        #仕事場到着またはゲームオーバー表示
        if gameover_flag == 1:
            SURFACE.blit(image_final_bonus, (25, 70))
        else:
            SURFACE.blit(image_gameover, (50, 129))

        #画面コピー
        filler = SURFACE.copy()

        #変数初期設定(ゲームオーバー)
        a = 0
        counter2 = 0

        #ループ3(ゲームオーバー)
        while gameover_flag <= 2:

            #カウンター(ゲームオーバー処理用)
            counter2 += 1
            if counter2 >= 210:
                gameover_flag = 3

            #BGMミュート＆停止
            if counter2 <= 120:
                pygame.mixer.music.set_volume(0.4 - counter2 / 300)
            else:
             	pygame.mixer.music.stop()

            #ウィンドウ閉じるボタン
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_F11:
                    #F11でフルスクリーンモードへの切り替え
                    fullscreen_flag = not fullscreen_flag
                    if fullscreen_flag:
                        screen = pygame.display.set_mode((400, 300), FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((400, 300), 0)

            #キー入力判定
            pressed = pygame.key.get_pressed()
            if pressed[K_SPACE] == 0 and a == 0:
                a = 1
            elif pressed[K_SPACE] and a == 1:
                a = 2
            elif pressed[K_SPACE] == 0 and a == 2:
                a = 0
                gameover_flag = 3

            #画面再描写(フルスクリーン対応)
            SURFACE.blit(filler, (0,0))

            #画面アップデート
            pygame.display.update()
            FPSCLOCK.tick(30)

if __name__ == '__main__':
    main()
