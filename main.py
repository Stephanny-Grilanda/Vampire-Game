import pygame
from constants import HEIGHT, WIDTH
from game import game_start
from menu import show_game_over, show_menu

pygame.init()
pygame.display.set_caption("A Morte do Vampiro")

window = pygame.display.set_mode((WIDTH, HEIGHT))

if __name__ == "__main__":
    while True: 
        show_menu(window)
        score = game_start(window)
        show_game_over(window, score)