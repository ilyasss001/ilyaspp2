import pygame
import math
from collections import deque


def flood_fill(surface, start_pos, fill_color):
    width, height = surface.get_size()
    x, y = start_pos

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))

    if target_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        x, y = queue.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), fill_color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))


def draw_square(surface, color, start_pos, end_pos, thickness):
    x1, y1 = start_pos
    x2, y2 = end_pos

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        x1 -= side

    if y2 < y1:
        y1 -= side

    rect = pygame.Rect(x1, y1, side, side)
    pygame.draw.rect(surface, color, rect, thickness)


def draw_right_triangle(surface, color, start_pos, end_pos, thickness):
    x1, y1 = start_pos
    x2, y2 = end_pos

    points = [
        (x1, y1),
        (x2, y1),
        (x1, y2)
    ]

    pygame.draw.polygon(surface, color, points, thickness)


def draw_equilateral_triangle(surface, color, start_pos, end_pos, thickness):
    x1, y1 = start_pos
    x2, y2 = end_pos

    side = abs(x2 - x1)

    if side == 0:
        return

    if x2 >= x1:
        p1 = (x1, y1)
        p2 = (x1 + side, y1)
    else:
        p1 = (x1, y1)
        p2 = (x1 - side, y1)

    height = int((math.sqrt(3) / 2) * side)

    if y2 < y1:
        p3 = ((p1[0] + p2[0]) // 2, y1 - height)
    else:
        p3 = ((p1[0] + p2[0]) // 2, y1 + height)

    pygame.draw.polygon(surface, color, [p1, p2, p3], thickness)


def draw_rhombus(surface, color, start_pos, end_pos, thickness):
    x1, y1 = start_pos
    x2, y2 = end_pos

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    dx = abs(x2 - x1) // 2
    dy = abs(y2 - y1) // 2

    points = [
        (cx, cy - dy),
        (cx + dx, cy),
        (cx, cy + dy),
        (cx - dx, cy)
    ]

    pygame.draw.polygon(surface, color, points, thickness)