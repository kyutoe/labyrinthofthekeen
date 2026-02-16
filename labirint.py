# Create your game in this file!
# yzzr

from pygame import *
import os

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    
    # def update(sellf):
    #     self.rect.x += self.x_speed
    #     self.rect.y += self.y_speed
    
    def update(self):
        if pacman.rect.x <= win_width-80 and pacman.x_speed > 0 or pacman.rect.x >= 0 and pacman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if pacman.rect.y <= win_height-80 and pacman.y_speed > 0 or pacman.rect.y >= 0 and pacman.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        if self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = min(self.rect.top, p.rect.bottom)
    
    def shoot(self):
        bullet = Bullet('slash.png', self.rect.right, self.rect.centery, 30,20,10) # cari gambarnya
        bullets.add(bullet) 

class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    
    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height+10:
            self.kill()

icon_path = os.path.join('virus_logo.png') 
app_icon = image.load(icon_path)

win_width = 700
win_height = 500
display.set_caption('Labyrinth of the Keen')
display.set_icon(app_icon)
window = display.set_mode((win_width, win_height))
back = (151, 151, 143)
background_image = image.load("bg.webp").convert()


barriers = sprite.Group()
bullets = sprite.Group()
viruses = sprite.Group()


w1 = GameSprite('wall.jpeg', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('wall1.jpeg', 370, 100, 50, 400)

barriers.add(w1)
barriers.add(w2)

pacman = Player('samurai1.png', 5, win_height - 80, 80, 80, 0, 0)
finish = GameSprite('finish.png', win_width - 65, 440, 80, 80)

virus1 = Enemy('virus.png', win_width - 250,150,70,35,10)
virus2 = Enemy('virus.png', win_width - 250, 210,70,35,15)
virus3 = Enemy('virus.png', win_width - 250,283,70,35,35)
virus4 = Enemy('virus.png', win_width - 250,353,70,35,45)
virus5 = Enemy('virus.png', win_width - 250,443,70,35,75) #yey

viruses.add(virus1)
viruses.add(virus2)
viruses.add(virus3)
viruses.add(virus4)
viruses.add(virus5)

end = False
run = True
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e .type == KEYDOWN:
            if e.key == K_LEFT or e.key == K_a:
                pacman.x_speed = -5
            elif e.key == K_RIGHT or e.key == K_d:
                pacman.x_speed = 5
            elif e.key == K_UP or e.key == K_w:
                pacman.y_speed = -5
            elif e.key == K_DOWN or e.key == K_s:
                pacman.y_speed = 5
            elif e.key == K_SPACE:
                pacman.shoot()
        
        elif e .type == KEYUP:
            if e.key == K_LEFT or e.key == K_a:
                pacman.x_speed = 0
            elif e.key == K_RIGHT or e.key == K_d:
                pacman.x_speed = 0
            elif e.key == K_UP or e.key == K_w:
                pacman.y_speed = 0
            elif e.key == K_DOWN or e.key == K_s:
                pacman.y_speed = 0

    if not end:
        window.fill(back)
        pacman.update()
        bullets.update()

        pacman.reset()
        bullets.draw(window)
        barriers.draw(window)
        finish.reset()

        sprite.groupcollide(viruses, bullets, True, True)
        viruses.update()
        viruses.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)

        if sprite.spritecollide(pacman, viruses, False):
            end = True
            img = image.load('lost.png')
            d = img.get_width()//img.get_height()
            window.fill((255, 0, 0))
            window.blit(transform.scale(img, (win_width, win_height)), (0,0))
        
        if sprite.collide_rect(pacman, finish):
            end = True
            img = image.load('win.png')
            window.fill((0, 255, 0))
            window.blit(transform.scale(img, (win_width, win_height)), (0,0))

        display.update()
