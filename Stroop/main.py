import pygame
import random
from statistics import mean
import time
import os


pygame.font.init()


# window settings
WIDTH: int = 900
HEIGHT: int = 500
WIN: pygame = pygame.display.set_mode((WIDTH, HEIGHT))
FPS: int = 60
pygame.display.set_caption(("Stroop game"))

# colors
WHITE: tuple = (248,248,255)
BLACK: tuple = (0, 0, 0)
RED: tuple = (255, 0, 0)
GREEN: tuple = (0, 255, 0)
BLUE: tuple = (0, 0, 255)
YELLOW: tuple = (255, 255, 0)
LIGHTBLUE: tuple = (180, 181, 214)


# fonts
WORDS_FONT: pygame = pygame.font.SysFont('comicsans', 40)
TEXT_COLOR_FONT: pygame = pygame.font.SysFont('comicsans', 30)
COUNTER_FONT: pygame = pygame.font.SysFont('comicsans', 20)
TIMER_FONT: pygame = pygame.font.SysFont('comicsans', 20)
LIVES_FONT: pygame = pygame.font.SysFont('comicsans', 20)
END_FONT: pygame = pygame.font.SysFont('comicsans', 70)


class Word():

    color_list: list = [RED, GREEN, BLUE, YELLOW]
    content_list: list = ["CZERWONY", "ZIELONY", "NIEBIESKI", "ŻÓŁTY"]
    timer: int = 0

    def __init__(self, x_pos: int, y_pos: int) -> None:
        self.color = random.choice(self.color_list)
        self.content = random.choice(self.content_list)
        self.word =  WORDS_FONT.render(self.content, 1, self.color)
        self.x_pos = x_pos
        self.y_pos = y_pos

    def draw_word(self, window) -> None:
        window.blit(self.word, (self.x_pos, self.y_pos))

    def get_width(self) -> int:
        return self.word.get_width()

    def get_height(self) -> int:
        return self.word.get_height()

    def get_name(self) -> str:
        return self.content

    def get_rectangle(self) -> pygame:
        return self.word.get_rect()

    def return_position(self) -> tuple:
        return (self.x_pos, self.y_pos)

    def timer_start(self) -> None:
        self.timer += 1

    def timer_stop(self) -> int:
        return self.timer

    def delete() -> None:
        None

# handle clicking
def handle_click(words: list, typed_name: str) -> bool:
    mouse_position: pygame = pygame.mouse.get_pos()

    for word in words:
        new_rect: pygame = pygame.Rect(word.x_pos, word.y_pos, word.get_width(), word.get_height())

        if new_rect.collidepoint(mouse_position):

            if word.get_name() == typed_name:
                words.remove(word)
                time = word.timer_stop()
                return (True, time)


# endscreen definiton
def draw_start_screen():
    WIN.fill(BLACK)
    text_end: pygame = END_FONT.render("STROOP GAME", 1, WHITE)
    WIN.blit(text_end, (WIDTH//2 - text_end.get_width()//2, HEIGHT* 1/3))
    text_new_game: pygame = WORDS_FONT.render("Naciśnij dowolony klawisz by rozpocząć", 1, WHITE)
    WIN.blit(text_new_game, (WIDTH//2 - text_new_game.get_width()//2, HEIGHT * 1/2))
    
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def draw_end_screen(timer_mean, global_counter):
    WIN.fill(LIGHTBLUE)
    text_end: pygame = END_FONT.render("STROOP GAME", 1, WHITE)
    WIN.blit(text_end, (WIDTH//2 - text_end.get_width()//2, HEIGHT* 1/6))
    text_timer: pygame = WORDS_FONT.render("Średni czas reakcji: " + str(timer_mean) + " s", 1, WHITE)
    WIN.blit(text_timer, (WIDTH//2 - text_timer.get_width()//2, HEIGHT* 1/4))
    text_counter: pygame = WORDS_FONT.render("Wynik: " + str(global_counter), 1, WHITE)
    WIN.blit(text_counter, (WIDTH//2 - text_counter.get_width()//2, HEIGHT* 1/3))
    text_new_game: pygame = WORDS_FONT.render("Naciśnij dowolony klawisz by kontynuować", 1, WHITE)
    WIN.blit(text_new_game, (WIDTH//2 - text_new_game.get_width()//2, HEIGHT * 4/5))
    
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def main() -> None:
    # main function variables
    clock: pygame = pygame.time.Clock()
    run: bool = True

    words: list[Word] = []
    wave_length: int = 10
    counter: int = 0
    timer_mean: float = 0
    lives: int = 3
    time_lst: list[int] = []
    velocity: int = 2
    level: int = 1
    start_game: bool = True

    content_list: list = ["CZERWONY", "ZIELONY", "NIEBIESKI", "ŻÓŁTY"]
    typed_name = random.choice(content_list)

    # redraw function definition
    def redraw_window(back_color: tuple, typed_name: str, counter: int) -> None:

        WIN.fill(back_color)

        text_color: pygame = TEXT_COLOR_FONT.render(typed_name, 1, BLACK)
        text_counter: pygame = COUNTER_FONT.render("Punkty: " + str(counter), 1, BLACK)
        text_timer: pygame = COUNTER_FONT.render("Średni czas: " + str(timer_mean) + " s", 1, BLACK)
        text_lives: pygame = COUNTER_FONT.render("Pozostałe życia: " + str(lives), 1, BLACK)
        text_level: pygame = COUNTER_FONT.render("Poziom: " + str(level), 1, BLACK)
        WIN.blit(text_color, (WIDTH//2 - text_color.get_width()//2, 10))
        WIN.blit(text_counter, (WIDTH//2 - text_counter.get_width() - 10, 30))
        WIN.blit(text_timer, (WIDTH//2 + 10, 30))
        WIN.blit(text_lives, (WIDTH//2 - text_lives.get_width()//2, 50))
        WIN.blit(text_level, (WIDTH//2 - text_level.get_width()//2 - 150, 50))
      
        for word in words:
            word.draw_word(WIN)
            word.x_pos += velocity
            if word.x_pos > -50:
                word.timer_start()
                      
        pygame.display.update()

    while run:
        clock.tick(FPS)
        
        if start_game:
            draw_start_screen()
            start_game = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                click: tuple = handle_click(words, typed_name)
                if click == None:
                    lives -= 1                   

                elif click[0]:
                    counter += 1
                    time_lst.append(click[1])
                    timer_mean = round(mean(time_lst) / FPS, 2)            
                                
        # draw words
        if len(words) < 15:
            for _ in range(wave_length):
                
                while True:
                    
                    x: int = random.randrange(-2000, -100)
                    y: int = random.randrange(50, HEIGHT - 70)
                    word: Word = Word(x, y)

                    new_rect: pygame = pygame.Rect(x, y, word.get_width(), word.get_height())
                    if not any(word for word in words if new_rect.colliderect(word.x_pos, word.y_pos, word.get_width(), word.get_height())):
                        break
                
                words.append(word)

        if lives <= 0:
            draw_end_screen(timer_mean, counter)
            words: list[Word] = []
            wave_length: int = 10
            counter: int = 0
            timer_mean: float = 0
            lives: int = 3
            time_lst: list[int] = []
            level: int = 1
            break   

        for word in words:
            if word.get_name() == typed_name and word.x_pos > WIDTH:
                words.remove(word)
                lives -= 1
            elif word.x_pos > WIDTH:
                words.remove(word)

        if counter == 5:
            counter = 0
            lives += 1
            velocity += 1
            wave_length += 5
            level += 1
   
        redraw_window(WHITE, typed_name, counter)
        
    main()


if __name__ == "__main__":
    main()