#Create your own shooter

# 1. Import stuff
from pygame import *
from random import randint
font.init()

# 2. Create window + clock
WIDTH,HEIGHT = 800,650

window = display.set_mode((WIDTH,HEIGHT))
clock = time.Clock()


class ImageSprite(sprite.Sprite):
    # constructor function. Runs ONCE every time a new object it's created
    def __init__(self, filename, pos, size):
        super().__init__()
        self.image = image.load(filename)
        self.image = transform.scale(self.image, size)
        self.rect = Rect(pos, size)
        self.initial_pos = pos
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    def reset(self):
        self.rect.topleft = self.initial_pos
class PlayerSprite(ImageSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_s]:
            self.rect.y += 8
        if keys[K_w]:
            self.rect.y -= 8
        if keys[K_d]:
            self.rect.x += 8
        if keys[K_a]:
            self.rect.x -= 8
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
           self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


    
    def shoot(self):
        b = BulletSprite(filename='Bul.png', pos=(0,0), size=(30,30)) #Create a bullet
        b.rect.center = self.rect.midtop # Place the bullet
        bullets.add(b) # Add it to the group



    def is_colliding_with(self, other_sprite):
        col = sprite.collide_rect(self,other_sprite)
        return col



class EnemySprite(ImageSprite):
    def __init__(self,filename,pos,size,speed):
        super().__init__(filename, pos, size)
        self.speed = Vector2(speed)
    def update(self):
        self.rect.topleft += self.speed
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0,WIDTH-self.rect.width)

class BulletSprite(ImageSprite):
    def update(self):
        self.rect.y += -10
        self.rect.x += -10
        if self.rect.bottom < 0 :
            self.kill()

class TextSprite():
    def __init__(self,text,color,pos,font_size):  #pos - top-left
        self.font = font.Font(None, font_size) #create the font  None - wat font u want it 2b
        self.pos = pos
        self.color = color
        self.set_new_text(text)
    def set_new_text(self, new_text):
        self.image = self.font.render(new_text, True, self.color)
    def draw(self, surface):
        surface.blit(self.image,self.pos) #Draw the pic on surface
        super().__init__()







bg = ImageSprite(filename = 'bg.jpg',pos = (0,0),size = (WIDTH,HEIGHT))
player = PlayerSprite(filename = 'toilet.png',pos = (400,600), size = (90,90)) 
scorew = TextSprite(text = "0",color = (255,255,255),pos = (0,0),font_size = 50)
bullets = sprite.Group()
enemies = sprite.Group()
score = 0


def create_enemy():
    y = -40
    x = randint(0,WIDTH-60)
    speey = randint(4,8)
    e = EnemySprite(filename = 'poo.png',pos = (x,y) ,size = (60,60), speed = (0,speey))
    enemies.add(e)

for l in range(50):
    create_enemy()

while not event.peek(QUIT):
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.shoot()
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                player.shoot()
    bg.draw(window)
    player.draw(window)
    player.update()
    enemies.update()
    enemies.draw(window)
    bullets.draw(window)
    bullets.update()
    scorew.draw(window)
    player_hits = sprite.spritecollide(player,enemies,True)  #check collision
    for hit in player_hits:
        create_enemy()
        score -= 1
    enemy_hits = sprite.groupcollide(bullets,enemies,True,True)  #check collision
    for hit in enemy_hits:
        score += 1
        create_enemy()

    print((type(score)))
    scorew.set_new_text(str(score))
    
    display.update() # show frame to user
    clock.tick(60)
