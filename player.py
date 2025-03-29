import pygame
from constants import PLAYER_SPEED, JUMP_STRENGTH, GRAVITY, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('assets/player.png'), (50, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.lives = 3
        self.on_ground = False  # Indica se o jogador está no chão
        self.can_jump = True  # Permite pular
        self.is_jumping = False  # Indica se o jogador está no meio de um pulo

    def move(self, keys):
        """Movimenta o jogador para a esquerda ou direita."""
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

    def jump(self):
        """Faz o jogador pular."""
        if self.can_jump and self.on_ground:  # Só permite pular se estiver no chão
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True
            self.can_jump = False
            self.on_ground = False  # O jogador não está mais no chão

    def reset_jump(self):
        """Permite que o jogador pule novamente quando ele tocar o chão."""
        if self.on_ground:
            self.can_jump = True

    def update(self):
        """Atualiza a posição do jogador."""
        # Aplica gravidade
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Impede que o jogador caia abaixo do chão
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.on_ground = True  # Permite pular novamente
        else:
            self.on_ground = False  # O jogador está no ar

    def check_boundary(self, screen_width):
        """Impede que o jogador saia da tela."""
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
