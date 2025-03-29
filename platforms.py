import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, is_ground=False):
        super().__init__()
        if is_ground:
            # Criar uma plataforma de chão com toda a largura da tela
            self.image = pygame.Surface((SCREEN_WIDTH, 50))
            self.image.fill((100, 100, 100))  # Cor cinza para o chão
        else:
            # Plataformas móveis
            self.image = pygame.Surface((100, 20))
            self.image.fill((255, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_ground = is_ground

    def update(self, camera_offset):
        # Apenas plataformas não-chão se movem com o deslocamento da câmera
        if not self.is_ground:
            self.rect.y -= camera_offset
            
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()