from typing import Any
from  pygame import*
from random import randint#бібліотеки
import time as t

init()
#розмір вікна
w = 500
h = 700


window = display.set_mode((w,h))#робемо вікно
display.set_caption("UFO")#назва вікна
display.set_icon(image.load("rocket.png"))#робемо ракету

back = transform.scale(image.load("galaxy.jpg"), (w,h))#фон гри
#clock = time.Clock()
lost = 0
killed = 0 
life = 5
"""ЗВУКИ"""
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.3)
fire = mixer.Sound('fire.ogg')
mixer_music.play()
"""ШРИВТИ"""
font.init()
font1 = font.SysFont("Arial", 30, bold=True)
font2 = font.SysFont("Arial", 60, bold=True)


"""КЛАСИ"""
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
# кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):#клас гравець
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < w -80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 10)
        bullets.add(bullet)
class Enemy (GameSprite):#клас ворог
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > h:
            self.rect.y = 0
            self.rect.x = randint(0, w - 80)
            lost += 1

class Asteror(Enemy):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > h:
            self.rect.y = 0
            self.rect.x = randint(0, w - 80)

    
class Bullet(GameSprite):#клас пуля
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill   

player = Player("rocket.png", w/2, h-100, 80, 100, 10)
enemys = sprite.Group()
bullets = sprite.Group()    
asteror = sprite.Group()

for i in range(5):
    enemy = Enemy("ufo.png", randint(0, w-80), 0, 80, 50, randint(2 , 5))
    enemy.add(enemys)

for i in range(3):
    asteror1 = Asteror("asteroid.png", randint(0, w-80), 0, 80, 50, randint(2 , 5))
    asteror.add(asteror1)

game = True#
finish = False
num_fire = 0
rel_time = False
while game:#головний цикл гри
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 7 and rel_time == False:
                    num_fire += 1
                    player.fire()
                    fire.play()
                if num_fire > 7 and rel_time is False:
                    rel_time = True
                    last_time = t.time()
                    print(last_time)





    if not finish:
        window.blit(back, (0, 0))
        player.reset()
        player.update()

        enemys.draw(window)
        enemys.update()

        asteror.draw(window)
        asteror.update()


        bullets.draw(window)
        bullets.update()

        if rel_time:
            new_time = t.time()
            if new_time - last_time < 3:
                reload_txt = font1.render('перезарядка',True, (0, 0, 0))
                window.blit(reload_txt, (w/2-100, h/2))
            else:
                rel_time = False
                num_fire = 0 
                

        lost_txt = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))#робемо напис пропущено
        window.blit(lost_txt, (10, 10))
        kill_txt = font1.render("Збито:" + str(killed), 1, (255, 255, 255))#робемо напис збито
        window.blit(kill_txt, (10, 45))
        life_txt = font2.render(str(life), 1, (0, 255, 0))# робемо щоб відображались жизні
        window.blit(life_txt, (450, 5))

        if life == 2:
                life_txt = font2.render(str(life), 1, (255,127,80))# робемо щоб відображались жизні
        if life == 1:
                life_txt = font2.render(str(life), 1, (255, 0, 0))# робемо щоб відображались жизні
        if sprite.spritecollide(player, enemys, True):
            life -= 1
            enemy = Enemy("ufo.png", randint(0, w-80),randint(-50, 0) , 80, 50, randint(1 , 3))
            enemy.add(enemys)

        collides = sprite.groupcollide(enemys, bullets, True, True)
        for col in collides:
            enemy = Enemy("ufo.png", randint(0, w-80), 0, 80, 50, randint(1 , 3))
            enemy.add(enemys)
            killed += 1
            
        if killed >= 10:
            win = font2.render('ТИ НУБ', True, (0, 200, 0))#натпис ти виграть
            window.blit(win, (w/2-100, h/2))
            finish = True

        if life == 0:
            los = font2.render('ТИ НУБ', True, (200, 0, 0))#натпис ти програти
            window.blit(los, (w/2-100, h/2))
            finish = True

        if sprite.spritecollide(player, asteror, True):
            life -= 1
            asteror1 = Asteror("asteroid.png", randint(0, w - 80), randint(-50, 0), 80, 50, randint(1, 3))
            asteror.add(asteror1)


        else:
            key_pressed = key.get_pressed()
            if key_pressed[K_r]:
                life = 5
                killed = 0
                lost = 0
                for m in enemy:
                    m.kill()
                for b in bullets:
                    b.kill()
                for i in range(5):
                    enemy = Enemy("ufo.png", randint(0, w-80), 80, 50, 
                                randint(1 , 3))
                    
                    enemys.add(enemy)
            



    display.update()


