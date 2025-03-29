import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('assets/bg_menu.png')
        self.font = pygame.font.Font(None, 36)

    def show(self, high_score):
        self.screen.blit(self.background, (0, 0))

        # Mostrar título
        title = self.font.render("Doodle Jump", True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Mostrar instruções
        instruction = self.font.render("Pressione ESPAÇO para jogar", True, (255, 255, 255))
        self.screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 200))

        # Mostrar pontuação máxima
        score_text = self.font.render(f"High Score: {high_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))

        pygame.display.flip()
