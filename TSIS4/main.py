import pygame
import sys
import json

from game import SnakeGame, WIDTH, HEIGHT
from db import setup_database, get_top_10
from game import load_settings, save_settings


# Инициализация Pygame
pygame.init()

# Инициализация музыки
pygame.mixer.init()

pygame.mixer.music.load("assets/t1.mp3")
pygame.mixer.music.set_volume(0.5)


# Создание таблиц базы данных, если их нет
setup_database()

# Создание игрового окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Snake")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG = (35, 35, 35)
GREEN = (0, 220, 0)
BLUE = (80, 170, 255)
RED = (220, 0, 0)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont("Verdana", 22)
small_font = pygame.font.SysFont("Verdana", 17)
big_font = pygame.font.SysFont("Verdana", 45)

# state отвечает за текущий экран игры
state = "menu"
username = ""
game = None


# Класс кнопки для меню, настроек и экрана Game Over
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            color = (170, 220, 255)
        else:
            color = (230, 230, 230)

        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=12)

        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


# Функция рисует главный заголовок на экране
def draw_title(text):
    title = big_font.render(text, True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 90)))


# Экран для ввода имени игрока
def username_screen():
    global username, state

    username = ""

    while state == "username":
        screen.fill(BG)

        draw_title("Enter Username")

        box = pygame.Rect(150, 230, 300, 50)
        pygame.draw.rect(screen, WHITE, box, border_radius=8)
        pygame.draw.rect(screen, BLUE, box, 3, border_radius=8)

        name_text = font.render(username + "|", True, BLACK)
        screen.blit(name_text, (box.x + 10, box.y + 10))

        hint = small_font.render("Type name and press Enter", True, YELLOW)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 310)))

        # Обработка событий клавиатуры для ввода имени
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username == "":
                        username = "Player"

                    state = "game"

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    if len(username) < 12:
                        username += event.unicode

        pygame.display.flip()
        clock.tick(60)


# Главное меню игры
def menu_screen():
    global state

    play = Button(190, 180, 220, 55, "Play")
    leaderboard = Button(190, 250, 220, 55, "Leaderboard")
    settings = Button(190, 320, 220, 55, "Settings")
    quit_btn = Button(190, 390, 220, 55, "Quit")

    while state == "menu":
        screen.fill(BG)

        draw_title("Snake Pro")

        play.draw()
        leaderboard.draw()
        settings.draw()
        quit_btn.draw()

        # Обработка нажатий на кнопки меню
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if play.clicked(event):
                state = "username"

            if leaderboard.clicked(event):
                state = "leaderboard"

            if settings.clicked(event):
                state = "settings"

            if quit_btn.clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)


# Экран таблицы лидеров
def leaderboard_screen():
    global state

    back = Button(190, 520, 220, 50, "Back")

    while state == "leaderboard":
        screen.fill(BG)

        draw_title("Leaderboard")

        # Получаем топ-10 результатов из базы данных
        data = get_top_10()

        y = 155

        if len(data) == 0:
            empty = font.render("No scores yet", True, WHITE)
            screen.blit(empty, empty.get_rect(center=(WIDTH // 2, 270)))

        # Вывод результатов игроков на экран
        for i, row in enumerate(data):
            name, score, level, date = row

            text = f"{i + 1}. {name} | Score: {score} | Level: {level}"
            line = small_font.render(text, True, WHITE)
            screen.blit(line, (60, y))

            y += 35

        back.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back.clicked(event):
                state = "menu"

        pygame.display.flip()
        clock.tick(60)


# Экран настроек игры
def settings_screen():
    global state

    pygame.mixer.music.stop()

    # Загружаем сохранённые настройки из файла
    settings = load_settings()

    grid_btn = Button(160, 180, 280, 50, "")
    sound_btn = Button(160, 250, 280, 50, "")
    color_btn = Button(160, 320, 280, 50, "")
    back_btn = Button(160, 430, 280, 50, "Save & Back")

    colors = [
        [0, 255, 0],
        [255, 0, 0],
        [0, 120, 255],
        [255, 255, 0],
        [160, 32, 240]
    ]

    while state == "settings":
        screen.fill(BG)

        draw_title("Settings")

        grid_btn.text = "Grid: " + str(settings["grid"])
        sound_btn.text = "Sound: " + str(settings["sound"])
        color_btn.text = "Snake Color"

        grid_btn.draw()
        sound_btn.draw()
        color_btn.draw()
        back_btn.draw()

        # Показывает текущий цвет змейки
        pygame.draw.rect(screen, settings["snake_color"], (460, 330, 35, 35))
        pygame.draw.rect(screen, WHITE, (460, 330, 35, 35), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Включение или выключение сетки
            if grid_btn.clicked(event):
                settings["grid"] = not settings["grid"]

            # Включение или выключение звука
            if sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]

                if settings["sound"]:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

            # Смена цвета змейки
            if color_btn.clicked(event):
                current = colors.index(settings["snake_color"])
                settings["snake_color"] = colors[(current + 1) % len(colors)]

            # Сохранение настроек и возврат в меню
            if back_btn.clicked(event):
                save_settings(settings)
                state = "menu"

        pygame.display.flip()
        clock.tick(60)


# Экран после проигрыша
def game_over_screen():
    global state, game

    retry = Button(190, 390, 220, 55, "Retry")
    menu = Button(190, 470, 220, 55, "Main Menu")

    while state == "game_over":
        screen.fill((90, 0, 0))

        draw_title("Game Over")

        score_text = font.render("Score: " + str(game.score), True, WHITE)
        level_text = font.render("Level: " + str(game.level), True, WHITE)
        best_text = font.render("Personal Best: " + str(game.personal_best), True, WHITE)

        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, 210)))
        screen.blit(level_text, level_text.get_rect(center=(WIDTH // 2, 250)))
        screen.blit(best_text, best_text.get_rect(center=(WIDTH // 2, 290)))

        retry.draw()
        menu.draw()

        # Обработка кнопок Retry и Main Menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if retry.clicked(event):
                state = "game"

            if menu.clicked(event):
                pygame.mixer.music.stop()
                state = "menu"

        pygame.display.flip()
        clock.tick(60)


# Основной запуск игрового процесса
def run_game():
    global state, game

    # Запуск музыки, если звук включён в настройках
    if load_settings()["sound"]:
        pygame.mixer.music.load("assets/t1.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    # Создаём объект игры SnakeGame
    game = SnakeGame(screen, username)

    while state == "game":
        # Один кадр игры: движение, еда, столкновения, отрисовка
        over = game.run_frame()

        # Если игрок проиграл, переходим на экран Game Over
        if over:
            pygame.mixer.music.stop()
            state = "game_over"

        pygame.display.flip()
        clock.tick(game.speed)


# Главный цикл программы, который переключает экраны
while True:
    if state == "menu":
        menu_screen()

    elif state == "username":
        username_screen()

    elif state == "game":
        run_game()

    elif state == "game_over":
        game_over_screen()

    elif state == "leaderboard":
        leaderboard_screen()

    elif state == "settings":
        settings_screen()