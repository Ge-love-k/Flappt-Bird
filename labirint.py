import pygame
import random
pygame.init()

NE_OTDAM = 336
KOTYARA = 540
CS = 60
WHITE = (255, 255, 255)

macos = pygame.display.set_mode((NE_OTDAM, KOTYARA))
clock = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird')
class Fon():
    def __init__(self):
        self.image = pygame.image.load('background.png')
        self.x1 = 0
        self.x2 = NE_OTDAM
    def draw(self):
        macos.blit(self.image, (self.x1, 0))
        macos.blit(self.image, (self.x2, 0))
    def update(self):
        self.x1 -= 1
        self.x2 -= 1
        if self.x1 <= -NE_OTDAM:
            self.x1 = NE_OTDAM
        if self.x2 <= -NE_OTDAM:
            self.x2 = NE_OTDAM

class Ground():
    def __init__(self):
        self.image = pygame.image.load('ground.png')
        self.x1 = 0
        self.x2 = NE_OTDAM
        self.y = KOTYARA - 100
    def draw(self):
        macos.blit(self.image, (self.x1, self.y))
        macos.blit(self.image, (self.x2, self.y))
    def update(self):
        self.x1 -= 2
        self.x2 -= 2
        if self.x1 <= -NE_OTDAM:
            self.x1 = NE_OTDAM
        if self.x2 <= -NE_OTDAM:
            self.x2 = NE_OTDAM            
    
class Ptica(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = pygame.image.load('bird.png')
        self.image = self.image_orig
        self.angle = 0
        self.rect = self.image.get_rect(center = (
            NE_OTDAM // 3,
            KOTYARA // 2))
        self.BaseSpeed = -2
        self.speed = self.BaseSpeed


    def draw(self):
        macos.blit(self.image, self.rect)

    def update(self, events):
        self.rect.y -= self.speed
        
        if self.speed > self.BaseSpeed or game.state == 'over':
            self.speed -= 1
        if game.state == 'play':
            if self.speed > 0:
                self.angle += 3.1415
                if self.angle > 30:
                    self.angle = 30
            elif self.speed < 0:
                self.angle -= 1
                if self.angle < -45:
                    self.angle = -45
        self.image = pygame.transform.rotate(self.image_orig, self.angle)
        if self.rect.y < 0:
            self.rect.y = 0
            game.state = 'over'
        if self.rect.bottom > KOTYARA-100:
            self.rect.bottom = KOTYARA-100
            game.state = 'over'
        if game.state == 'play':
            for eak in events:
                if eak.type == pygame.MOUSEBUTTONDOWN:
                    self.speed = 10
            if self.rect.collidelistall([pipe.top_rect, pipe.bot_rect]):
                game.state = 'over'
                self.angle = -45
class Mario():
    def __init__(self):
        self.gate = random.randint(100, KOTYARA - 200)
        self.gap = random.randint(45, 55)
        self.top_image = pygame.image.load('top-pipe.png')
        self.top_rect = self.top_image.get_rect()
        self.top_rect.bottomleft = (NE_OTDAM, self.gate-self.gap)

        self.bot_image = pygame.image.load('bot-pipe.png')
        self.bot_rect = self.bot_image.get_rect()
        self.bot_rect.topleft =  (NE_OTDAM, self.gate+self.gap)

    def draw(self):
        macos.blit(self.top_image, self.top_rect)
        macos.blit(self.bot_image, self.bot_rect)

    def update(self):
        self.top_rect.x -= 2
        self.bot_rect.x -= 2
        if self.top_rect.right < 0:
            self.gap = random.randint(45, 55)
            self.gate = random.randint(100, KOTYARA - 200)
            self.top_rect.bottomleft = (NE_OTDAM, self.gate-self.gap)
            self.bot_rect.topleft =  (NE_OTDAM, self.gate+self.gap)
            game.score += 1
            game.update_score()

class GameManager():
    def __init__(self):
        self.state = 'play'
        self.score = 0
        self.font = pygame.font.Font('Flappy-Bird.ttf', 150)
        self.font2 = pygame.font.Font(None, 30)
        self.score_text = self.font.render('0', True, (0,0,0))
        self.restart_text = self.font2.render('Нажми R для рестарта!', True, (0,0,0))
    def centerx(self, surf):
        return (NE_OTDAM // 2) - (surf.get_width() // 2)
    
    def centery(self, surf):
        return (KOTYARA // 2) - (surf.get_width() // 2)
    
    def draw_score(self):
        macos.blit(self.score_text, (self.centerx(self.score_text), 10))

    def update_score(self):
        self.score_text = self.font.render(str(self.score), True, (0,0,0))

    def draw_rest(self):
        macos.blit(self.restart_text, (self.centerx(self.restart_text), self.centery(self.restart_text)))

    def restart(self):
        self.state = 'play'
        self.score = 0
        self.update_score()
        bird.rect.center = (NE_OTDAM // 3, KOTYARA // 2)
        bird.speed = bird.BaseSpeed
        bird.angle = 0
        pipe.gap = random.randint(45, 55)
        pipe.gate = random.randint(100, KOTYARA - 200)
        pipe.top_rect.bottomleft = (NE_OTDAM, pipe.gate-pipe.gap)
        pipe.bot_rect.topleft =  (NE_OTDAM, pipe.gate+pipe.gap)


bg = Fon()
globalcs = Ground()
bird = Ptica()
pipe = Mario()
game = GameManager()
while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r and game.state == 'over':   
                game.restart()
    if game.state == 'play':
        bg.update()                    
        globalcs.update()
        pipe.update()

    bird.update(events)
    bg.draw()                    
    pipe.draw()
    globalcs.draw()
    bird.draw()
    game.draw_score()
    if game.state == 'over':
        game.draw_rest()
    pygame.display.flip()
    clock.tick(CS)
    
