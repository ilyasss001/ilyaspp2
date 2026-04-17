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
        self.clock_img = pygame.transform.scale(self.clock_img, (800, 600))
        self.mickey = pygame.transform.scale(self.mickey, (220, 220))

        self.hand_l = pygame.transform.scale(self.hand_l, (120, 260))
        self.hand_r = pygame.transform.scale(self.hand_r, (120, 260))

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
        # 🔥 центр экрана (автоматически)
        screen_rect = screen.get_rect()
        center = screen_rect.center

        # фон часов
        clock_rect = self.clock_img.get_rect(center=center)
        screen.blit(self.clock_img, clock_rect)

        # время
        seconds_angle, minutes_angle = self.get_angles()

        # 🔥 точка вращения (чуть ниже центра = плечи)
        pivot = (center[0], center[1] + 15)

        # 🔥 offset (настроены под твою картинку)
        sec_offset = pygame.math.Vector2(0, -95)   # секундная ближе к телу
        min_offset = pygame.math.Vector2(0, -105)

        # 🔥 поменяли руки местами правильно
        min_img, min_rect = self.rotate(self.hand_l, minutes_angle, pivot, min_offset)
        sec_img, sec_rect = self.rotate(self.hand_r, seconds_angle, pivot, sec_offset)

        # порядок слоёв
        screen.blit(min_img, min_rect)

        # микки чуть ниже центра
        mic_rect = self.mickey.get_rect(center=(center[0], center[1] + 30))
        screen.blit(self.mickey, mic_rect)

        screen.blit(sec_img, sec_rect)