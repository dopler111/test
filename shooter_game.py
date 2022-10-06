from pygame import *
from random import *
from time import time as timer
vov = 0
life = 3
num_fire = 0
rel_time = False 
WIDTH = 700
HEIGHT = 500
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
mixer.init()
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("My Game")
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,width,height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(width,height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):  
    def relod(self):
        Keys_pressed = key.get_pressed()
        if Keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x-=self.speed
        if Keys_pressed[K_d] and self.rect.x < WIDTH - 80:
            self.rect.x+=self.speed
    def fire(self):
        psi_blade_x =self.rect.centerx
        psi_blade_y = self.rect.y
        psi_blade = Bullet('boom.png',psi_blade_x,psi_blade_y  ,75,75,-10)
        psi_blades.add(psi_blade)

lost = 0
schet = 0

class Enemy(GameSprite): 
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > HEIGHT :
            lost += 1
            self.rect.y =0
            self.rect.x =randint(10,600)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self .kill()

life_color =0
kills = 0

    
psi_blades = sprite.Group()   
psi_blades2 = sprite.Group()    
player=Player('tech.png',369,400,80,80,10)
krips  = sprite.Group()
for i in range (7):
    monster = Enemy('ufo.png',randint(10,600),-10,80,70,randint(1,6))
    krips.add(monster)
for i in range (3):
    monster = Enemy('asteroid.png',randint(10,600),-10,80,70,randint(1,6))
    psi_blades2.add(monster)
font.init()
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',200)
font3 = font.SysFont('Arial',36)
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound('fire.ogg')
bg = transform.scale(image.load('galaxy.jpg'),(WIDTH,HEIGHT))

finish = False
running = True
while running:
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE :
                if num_fire < 5 and rel_time == False:
                    num_fire +=1
                    player.fire()
                    fire.play()
                if num_fire >=5 and rel_time == False:
                    rel_time = True
                    vov = timer()

    if not finish:       
        screen.blit(bg,(0,0))   
        text = font1.render('пропушено '+str(lost),1,(255,255,255))
        screen.blit(text,(5,40)  ) 
        text1 = font1.render('CЧЕТ '+str(kills),1,(255,255,255))
        screen.blit(text1,(5,15))
        krips.draw(screen)
        krips.update()       
        psi_blades.draw(screen)
        psi_blades.update()
        psi_blades2.draw(screen)
        psi_blades2.update()
        player.relod()
        player.reset()
        if rel_time == True:
            ab = timer()
            if ab - vov <= 3:
                reload = font3.render('Silence',1,(150,0,0))
                screen.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False


        collides=sprite.groupcollide(psi_blades,krips,True,True)
        for i in collides:
            monster = Enemy('ufo.png',randint(10,600),-10,80,70,randint(1,6))
            krips.add(monster)
            kills += 1
        if kills >= 5 :
            tx = font2.render('победа',20,(255,255,255))
            screen.blit(tx,(200,200))
            finish = True
        if sprite.spritecollide(player,krips,False) or sprite.spritecollide(player,psi_blades2,False) :
            sprite.spritecollide(player,krips,True)
            sprite.spritecollide(player,psi_blades2,True)
            life -= 1
        if life == 0 or lost >= 10:
            finish = True
            lose = font2.render('попуск',True,(0,0,0))
            screen.blit(lose,(200,200))
        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)
        text_life =font1.render(str(life),1,life_color)
        screen.blit(text_life,(650,10))
        display.flip()






