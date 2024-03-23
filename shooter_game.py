
import random
from pygame import *

window = display.set_mode((700, 500))

bg = image.load("galaxy.jpg")
bg = transform.scale(bg, (700, 500))

game = True
clock = time.Clock()

mixer.init()
space = mixer.Sound("space.ogg")
space.play()

class Hero(sprite.Sprite):
    def __init__ (self, x, y, width, height, speed, img_name = "rocket.png"):
        self.image = image.load(img_name)
        self.image = transform.scale(self.image, (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        super().__init__()

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Hero):
    def move (self):
        keys = key.get_pressed()
        if keys [K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys [K_d] and self.rect.x < 700:
            self.rect.x += self.speed

   

    def fire(self):
        bullet = Bullet(self.rect.x, self.rect.y, 10, 10, 10, "bullet.png")
        bullets.add(bullet)

counter = 0
bullets = sprite.Group()


class Enemy (Hero):
    def move(self):
        self.rect.y += self.speed
        global counter
        if self.rect.y > 560:
            counter += 1
            self.rect.x = random.randint(50, 565)
            self.speed = random.randint(1, 4)
            self.rect.y = -100

    
class Bullet(Hero):
    def move(self):
        self.rect.y -= self.speed
        if (self.rect.y < 0):
            self.kill()



rocket = Player (350, 400, 50, 100, 5)




enemys = sprite.Group()
finish = False

for i in range(5):
    enemy1 = Enemy (random.randint(50, 565), -100, 150, 50, random.randint(1, 4), "ufo.png")
    enemys.add(enemy1)

font.init()

font1 = font.Font(None, 30)

font3 = font.Font(None, 30)
font4 = font.Font(None, 30)

lifes = 3
killed = 0

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

    window.blit(bg, (0, 0))
    if finish != True:
        print(counter)
        window.blit(font1.render(f"Лічильник пропущених {counter}", True, (255,255,255), (0,0,0)), (0, 0))
        
        window.blit(font3.render(f"Життя: {lifes}", True, (255,255,255), (0,0,0)), (15, 90))
        window.blit(font4.render(f"Збитих: {killed}", True, (255,255,255), (0,0,0)), (15, 130))

        for i in enemys:
            i.reset()
            i.move()

        for b in bullets:
            b.reset()
            b.move()

    

        list_collides = sprite.spritecollide(rocket, enemys, False)
        for collide in list_collides:
            if collide:
                lifes -= 1
                for i in enemys:
                    i.rect.y = -100    
                    i.rect.x = random.randint(50, 565)

        list_collides = sprite.groupcollide(enemys, bullets, True, True)

        for collide in list_collides:
            if collide:
                killed += 1
                enemy1 = Enemy (random.randint(50, 565), -100, 100, 30, random.randint(1, 4), "ufo.png")
                enemys.add(enemy1)

        
        rocket.reset()
        rocket.move()

    clock.tick(60)
    display.update()