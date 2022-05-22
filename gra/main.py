import sys
import pygame
import random
import os

from pygame.constants import JOYAXISMOTION

pygame.init()
pygame.font.init()

WIDTH = 500
HEIGHT = 700
FPS = 30
GRAVITY = 0.25
WHITE: tuple = (248, 248, 255)

END_FONT: pygame = pygame.font.SysFont('comicsans', 55)

ziomal_movement = 5
ziomal_jump = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stoner Head")

clock = pygame.time.Clock()

# images
clouds = pygame.image.load(os.path.join("assets", "clouds.png"))
clouds_2 = pygame.image.load(os.path.join("assets", "clouds_2.png"))
ziomal = pygame.image.load(os.path.join("assets", "ziomal_2.png"))
ziomal2 = pygame.image.load(os.path.join("assets", "ziomal.png"))
joint = pygame.image.load(os.path.join("assets", "jont.png"))
bonio = pygame.image.load(os.path.join("assets", "bonio.png"))
bg = pygame.image.load(os.path.join("assets", "bg.png"))

oczy_bg = pygame.image.load(os.path.join("assets", "oczy_bg.png"))
oczy1 = pygame.image.load(os.path.join("assets", "oczy1.png"))
oczy2 = pygame.image.load(os.path.join("assets", "oczy2.png"))
oczy3 = pygame.image.load(os.path.join("assets", "oczy3.png"))
oczy_1 = pygame.image.load(os.path.join("assets", "oczy_1.png"))
oczy_2 = pygame.image.load(os.path.join("assets", "oczy_2.png"))
oczy_3 = pygame.image.load(os.path.join("assets", "oczy_3.png"))

bg_y_pos = 0


ziomal_rect = ziomal.get_rect(center=(WIDTH/2, 450))

packi = []
wazony = []
main_font = pygame.font.SysFont("comicsans", 50)


def draw_bg():
    screen.blit(bg, (0, bg_y_pos))
    screen.blit(bg, (0, bg_y_pos - 1000))
    level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
    screen.blit(oczy_bg, (10, 10))
    screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))


def collisions():
    if ziomal_rect.y > HEIGHT - 50:
        ziomal_hp = 0


wave_length = 5
ziomal_hp = 100
run = True
level = 1
menu = True
while run:
    clock.tick(FPS)

    end_screen = False
    bg_y_pos += 3 * level/2

    if level <= 4:
        hp_loss = 0.3
    elif level > 4 and level <= 8:
        hp_loss = 0.5
    elif level > 8 and level <= 12:
        hp_loss = 0.6

    ziomal_hp -= hp_loss

    while menu:
        clock.tick(FPS)
        screen.blit(bg, (0, 0))
        screen.blit(clouds_2, (0, 0))
        name_label = END_FONT.render("STONER HEAD", 1, (WHITE))
        screen.blit(name_label, (50, HEIGHT/4))
        name_label = main_font.render("press key to start", 1, (WHITE))
        screen.blit(name_label, (40, HEIGHT * 2/3))
        level = 1
        wave_length = 5
        ziomal_hp = 100
        packi = []
        wazony = []
        bg_y_pos = 0
        ziomal_rect = ziomal.get_rect(center=(WIDTH/2, 450))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                run = True
                menu = False

    if ziomal_hp >= 200:
        menu = True
        print("smierc za duzo")
    elif ziomal_hp <= 0:
        menu = True
        print("smierc za malo")
    elif ziomal_rect.y >= HEIGHT:
        menu = True
        print("smierc za nisko")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and ziomal_rect.y - ziomal_jump - 150 > 0:
            ziomal_jump = 0
            ziomal_jump -= 10
        if keys[pygame.K_a] and ziomal_rect.x >= 0:
            ziomal_rect.x -= ziomal_movement
            ziomal_rect.y -= 3 * level/2
        if keys[pygame.K_d] and ziomal_rect.x + 60 < WIDTH:
            ziomal_rect.x += ziomal_movement
            ziomal_rect.y -= 3 * level/2

    draw_bg()
    if bg_y_pos >= 1000:
        bg_y_pos = 0
        level += 1

    if ziomal_hp >= 180:
        screen.blit(oczy_3, (10, 10))

    if ziomal_hp >= 150 and ziomal_hp < 180:
        screen.blit(oczy_2, (10, 10))

    if ziomal_hp >= 120 and ziomal_hp < 150:
        screen.blit(oczy_1, (10, 10))

    if ziomal_hp <= 80:
        screen.blit(oczy1, (10, 10))

    if ziomal_hp <= 50:
        screen.blit(oczy2, (10, 10))

    if ziomal_hp <= 20:
        screen.blit(oczy3, (10, 10))

    if bg_y_pos == 1000:
        level += 1

    if ziomal_rect.y >= HEIGHT:
        end_screen = True

    if len(packi) < 10:
        for i in range(wave_length):
            img = joint
            x = random.randrange(0 + 50, WIDTH - 20)
            y = random.randrange(-2000, 0)
            pacek = img.get_rect(center=(x, y))
            packi.append(pacek)
            print(len(packi))

    for pacek in packi:
        screen.blit(joint, pacek)
        pacek.y += 3

        if level > 3:
            pacek.y += level/5
        if pacek.y > HEIGHT:
            packi.remove(pacek)
        if ziomal_rect.colliderect(pacek):
            packi.remove(pacek)
            ziomal_hp += 20

    if len(wazony) < 5:
        for i in range(wave_length):
            img = bonio
            x = random.randrange(0, WIDTH - 20)
            y = random.randrange(-10000, 0)
            wazon = img.get_rect(center=(x, y))
            wazony.append(wazon)

    for wazon in wazony:
        screen.blit(bonio, wazon)
        wazon.y += 3
        if wazon.y > HEIGHT:
            wazony.remove(wazon)
        if ziomal_rect.colliderect(wazon):
            wazony.remove(wazon)
            ziomal_hp += 50

    collisions()

    ziomal_jump += GRAVITY
    ziomal_rect.centery += ziomal_jump
    screen.blit(ziomal, ziomal_rect)

    pygame.display.update()
