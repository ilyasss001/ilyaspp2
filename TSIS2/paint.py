import pygame
import time
from datetime import datetime

from tools import flood_fill
from tools import draw_square
from tools import draw_right_triangle
from tools import draw_equilateral_triangle
from tools import draw_rhombus


pygame.init()

WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Full Paint")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GRAY = (245, 245, 245)
LIGHT_GRAY = (235, 235, 235)
DARK_GRAY = (120, 120, 120)
BORDER = (180, 180, 180)
HOVER = (210, 230, 255)
SELECTED = (170, 210, 255)

RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 165, 0)

font = pygame.font.SysFont("Verdana", 15)
small_font = pygame.font.SysFont("Verdana", 12)
text_font = pygame.font.SysFont("Verdana", 28)

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

mode = "pencil"
color = BLACK
brush_size = 5

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_position = None
text_value = ""

save_message_time = 0

buttons = []


def canvas_pos(pos):
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


def is_on_canvas(pos):
    return pos[1] >= TOOLBAR_HEIGHT


def add_button(name, rect, action_type, value):
    buttons.append({
        "name": name,
        "rect": pygame.Rect(rect),
        "action_type": action_type,
        "value": value
    })


def create_buttons():
    buttons.clear()

    x = 10
    y = 10
    w = 75
    h = 25
    gap = 5

    tool_list = [
        ("Pencil", "pencil"),
        ("Line", "line"),
        ("Rect", "rect"),
        ("Circle", "circle"),
        ("Square", "square"),
        ("R-Tri", "right_triangle"),
        ("Eq-Tri", "equilateral_triangle"),
        ("Rhombus", "rhombus"),
        ("Fill", "fill"),
        ("Text", "text"),
        ("Eraser", "eraser")
    ]

    for label, tool in tool_list:
        add_button(label, (x, y, w, h), "tool", tool)
        x += w + gap

    x = 10
    y = 50

    size_list = [
        ("Small", 2),
        ("Medium", 5),
        ("Large", 10)
    ]

    for label, size in size_list:
        add_button(label, (x, y, w, h), "size", size)
        x += w + gap

    x += 20

    color_list = [
        ("Black", BLACK),
        ("Red", RED),
        ("Green", GREEN),
        ("Blue", BLUE),
        ("Yellow", YELLOW),
        ("Purple", PURPLE),
        ("Orange", ORANGE),
        ("White", WHITE)
    ]

    for label, col in color_list:
        add_button(label, (x, y, 35, 25), "color", col)
        x += 40

    add_button("Save", (890, 50, 80, 25), "save", None)
    add_button("Clear", (890, 10, 80, 25), "clear", None)


def save_canvas():
    global save_message_time

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_{now}.png"
    pygame.image.save(canvas, filename)

    save_message_time = pygame.time.get_ticks()
    print("Saved:", filename)


def draw_shape(surface, current_mode, start, end):
    x1, y1 = start
    x2, y2 = end

    if current_mode == "line":
        pygame.draw.line(surface, color, start, end, brush_size)

    elif current_mode == "rect":
        rect = pygame.Rect(
            min(x1, x2),
            min(y1, y2),
            abs(x2 - x1),
            abs(y2 - y1)
        )
        pygame.draw.rect(surface, color, rect, brush_size)

    elif current_mode == "circle":
        dx = x2 - x1
        dy = y2 - y1
        radius = int((dx ** 2 + dy ** 2) ** 0.5)
        pygame.draw.circle(surface, color, start, radius, brush_size)

    elif current_mode == "square":
        draw_square(surface, color, start, end, brush_size)

    elif current_mode == "right_triangle":
        draw_right_triangle(surface, color, start, end, brush_size)

    elif current_mode == "equilateral_triangle":
        draw_equilateral_triangle(surface, color, start, end, brush_size)

    elif current_mode == "rhombus":
        draw_rhombus(surface, color, start, end, brush_size)


def draw_toolbar():
    mouse_pos = pygame.mouse.get_pos()

    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BORDER, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

    for button in buttons:
        rect = button["rect"]
        name = button["name"]
        action_type = button["action_type"]
        value = button["value"]

        selected = False

        if action_type == "tool" and value == mode:
            selected = True

        if action_type == "size" and value == brush_size:
            selected = True

        if action_type == "color":
            pygame.draw.rect(screen, value, rect)

            if value == color:
                pygame.draw.rect(screen, BLACK, rect, 3)
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect, 1)

        else:
            if selected:
                pygame.draw.rect(screen, SELECTED, rect)
            elif rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, HOVER, rect)
            else:
                pygame.draw.rect(screen, LIGHT_GRAY, rect)

            pygame.draw.rect(screen, DARK_GRAY, rect, 1)

            text = small_font.render(name, True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    info = f"Tool: {mode} | Brush: {brush_size}px | Ctrl+S = Save"
    screen.blit(font.render(info, True, BLACK), (500, 55))

    if pygame.time.get_ticks() - save_message_time < 2000:
        saved_text = font.render("Saved!", True, GREEN)
        screen.blit(saved_text, (800, 55))


def handle_button_click(pos):
    global mode, color, brush_size

    for button in buttons:
        if button["rect"].collidepoint(pos):
            action_type = button["action_type"]
            value = button["value"]

            if action_type == "tool":
                mode = value

            elif action_type == "size":
                brush_size = value

            elif action_type == "color":
                color = value

            elif action_type == "save":
                save_canvas()

            elif action_type == "clear":
                canvas.fill(WHITE)


create_buttons()

running = True

while running:
    screen.fill((230, 230, 230))

    # Draw canvas
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    # Canvas border
    pygame.draw.rect(
        screen,
        BORDER,
        (0, TOOLBAR_HEIGHT, WIDTH, HEIGHT - TOOLBAR_HEIGHT),
        2
    )

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and event.key == pygame.K_s:
                save_canvas()

            elif text_mode:
                if event.key == pygame.K_RETURN:
                    rendered_text = text_font.render(text_value, True, color)
                    canvas.blit(rendered_text, text_position)
                    text_mode = False
                    text_value = ""

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_value = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

            else:
                if event.key == pygame.K_d:
                    mode = "pencil"
                if event.key == pygame.K_l:
                    mode = "line"
                if event.key == pygame.K_r:
                    mode = "rect"
                if event.key == pygame.K_c:
                    mode = "circle"
                if event.key == pygame.K_q:
                    mode = "square"
                if event.key == pygame.K_t:
                    mode = "right_triangle"
                if event.key == pygame.K_y:
                    mode = "equilateral_triangle"
                if event.key == pygame.K_h:
                    mode = "rhombus"
                if event.key == pygame.K_f:
                    mode = "fill"
                if event.key == pygame.K_x:
                    mode = "text"
                if event.key == pygame.K_e:
                    mode = "eraser"

                if event.key == pygame.K_1:
                    brush_size = 2
                if event.key == pygame.K_2:
                    brush_size = 5
                if event.key == pygame.K_3:
                    brush_size = 10

                if event.key == pygame.K_a:
                    color = BLACK
                if event.key == pygame.K_z:
                    color = RED
                if event.key == pygame.K_g:
                    color = GREEN
                if event.key == pygame.K_b:
                    color = BLUE
                if event.key == pygame.K_w:
                    color = WHITE

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < TOOLBAR_HEIGHT:
                handle_button_click(event.pos)

            elif is_on_canvas(event.pos):
                drawing = True
                start_pos = canvas_pos(event.pos)
                last_pos = canvas_pos(event.pos)

                if mode == "fill":
                    flood_fill(canvas, start_pos, color)
                    drawing = False

                elif mode == "text":
                    text_mode = True
                    text_position = start_pos
                    text_value = ""
                    drawing = False

        if event.type == pygame.MOUSEMOTION:
            if drawing and is_on_canvas(event.pos):
                current_pos = canvas_pos(event.pos)

                if mode == "pencil":
                    pygame.draw.line(canvas, color, last_pos, current_pos, brush_size)
                    last_pos = current_pos

                elif mode == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, current_pos, brush_size)
                    last_pos = current_pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos is not None and is_on_canvas(event.pos):
                end_pos = canvas_pos(event.pos)

                if mode in [
                    "line",
                    "rect",
                    "circle",
                    "square",
                    "right_triangle",
                    "equilateral_triangle",
                    "rhombus"
                ]:
                    draw_shape(canvas, mode, start_pos, end_pos)

            drawing = False
            start_pos = None
            last_pos = None

    # Live preview for shapes
    if drawing and start_pos is not None and is_on_canvas(mouse_pos):
        preview_pos = canvas_pos(mouse_pos)

        if mode in [
            "line",
            "rect",
            "circle",
            "square",
            "right_triangle",
            "equilateral_triangle",
            "rhombus"
        ]:
            preview_surface = canvas.copy()
            draw_shape(preview_surface, mode, start_pos, preview_pos)
            screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))

    # Text preview + blinking cursor
    if text_mode:
        preview_text = text_font.render(text_value, True, color)

        screen.blit(
            preview_text,
            (text_position[0], text_position[1] + TOOLBAR_HEIGHT)
        )

        cursor_x = text_position[0] + preview_text.get_width()
        cursor_y = text_position[1] + TOOLBAR_HEIGHT

        if int(time.time() * 2) % 2 == 0:
            pygame.draw.line(
                screen,
                color,
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + 30),
                2
            )

    draw_toolbar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()