import pygame
from os.path import join
from collisions import check_collisions
from constants import FPS, HEIGHT, WIDTH
from enemy import Enemy
from generators import draw_lives, draw_score, generate_enemies, generate_floor, generate_platforms, get_background
from menu import show_game_over
from objects import Block, draw
from player import Player, handle_move


def game_start(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("bg_game.png")

    pygame.mixer.music.load(join("assets-2", "game_music.mp3"))
    pygame.mixer.music.play(-1)

    block_size = 96
    player = Player(0, 100, 50, 50)  # Posiciona o jogador no limite esquerdo

    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*floor]

    offset_x = 0
    scroll_area_width = 200
    player.lives = 3
    player.score = 0

    run = True
    game_start_time = pygame.time.get_ticks()

    while run:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_ESCAPE:
                    run = False
                    return
                if event.key == pygame.K_RCTRL:  # Detecta o ataque
                    player.attack()

        player.loop(FPS)
        handle_move(player, objects)

        player.score = (current_time - game_start_time) // 1000  # 1 ponto por segundo

        generate_floor(objects, block_size, offset_x)
        generate_platforms(objects, block_size, offset_x)
        generate_enemies(objects, block_size, offset_x)

        game_over = check_collisions(player, objects)
        if game_over:
            run = False

        objects = [obj for obj in objects if not (isinstance(obj, Enemy) and obj.is_off_screen())]
        objects = [obj for obj in objects if not (isinstance(obj, Block) and obj.rect.right < offset_x - WIDTH)]

        for obj in objects:
            if isinstance(obj, Enemy):
                obj.move()

        if player.rect.top > HEIGHT:
            player.lives = 0
            run = False

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        draw(window, background, bg_image, player, objects, offset_x)
        draw_lives(window, player.lives)
        draw_score(window, player.score)

        pygame.display.update()

    pygame.mixer.music.stop()
    if player.lives <= 0:
        show_game_over(window, player.score)
    return player.score