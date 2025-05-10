import pygame
import sys  # Importa o módulo sys
from os.path import join

from constants import HEIGHT, WIDTH

def show_menu(window):
    pygame.mixer.music.load(join("assets-2", "menu_music.mp3")) 
    pygame.mixer.music.play(-1) 

    bg_image = pygame.image.load(join("assets-2", "bg_menu.png")).convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    font = pygame.font.Font(join("assets-2", "creepster.ttf"), 60)
    title_text = font.render("A Morte do Vampiro", True, (255, 0, 0)) 
    start_text = font.render("Aperte ENTER para jogar", True, (255, 255, 255)) 
    quit_text = font.render("Aperte ESC para sair", True, (255, 255, 255))

    shadow_offset = 2
    shadow_color = (0, 0, 0)
    window.blit(font.render("A Morte do Vampiro", True, shadow_color), 
                (WIDTH // 2 - title_text.get_width() // 2 + shadow_offset, HEIGHT // 3 + shadow_offset))

    run = True
    while run:
        window.blit(bg_image, (0, 0)) 
        window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        window.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        window.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Substitui quit() por sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  # Substitui quit() por sys.exit()

    pygame.mixer.music.stop()

# MENU DE GAME OVER

def show_game_over(window, score):
    pygame.mixer.music.load(join("assets-2", "menu_music.mp3"))
    pygame.mixer.music.play(-1)

    bg_image = pygame.image.load(join("assets-2", "bg_menu.png")).convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    font = pygame.font.Font(join("assets-2", "creepster.ttf"), 60)
    title_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Sua Pontuação: {score}", True, (255, 255, 255))
    retry_text = font.render("Aperte ENTER para jogar novamente", True, (255, 255, 255))
    quit_text = font.render("Aperte ESC para sair", True, (255, 255, 255))

    run = True
    while run:
        window.blit(bg_image, (0, 0))
        window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
        window.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 50))
        window.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 120))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Substitui quit() por sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  # Substitui quit() por sys.exit()

    pygame.mixer.music.stop()