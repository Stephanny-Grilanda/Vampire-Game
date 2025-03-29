import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('assets/enemy.png'),(40,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0  # Inimigos começam no topo da tela
        self.velocity_y = 2  # Velocidade inicial de queda

    def update(self):
        """Atualiza a posição do inimigo."""
        self.velocity_y += GRAVITY  # Aplica gravidade
        self.rect.y += self.velocity_y

        # Remove o inimigo se ele sair da tela
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
