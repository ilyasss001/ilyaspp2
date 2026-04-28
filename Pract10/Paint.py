import pygame
import math
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    current_color = (255, 0, 0) 
    mode = 'pen' 
    
    points = [] 
    drawing = False
    start_pos = None
    last_pos = None 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_r: current_color = (255, 0, 0)
                if event.key == pygame.K_g: current_color = (0, 255, 0)
                if event.key == pygame.K_b: current_color = (0, 0, 255)
                if event.key == pygame.K_w: current_color = (255, 255, 255)
                
                
                if event.key == pygame.K_1: mode = 'pen'
                if event.key == pygame.K_2: mode = 'rect'
                if event.key == pygame.K_3: mode = 'square'
                if event.key == pygame.K_4: mode = 'right_triangle'
                if event.key == pygame.K_5: mode = 'equilateral_triangle'
                if event.key == pygame.K_6: mode = 'rhombus'
                if event.key == pygame.K_7: mode = 'eraser'
                if event.key == pygame.K_8: mode = 'circle' 

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos 

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and mode not in ['pen', 'eraser']:
                    points.append((mode, current_color, (start_pos, event.pos), 2))
                drawing = False
                last_pos = None 

            if event.type == pygame.MOUSEMOTION and drawing:
                if mode == 'pen' or mode == 'eraser':
                    color = (0, 0, 0) if mode == 'eraser' else current_color
                    thick = 20 if mode == 'eraser' else 3
                    points.append(('line', color, (last_pos, event.pos), thick))
                    last_pos = event.pos 

        screen.fill((0, 0, 0))
        
        
        for shape_type, color, data, thick in points:
            if shape_type == 'line':
                pygame.draw.line(screen, color, data[0], data[1], thick)
            else:
                draw_generic_shape(screen, shape_type, color, data[0], data[1], thick)

        
        if drawing and mode not in ['pen', 'eraser']:
            draw_generic_shape(screen, mode, current_color, start_pos, pygame.mouse.get_pos(), 1)

        pygame.display.flip()
        clock.tick(60)

def draw_generic_shape(surface, shape_type, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1

    if shape_type == 'rect':
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(dx), abs(dy))
        pygame.draw.rect(surface, color, rect, thickness)

    elif shape_type == 'circle':
       
        radius = int(math.sqrt(dx**2 + dy**2))
        pygame.draw.circle(surface, color, start, radius, thickness)

    elif shape_type == 'square':
        side = max(abs(dx), abs(dy))
        rect = pygame.Rect(x1 if x2 > x1 else x1 - side, y1 if y2 > y1 else y1 - side, side, side)
        pygame.draw.rect(surface, color, rect, thickness)

    elif shape_type == 'right_triangle':
        v = [start, end, (x1, y2)]
        pygame.draw.polygon(surface, color, v, thickness)

    elif shape_type == 'equilateral_triangle':
        height = int((math.sqrt(3) / 2) * dx)
        v = [start, (x2, y1), (x1 + dx // 2, y1 - height)]
        pygame.draw.polygon(surface, color, v, thickness)

    elif shape_type == 'rhombus':
        v = [(x1 + dx // 2, y1), (x2, y1 + dy // 2), (x1 + dx // 2, y2), (x1, y1 + dy // 2)]
        pygame.draw.polygon(surface, color, v, thickness)


main()