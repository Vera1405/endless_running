import pygame
from random import randint
import sys
import os


WIDTH = 800
HEIGHT = 600
size = WIDTH, HEIGHT
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
score = 0
pygame.init()


def start_screen2():
    intro_text = ["------Счёт------",
                  str(score),
                  "PRESS ANY KEY"]

    fon = pygame.transform.scale(load_image('fon.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 130
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('GREEN'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 315
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинало игры
        pygame.display.flip()
        clock.tick(FPS)

def start_screen():
    text = ["нажмите, чтобы начать",
            "",
            "удачи"]

    background = load_image('back.jpg')
    screen.blit(background, (0, 0))

    pygame.font.init()
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in text:
        string = font.render(line, 1, pygame.Color('green'))
        string_rect = string.get_rect()
        text_coord = text_coord + 10
        string_rect.top = text_coord
        string_rect.x = 300
        text_coord = text_coord + string_rect.height
        screen.blit(string, string_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fullname = 'data'+'/'+name
    try:
        if name[-2:] == 'jpg':
            image = pygame.image.load(fullname).convert()
        else:
            image = pygame.image.load(fullname).convert_alpha()
    except:
        print('Cannot load image:', name)
        raise SystemExit()

    return image


#images
RUNNING = pygame.transform.scale((pygame.image.load("girl.png")), (64, 64))
LARGE_CACTUS = pygame.transform.scale((pygame.image.load("LargeCactus1.png")), (78, 78))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = RUNNING
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 8, HEIGHT // 2)
        self.is_now_jump = False
        self.y_speed = 0
        self.JUMP_POWER = 16
        self.score = score
        self.high_score = 0

    def jump(self):
        if not self.is_now_jump:
            self.y_speed = -self.JUMP_POWER
            self.is_now_jump = True

    def update(self):
        if self.is_now_jump:
            if self.y_speed == self.JUMP_POWER:
                self.is_now_jump = False
            self.rect.y += self.y_speed
            self.y_speed += 1


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = LARGE_CACTUS
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH + randint(50, 500), HEIGHT // 2)
        self.x_speed = randint(7, 15)

    def update(self):
        if self.rect.left + 50 < 0:
            self.kill()
        global running
        self.rect.left -= self.x_speed
        if pygame.sprite.collide_rect(self, player):
            running = False


player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
start_screen()
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            player.jump()
            score += 1

    if len(all_sprites) < 2:
        obstacle = Obstacle()
        all_sprites.add(obstacle)
    all_sprites.update()
    screen.fill((220, 220, 220))
    screen.fill((20, 20, 20), rect=(0, 0, WIDTH, HEIGHT // 2 + 20))
    all_sprites.draw(screen)
    pygame.display.flip()

start_screen2()
pygame.quit()