from pygame import *

from random import *

img_back='3jpg.jpg'
img_hero = 'istr.png'
img_enemy = 'wing.png'
img_enemy2 = 'bom.png'
font.init()
font2 = font.SysFont('Arial',36)
font3 = font.SysFont('Arial', 100)
img_bullet='bullet.png'

score = 0
lost = 0


mixer.init()
mixer.music.load('sme.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image=transform.scale(image.load(player_image),(size_x,size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect() 
        self.rect.x=player_x
        self.rect.y=player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost+1
class Enemy2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost+1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 1200
win_height = 800

window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 150, 100, 20)
monsters = sprite.Group()
monsters2 = sprite.Group()
bullets=sprite.Group()
for i in range(randint(1,6)):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 140, 90, randint(1, 5))
    monsters.add(monster)
for i in range(randint(1,3)):
    monster2 = Enemy(img_enemy2, randint(80, win_width - 80), -40, 200, 150, randint(1, 3))
    monsters2.add(monster2)

win=font3.render('Ты выиграл!',1, (255,255,255))

lose=font3.render('Ты проиграл!',1, (128, 0, 0))
life = 100



finish = False
run=True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background,(0,0))
        text = font2.render('Счет:' + str(score), 1, (255,255,255))
        window.blit(text,(10,20))
        text_lose = font2.render('Пропущено:' + str(lost), 1,(255,255,255))
        window.blit(text_lose,(10,50))

        ser = font2.render('Броня:'+ str(life), 1, (255,255,255))
        window.blit(ser, (10, 80))
        lose = font3.render('Ты проиграл!',1,(255,255,255))
        
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, monsters2, False):
            if lost > 100:
                finish =True
                window.blit(lose,(350, 350))
            if life == 0:
                finish = True
                window.blit(lose, (350, 350))
            life = life - 1



        

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80,win_width - 80), -40, 140, 90, randint (1, 5))
            monsters.add(monster)

        # if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, monsters2, False) or lost >= 1:
        #     finish = True 
        #     window.blit(lose,(350, 350))
        if lost >=5:  
            finish = True 
            window.blit(lose,(350, 350))
        if score >= 5:
            finish = True
            window.blit(win, (370,350))
        if score >= 100:
            finish = True
            window.blit(lose, (350,350))

        # display.set_caption('От Винта!')

        ship.update()
        ship.reset()

        monsters.update()
        monsters.draw(window)

        monsters2.update()
        monsters2.draw(window)

        bullets.update()
        bullets.draw(window)



        display.update()

    time.delay(50)