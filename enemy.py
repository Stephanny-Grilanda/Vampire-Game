# CLASSE INIMIGO

import pygame
from objects import Object
from os.path import join


class Enemy(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "enemy")
        self.image = pygame.image.load(join("assets-2", "enemy.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.x_vel = -3 
        self.y_vel = 0
        self.creation_time = pygame.time.get_ticks()

    def move(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def is_off_screen(self):
        return self.rect.right < 0