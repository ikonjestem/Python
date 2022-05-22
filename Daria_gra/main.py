import pygame
import sys
import os


pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PROJECT_CISZKIEWICZ")

WHITE = 255, 255, 255
BLACK = 0, 0, 0

FPS = 60
VEL = 6
GRAVITY = 2


LONG_RECTANGLE_IMAGE = pygame.image.load(os.path.join('Assets', 'LONG_RECT.png'))
LONG_RECTANGLE = pygame.transform.scale(LONG_RECTANGLE_IMAGE, (60, 20))

SHORT_RECTANGLE_IMAGE = pygame.image.load(os.path.join('Assets', 'SHORT_RECT.png'))
SHORT_RECTANGLE = pygame.transform.rotate(SHORT_RECTANGLE_IMAGE, 0)

BASKETBALL_IMAGE = pygame.image.load(os.path.join('Assets', 'basketball.png'))
BASKETBALL = pygame.transform.scale(BASKETBALL_IMAGE, (40, 40))

BASKET_IMAGE = pygame.image.load(os.path.join('Assets', 'basket.png'))
BASKET = pygame.transform.scale(BASKET_IMAGE, (100, 100))
BASKET_LINE_IMAGE = pygame.image.load(os.path.join('Assets', 'basket_line.png'))
BASKET_LINE = pygame.transform.scale(BASKET_LINE_IMAGE, (100, 1))

SHORT_LINE = pygame.transform.rotate(pygame.transform.scale(BASKET_LINE_IMAGE, (40, 1)), 90)

BOARDER_X = 700
BORDER = pygame.Rect(BOARDER_X, 0, 10, HEIGHT)

FONT = pygame.font.SysFont('comicsansms', 32)
TEXT_X = 10
TEXT_Y = 10


def draw_window(short, long, ball, basket, line, score, short_line):
    WIN.fill((BLACK))
    pygame.draw.rect(WIN, WHITE, BORDER)
    WIN.blit(SHORT_RECTANGLE, (short.x, short.y))
    WIN.blit(SHORT_LINE, (short_line.x, short_line.y))
    WIN.blit(LONG_RECTANGLE, (long.x, long.y))
    WIN.blit(BASKETBALL, (ball.x, ball.y))  
    WIN.blit(BASKET,(basket.x, basket.y))
    WIN.blit(BASKET_LINE,(line.x, line.y))
    score_render = FONT.render("Score :" + str(score), True, WHITE)
    WIN.blit(score_render, (TEXT_X, TEXT_Y))
    pygame.display.update()
    
def hand_handle_movement(keys_pressed, long, short, ball, short_line):
    
    if keys_pressed[pygame.K_LEFT] and long.x - VEL > 0:
        long.x -= VEL
        short.x -= VEL
        short_line.x -= VEL
        if ball.colliderect(long):
            ball.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and long.x + VEL + long.width < BOARDER_X:
        long.x += VEL
        short.x += VEL
        short_line.x += VEL
        if ball.colliderect(long):
            ball.x += VEL
    if keys_pressed[pygame.K_UP] and short.y - VEL > 0:
        long.y -= VEL
        short.y -= VEL
        short_line.y -= VEL
        if ball.colliderect(long):
            ball.y -= VEL
    if keys_pressed[pygame.K_DOWN] and long.y + VEL + long.height < HEIGHT - 15:
        long.y += VEL
        short.y += VEL
        short_line.y += VEL
        if ball.colliderect(long):
            ball.y += VEL
        
def ball_gravity(ball, long):
    if not ball.colliderect(long):
        ball.y += GRAVITY 
        
def ball_respawn(ball):
    if ball.x < 0:
        ball.x = WIDTH // 2
        ball.y = 100
    
    if ball.x > WIDTH:
        ball.x = WIDTH // 2
        ball.y = 100
        
    if ball.y > HEIGHT:
        ball.x = WIDTH // 2
        ball.y = 100
     
    
def main():
    short = pygame.Rect(330, 250, 20, 40)
    short_line = pygame.Rect(350, 260, 1, 30)
    long = pygame.Rect(330, 290, 60, 20)
    ball = pygame.Rect(351, 250, 40, 40)
    basket = pygame.Rect(750, 400, 100, 100)
    line = pygame.Rect(750, 400, 100, 1)
    score = 0
    is_shot = False
    shot = False    
    clock = pygame.time.Clock()    
    run = True
    
    
    while run:
        
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shot = True
                    short.x += 30
                    short_line.x += 30

        if short.x > long.x:
            short.x -= 1
            
        if short_line.x > short.x + 20:
            short_line.x -= 1
            if short_line.x == long.x + 20:
                shot = False
    
        if ball.colliderect(short_line) and shot:
            is_shot = True
            
        if is_shot:
            ball.x += 5
    
        if ball.colliderect(line):
            ball.x = WIDTH // 2
            ball.y = 100
            score += 1
            is_shot = False
            
        if ball.x < 0:
            ball.x = WIDTH // 2
            ball.y = 100
            is_shot = False
    
        if ball.x > WIDTH:
            ball.x = WIDTH // 2
            ball.y = 100
            is_shot = False
            
        if ball.y > HEIGHT:
            ball.x = WIDTH // 2
            ball.y = 100 
            is_shot = False            
            
        hand_handle_movement(keys_pressed, long, short, ball, short_line)            
        draw_window(short, long, ball, basket, line, score, short_line)
        ball_gravity(ball, long)
                
    pygame.quit()
    
if __name__ == "__main__":
    main() 