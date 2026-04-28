import pygame
import datetime
import os
import pygame.math


class MickeyClock:
    def __init__(self, base_path):

        # загрузка изображений
        self.clock_img = pygame.image.load(os.path.join(base_path, 'clock.png')).convert_alpha()
        self.mickey = pygame.image.load(os.path.join(base_path, 'mUmrP.png')).convert_alpha()
        self.hand_l = pygame.image.load(os.path.join(base_path, 'hand_left.png')).convert_alpha()
        self.hand_r = pygame.image.load(os.path.join(base_path, 'hand_right.png')).convert_alpha()

        # размеры
        self.clock_img = pygame.transform.scale(self.clock_img, (600, 600))
        self.mickey = pygame.transform.scale(self.mickey, (420, 310))

        self.hand_l = pygame.transform.scale(self.hand_l, (145, 235))
        self.hand_r = pygame.transform.scale(self.hand_r, (145, 235))

    def rotate(self, image, angle, pivot, offset):
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_offset = offset.rotate(-angle)

        rect = rotated_image.get_rect(
            center=(pivot[0] + rotated_offset.x,
                    pivot[1] + rotated_offset.y)
        )
        return rotated_image, rect

    def get_angles(self):
        now = datetime.datetime.now()
        m = now.minute
        s = now.second

        seconds_angle = -(s * 6)
        minutes_angle = -(m * 6 + s * 0.1)

        return seconds_angle, minutes_angle

    def draw(self, screen):

        # центр экрана
        center = screen.get_rect().center

        # рисуем часы (фон)
        clock_rect = self.clock_img.get_rect(center=center)
        screen.blit(self.clock_img, clock_rect)

        # получаем углы
        seconds_angle, minutes_angle = self.get_angles()

        pivot = center

        # смещение (подогнано)
        sec_offset = pygame.math.Vector2(0, -85)
        min_offset = pygame.math.Vector2(0, -80)

        # вращаем
        min_img, min_rect = self.rotate(self.hand_l, minutes_angle, pivot, min_offset)
        sec_img, sec_rect = self.rotate(self.hand_r, seconds_angle, pivot, sec_offset)

        # 🔥 СНАЧАЛА МИККИ
        mic_rect = self.mickey.get_rect(center=center)
        screen.blit(self.mickey, mic_rect)

        # 🔥 ПОТОМ РУКИ (они будут поверх)
        screen.blit(min_img, min_rect)
        screen.blit(sec_img, sec_rect)