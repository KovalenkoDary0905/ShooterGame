#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

mixer.init()
#mixer.music.load("space.ogg")
#mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")

back = "ocean.jpg"
hero = "rocket.png"
enemy = "ufo.png"
bullets = "bullet.png"

win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(back), (win_width, win_height))

FPS = 60
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_width, sprite_height, sprite_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(sprite_image), (sprite_width, sprite_height))
        self.speed = sprite_speed

        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.y < 740:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(bullets, self.rect.centerx, self.rect.top, 15, 20, -10)
        bullets_group.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(50, 720)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

lost = 0
score = 0
enemy_group = sprite.Group()
for i in range(1, 6):
    enemy1 = Enemy(enemy, randint(50, 650), 0, 80, 50, randint(1, 3))
    enemy_group.add(enemy1)



bullets_group = sprite.Group()

ship = Player(hero, 400, 500, 50, 80, 5)

font.init()
my_font = font.SysFont('Arial',36)
font1 = font.SysFont('Arial' ,90)
win = font1.render('YOU WIN!!!!', True, (200, 150, 100))
lose = font1.render("YOU LOSE!!!!!", True, (200, 150, 100))
reload_time = False
num_fire = 0

finish = False
game = True 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and reload_time == False:
                    fire_sound.play()
                    ship.fire()
                    num_fire += 1
                if num_fire >= 5 and reload_time == False:
                    last_time = timer()
                    reload_time = True
    if not finish:
        collides = sprite.groupcollide(bullets_group, enemy_group, True, True)
        for c in collides:
            score += 1
            enemy1 = Enemy(enemy, randint(50, 650), 0, 80, 50, randint(1, 3))
            enemy_group.add(enemy1)
        

        window.blit(background, (0, 0))
        if reload_time == True:
            now_time = timer()
            if now_time - last_time < 5:
                reload = font1.render("Wait please", True, (200, 150, 100))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                reload_time = False
        if sprite.spritecollide(ship, enemy_group, False) or lost >= 10:
            window.blit(lose, (200,200))
            finish = True
        if score >= 10:
            window.blit(win, (200,200))
            finish  = True
        score_text = my_font.render('Счет: '+str(score), 1, (200, 200, 0))
        window.blit(score_text, (0,0))
        lost_text = my_font.render('Пропущено: '+str(lost), 1, (200, 200, 0))
        window.blit(lost_text,(0, 20))
        ship.update()
        ship.reset()
        enemy_group.update()
        enemy_group.draw(window)
        bullets_group.update()
        bullets_group.draw(window)

    else:
        lost = 0
        score = 0
        finish = False

        for b in bullets_group:
            b.kill()
        for e in enemy_group:
            e.kill()
        for i in range(1, 6):
            enemy1 = Enemy(enemy, randint(50, 650), 0, 80, 50, randint(1, 3))
            enemy_group.add(enemy1)

        time.delay(2000)


        
    display.update()
    clock.tick(FPS)

