import pygame
import random
import json
import sys
from db import save_result, get_personal_best


WIDTH, HEIGHT = 600, 600
CELL = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BG = (25, 25, 25)
GRID_COLOR = (50, 50, 50)
RED = (255, 0, 0)
DARK_RED = (120, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 120, 255)
PURPLE = (160, 32, 240)
ORANGE = (255, 165, 0)
GRAY = (120, 120, 120)


# Загружает настройки игры из settings.json
def load_settings():
    with open("settings.json", "r", encoding="utf-8") as file:
        return json.load(file)


# Сохраняет настройки игры в settings.json
def save_settings(settings):
    with open("settings.json", "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


# Главный класс игры Snake
class SnakeGame:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username

        self.settings = load_settings()

        self.font = pygame.font.SysFont("Verdana", 20)
        self.big_font = pygame.font.SysFont("Verdana", 45)

        # Получаем лучший результат игрока из базы данных
        self.personal_best = get_personal_best(username)

        self.reset()

    # Сбрасывает игру в начальное состояние
    def reset(self):
        self.snake = [(100, 100)]
        self.dx = CELL
        self.dy = 0

        self.score = 0
        self.level = 1
        self.speed = 10
        self.food_eaten = 0

        self.obstacles = []

        self.food_lifetime = 5000
        self.food = self.generate_food()

        self.poison = self.generate_poison()

        self.powerup = None
        self.powerup_spawn_time = 0
        self.powerup_lifetime = 8000

        self.active_power = None
        self.power_end_time = 0
        self.shield = False

        self.obstacles = []

        self.running = True
        self.game_over = False
        self.saved = False

    # Ищет свободную клетку, где нет змейки и препятствий
    def free_position(self):
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)

            pos = (x, y)

            if pos not in self.snake and pos not in self.obstacles:
                return pos

    # Создаёт еду с разным весом и цветом
    def generate_food(self):
        x, y = self.free_position()

        weight = random.choice([1, 2, 3])

        if weight == 1:
            color = RED
        elif weight == 2:
            color = YELLOW
        else:
            color = BLUE

        spawn_time = pygame.time.get_ticks()

        return {
            "pos": (x, y),
            "weight": weight,
            "color": color,
            "spawn_time": spawn_time
        }

    # Создаёт ядовитую еду
    def generate_poison(self):
        x, y = self.free_position()

        return {
            "pos": (x, y),
            "color": DARK_RED
        }

    # Создаёт случайный power-up
    def generate_powerup(self):
        kind = random.choice(["speed", "slow", "shield"])
        x, y = self.free_position()

        if kind == "speed":
            color = ORANGE
        elif kind == "slow":
            color = PURPLE
        else:
            color = BLUE

        self.powerup = {
            "pos": (x, y),
            "kind": kind,
            "color": color,
            "spawn_time": pygame.time.get_ticks()
        }

    # Создаёт препятствия на поле
    def generate_obstacles(self):
        self.obstacles = []

        count = min(5 + self.level, 14)

        head = self.snake[0]

        while len(self.obstacles) < count:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)

            pos = (x, y)

            near_head = abs(x - head[0]) <= CELL * 2 and abs(y - head[1]) <= CELL * 2

            if pos not in self.snake and not near_head:
                self.obstacles.append(pos)

    # Применяет эффект выбранного power-up
    def apply_powerup(self, kind):
        if kind == "speed":
            self.active_power = "speed"
            self.power_end_time = pygame.time.get_ticks() + 5000
            self.speed += 5

        elif kind == "slow":
            self.active_power = "slow"
            self.power_end_time = pygame.time.get_ticks() + 5000
            self.speed = max(5, self.speed - 5)

        elif kind == "shield":
            self.active_power = "shield"
            self.shield = True

    # Проверяет, закончился ли эффект power-up
    def update_powerup_timer(self):
        if self.active_power in ["speed", "slow"]:
            if pygame.time.get_ticks() > self.power_end_time:
                self.active_power = None
                self.speed = 10 + (self.level - 1) * 2

    # Обрабатывает столкновение, если есть shield
    def handle_collision(self):
        if self.shield:
            self.shield = False
            self.active_power = None

            self.snake[0] = (WIDTH // 2, HEIGHT // 2)

            return False

        return True

    # Обновляет состояние игры каждый кадр
    def update(self):
        # Управление змейкой с клавиатуры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.dy == 0:
                    self.dx, self.dy = 0, -CELL

                if event.key == pygame.K_DOWN and self.dy == 0:
                    self.dx, self.dy = 0, CELL

                if event.key == pygame.K_LEFT and self.dx == 0:
                    self.dx, self.dy = -CELL, 0

                if event.key == pygame.K_RIGHT and self.dx == 0:
                    self.dx, self.dy = CELL, 0

        head = self.snake[0]
        new_head = (head[0] + self.dx, head[1] + self.dy)

        # Проверка столкновения со стеной
        wall_hit = (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT
        )

        self_hit = new_head in self.snake
        obstacle_hit = new_head in self.obstacles

        # Если есть столкновение, игра заканчивается или shield спасает
        if wall_hit or self_hit or obstacle_hit:
            if self.handle_collision():
                self.end_game()
                return

        # Добавляем новую голову змейки
        self.snake.insert(0, new_head)

        current_time = pygame.time.get_ticks()

        # Если еда долго не съедена, она исчезает
        if current_time - self.food["spawn_time"] > self.food_lifetime:
            self.food = self.generate_food()

        # Если змейка съела обычную еду
        if new_head == self.food["pos"]:
            self.score += self.food["weight"]
            self.food_eaten += 1

            self.food = self.generate_food()

            # Каждые 4 еды повышается уровень
            if self.food_eaten % 4 == 0:
                self.level += 1
                self.speed += 2

                if self.level >= 3:
                    self.generate_obstacles()

        # Если змейка съела яд
        elif new_head == self.poison["pos"]:
            self.score = max(0, self.score - 2)

            for i in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()

            self.poison = self.generate_poison()

            if len(self.snake) <= 1:
                self.end_game()
                return

        # Если змейка взяла power-up
        elif self.powerup is not None and new_head == self.powerup["pos"]:
            if self.active_power is None or self.powerup["kind"] == "shield":
                self.apply_powerup(self.powerup["kind"])

            self.powerup = None

        else:
            self.snake.pop()

        # Случайное появление power-up
        if self.powerup is None:
            if random.randint(1, 200) == 1:
                self.generate_powerup()
        else:
            # Power-up исчезает, если его долго не взять
            if current_time - self.powerup["spawn_time"] > self.powerup_lifetime:
                self.powerup = None

        self.update_powerup_timer()

    # Завершает игру и сохраняет результат
    def end_game(self):
        if not self.saved:
            save_result(self.username, self.score, self.level)
            self.saved = True

        self.game_over = True

    # Рисует сетку на экране
    def draw_grid(self):
        if not self.settings["grid"]:
            return

        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y))

    # Рисует все объекты игры
    def draw(self):
        self.screen.fill(DARK_BG)

        self.draw_grid()

        # Рисуем препятствия
        for block in self.obstacles:
            pygame.draw.rect(
                self.screen,
                GRAY,
                (block[0], block[1], CELL, CELL),
                border_radius=4
            )

        # Рисуем змейку
        for i, segment in enumerate(self.snake):
            base_color = self.settings["snake_color"]
            green = max(60, base_color[1] - i * 4)
            color = (base_color[0], green, base_color[2])

            pygame.draw.rect(
                self.screen,
                color,
                (segment[0], segment[1], CELL, CELL),
                border_radius=5
            )

        # Рисуем еду
        fx, fy = self.food["pos"]

        pygame.draw.rect(
            self.screen,
            self.food["color"],
            (fx, fy, CELL, CELL),
            border_radius=5
        )

        # Рисуем яд
        px, py = self.poison["pos"]

        pygame.draw.rect(
            self.screen,
            self.poison["color"],
            (px, py, CELL, CELL),
            border_radius=5
        )

        # Рисуем power-up
        if self.powerup is not None:
            ux, uy = self.powerup["pos"]

            pygame.draw.circle(
                self.screen,
                self.powerup["color"],
                (ux + CELL // 2, uy + CELL // 2),
                CELL // 2
            )

        # Текст очков, уровня и рекорда
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        level_text = self.font.render("Level: " + str(self.level), True, WHITE)
        best_text = self.font.render("Best: " + str(self.personal_best), True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 35))
        self.screen.blit(best_text, (10, 60))

        # Показывает активный power-up
        if self.active_power:
            if self.active_power in ["speed", "slow"]:
                left = max(0, (self.power_end_time - pygame.time.get_ticks()) // 1000)
                text = f"Power: {self.active_power} {left}s"
            else:
                text = "Power: shield"

            power_text = self.font.render(text, True, YELLOW)
            self.screen.blit(power_text, (360, 10))

    # Один кадр игры: обновление + отрисовка
    def run_frame(self):
        self.update()
        self.draw()

        return self.game_over