import pygame

class Score:
    def __init__(self):
        self.current_score = 0
        self.high_score = 0
        self.font = pygame.font.Font(None, 36)

    def update(self, player_height):
        self.current_score = max(self.current_score, -int(player_height))

    def render(self, screen):
        score_text = self.font.render(f'Score: {self.current_score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

    def save_high_score(self):
        if self.current_score > self.high_score:
            self.high_score = self.current_score