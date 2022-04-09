from msilib.schema import Feature
from pygame import *
from ctypes  import *

print(windll.user32.GetSystemMetrics(0))
print(windll.user32.GetSystemMetrics(1))

mixer.init()
font.init()

balls                 = sprite.Group()

medium_font           = font.Font(None, 30) 
big_font              = font.Font(None, 50) 

screen_h, screen_w    = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)

block_size = (screen_w/100)*15

pause_text      = medium_font.render('-pause-', True, (255,202,24))
p_s             = medium_font.render('>>>press space<<<', True, (255,202,24))

background      = transform.scale(image.load('Resurses/images/background.jpg'),(screen_h, screen_w))
display.set_icon(image.load("Resurses/images/ico.bmp"))
screen          = display.set_mode((screen_h, screen_w))
display.set_caption('Pin Pong')
clock           = time.Clock()
FPS = 60

game, menu = True, True
act, pause = False, False 
wait       = False

p_y_1,p_y_2 = screen_w/2,screen_w/2

class GameSprite(sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image    = image
        self.speed    = speed
        self.rect     = self.image.get_rect()
        self.rect.x   = x
        self.rect.y   = y
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Ball(GameSprite):
    def update(self):
        global b_left, b_up, player_1, balls,act,wait,score_pleyer_2,score_pleyer_1,p_y_1,p_y_2,speed_bonus
        if b_left    == True and act == True:
            self.rect.x -= 7+speed_bonus
        if b_left    == False and act == True:
            self.rect.x += 7+speed_bonus
        if b_up      == True and act == True:
            self.rect.y -= 7+speed_bonus
        if b_up      == False and act == True:
            self.rect.y += 7+speed_bonus
        if self.rect.y <= 0:
            speed_bonus += 0.1
            b_up     = False
        if self.rect.y >= screen_w-15:
            speed_bonus += 0.1
            b_up     = True
        if sprite.spritecollide(player_1, balls, False):
            b_left   = False
            speed_bonus += 0.2
        if sprite.spritecollide(player_2, balls, False):
            b_left   = True
            speed_bonus += 0.2
        if self.rect.x <= 0:
            wait, act = True, False                 
            score_pleyer_2 += 1
        if self.rect.x >= screen_h:
            wait, act = True, False
            score_pleyer_1 += 1
        if wait == True:
            speed_bonus = 0
            p_y_1,p_y_2 = screen_w/2,screen_w/2
            self.rect.x = screen_h/2-16
            self.rect.y = screen_w/2+35

ball = balls.add(Ball(transform.scale(image.load('Resurses/images/block.png'),(15, 15)), screen_h/2-16, screen_w/2+35, 15))

while game:
    player_1 = GameSprite(transform.scale(image.load('Resurses/images/block.png'),(10, block_size)), 100, p_y_1, 15)
    player_2 = GameSprite(transform.scale(image.load('Resurses/images/block.png'),(10, block_size)), screen_h - 100, p_y_2, 15)

    keys_pressed = key.get_pressed()

    screen.blit(background,(0, 0))
    for e in event.get():
        if e.type == QUIT:
            game  = False  
        if e.type == KEYDOWN and e.key == K_ESCAPE:
            game  = False 
        if e.type == KEYDOWN and e.key == K_SPACE:
            if act == True and pause == False and menu == False:
                pause,act        = True,False
            else:
                pause,act        = False,True
            if menu == True:
                menu, act        = False,True
            if wait == True:
                wait, act        = False,True

    if act == True:
        balls.update()

    if keys_pressed[K_w] and p_y_1>0 and act == True:
        p_y_1 -= 10
    if keys_pressed[K_s] and p_y_1<screen_w-block_size and act == True:
        p_y_1 += 10
    if keys_pressed[K_UP] and p_y_2>0 and act == True:
        p_y_2 -= 10
    if keys_pressed[K_DOWN] and p_y_2<screen_w-block_size and act == True:
        p_y_2 += 10
                
    if menu == True:
        speed_bonus = 0
        pause               = False
        b_left, b_up        = True, True
        score_pleyer_1,score_pleyer_2 = 0,0
        screen.blit(p_s, (screen_h/2-100,screen_w/2))
        pause_text      = medium_font.render('-pause-', True, (255,202,24))

    if pause == True:
        screen.blit(pause_text, (screen_h/2-42,screen_w/2))

    statistic       = big_font.render(f'{score_pleyer_1} : {score_pleyer_2}', True, (255,202,24))

    screen.blit(statistic, (screen_h/2-40,20))

    player_1.reset()
    player_2.reset()
    balls.draw(screen)
    
    display.update()
    clock.tick(FPS)