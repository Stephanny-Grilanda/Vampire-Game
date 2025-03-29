import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game
from menu import Menu

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Doodle Jump')
    clock = pygame.time.Clock()

    high_score = 0

    while True:
        # Criar e mostrar o menu
        menu = Menu(screen)
        menu.show(high_score)

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False  # Sai do loop ao pressionar espaço

        # Criar o jogo
        game = Game(screen)
        game_over = False

        while not game_over:
            # Captura eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Atualiza o jogo
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:  # Verifica se a barra de espaço foi pressionada
                game.player.jump()
            else:
                game.player.reset_jump()

            game.update(keys)  # Atualiza o estado do jogo
            game.render()      # Renderiza o jogo

            # Verifica se o jogo terminou
            if game.player.lives <= 0:
                game_over = True
                high_score = max(high_score, game.score.current_score)

            clock.tick(FPS)

if __name__ == "__main__":
    main()
