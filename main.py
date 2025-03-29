import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    """
    Carrega o bloco do arquivo tile.png e mantém o tamanho especificado.
    """
    path = join("assets-2", "tile.png")  # Caminho para o novo arquivo de bloco
    image = pygame.image.load(path).convert_alpha()

    # Redimensiona a imagem para o tamanho do bloco especificado
    block = pygame.transform.scale(image, (size, size))

    return block


class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(join("assets-2", "player.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(width * 1.8), int(height * 1.8)))  # Redimensiona o vampiro
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x_vel = 0
        self.y_vel = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.lives = 3  # Número inicial de vidas

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel

    def move_right(self, vel):
        self.x_vel = vel

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Enemy(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "enemy")
        self.image = pygame.image.load(join("assets-2", "enemy.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))  # Redimensiona o inimigo
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # Cria a máscara baseada na imagem
        self.x_vel = -3  # Velocidade horizontal do inimigo
        self.y_vel = 0  # Velocidade vertical do inimigo

    def move(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def is_off_screen(self):
        return self.rect.right < 0 or self.rect.left > WIDTH or self.rect.top > HEIGHT


def get_background(name):
    path = join("assets-2", name)  # Ajustado para usar a pasta assets-2
    image = pygame.image.load(path).convert_alpha()

    # Redimensionar o background para o tamanho da tela
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))

    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def show_menu(window):
    """
    Exibe o menu inicial com a música e o fundo.
    """
    pygame.mixer.music.load(join("assets-2", "menu_music.mp3"))  # Carrega a música do menu
    pygame.mixer.music.play(-1)  # Toca a música em loop

    bg_image = pygame.image.load(join("assets-2", "bg_menu.png")).convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))  # Redimensiona o fundo do menu

    font = pygame.font.SysFont("Arial", 50)
    title_text = font.render("A Morte do Vampiro", True, (255, 255, 255))
    start_text = font.render("Aperte ENTER para jogar", True, (255, 255, 255))
    quit_text = font.render("Aperte ESC para sair", True, (255, 255, 255))  # Texto para sair do jogo

    run = True
    while run:
        window.blit(bg_image, (0, 0))  # Desenha o fundo do menu
        window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        window.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        window.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 60))  # Exibe a opção de sair

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER para iniciar o jogo
                    run = False
                if event.key == pygame.K_ESCAPE:  # Q para sair do jogo
                    pygame.quit()
                    quit()

    pygame.mixer.music.stop()  # Para a música do menu


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if not isinstance(obj, Enemy):  # Ignora inimigos
            if pygame.sprite.collide_mask(player, obj):
                if dy > 0:
                    player.rect.bottom = obj.rect.top
                    player.landed()
                elif dy < 0:
                    player.rect.top = obj.rect.bottom
                    player.hit_head()

                collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()


def generate_platforms(objects, block_size, offset_x):
    """
    Gera plataformas dinamicamente à frente do jogador.
    """
    # Define a distância máxima para gerar plataformas à frente
    max_distance = offset_x + WIDTH

    # Garante que sempre existam plataformas à frente do jogador
    while len(objects) < 20:  # Limita o número de plataformas na tela
        x = random.randint(max_distance, max_distance + block_size * 3)  # Gera à frente
        y = random.randint(HEIGHT // 2, HEIGHT - block_size * 2)  # Altura aleatória
        objects.append(Block(x, y, block_size))


def generate_enemies(objects, block_size, offset_x):
    """
    Gera inimigos dinamicamente, aparecendo de cima ou da direita.
    A frequência de spawn aumenta conforme o jogador avança.
    """
    # Aumenta a frequência de spawn com base no progresso do jogador
    progress_factor = max(1, offset_x // 500)  # Aumenta a dificuldade a cada 500 pixels
    spawn_chance = random.randint(1, max(100 - progress_factor * 2, 10))  # Reduz o intervalo de spawn

    # Garante que inimigos sejam gerados continuamente
    if spawn_chance <= 2:  # Aumenta a chance de spawn (ajustado dinamicamente)
        spawn_type = random.choice(["top", "right"])  # Escolhe o tipo de spawn

        for _ in range(progress_factor):  # Gera múltiplos inimigos com base no progresso
            if spawn_type == "top":
                # Spawn no topo da tela
                x = random.randint(offset_x, offset_x + WIDTH - block_size)
                y = -block_size  # Fora da tela, no topo
                enemy = Enemy(x, y, block_size // 2, block_size // 2)  # Inimigo menor que os blocos
                enemy.y_vel = 3  # Velocidade para descer

            elif spawn_type == "right":
                # Spawn na direita, com a base rente ao chão
                x = offset_x + WIDTH  # Ajusta para aparecer na borda direita da tela
                y = HEIGHT - block_size  # Base do inimigo alinhada ao chão
                enemy = Enemy(x, y - (block_size // 2), block_size // 2, block_size // 2)  # Ajusta a posição vertical
                enemy.x_vel = -3  # Velocidade para a esquerda

            objects.append(enemy)


def generate_floor(objects, block_size, offset_x):
    """
    Gera o chão dinamicamente à frente do jogador.
    """
    # Define a posição inicial do próximo bloco do chão
    max_x = max([obj.rect.x for obj in objects if isinstance(obj, Block)] + [-block_size])

    # Garante que o chão seja gerado continuamente
    while max_x < offset_x + WIDTH:
        max_x += block_size
        objects.append(Block(max_x, HEIGHT - block_size, block_size))


def draw_lives(window, lives):
    """
    Desenha as vidas do jogador no canto superior esquerdo da tela.
    """
    skull_image = pygame.image.load(join("assets-2", "skull.png")).convert_alpha()
    skull_image = pygame.transform.scale(skull_image, (40, 40))  # Redimensiona o tamanho do ícone

    for i in range(lives):
        x = 10 + i * 50  # Espaçamento horizontal entre os ícones
        y = 10  # Posição vertical fixa
        window.blit(skull_image, (x, y))


def check_collisions(player, objects):
    """
    Verifica colisões entre o jogador e os inimigos.
    Reduz as vidas do jogador ao colidir com um inimigo.
    """
    collided_enemies = []  # Lista para armazenar inimigos colididos

    for obj in objects:
        if isinstance(obj, Enemy):
            # Obtém as máscaras do jogador e do inimigo
            player_mask = player.mask
            enemy_mask = obj.mask

            # Calcula a posição relativa entre o jogador e o inimigo
            offset_x = obj.rect.x - player.rect.x
            offset_y = obj.rect.y - player.rect.y

            # Verifica a colisão usando máscaras
            collision_point = player_mask.overlap(enemy_mask, (offset_x, offset_y))
            if collision_point:  # Se houver colisão
                player.lives -= 1  # Reduz uma vida
                collided_enemies.append(obj)  # Adiciona o inimigo à lista de colididos

    # Remove os inimigos colididos após a iteração
    for enemy in collided_enemies:
        objects.remove(enemy)

    # Retorna True se o jogador perder todas as vidas
    return player.lives <= 0


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("bg_game.png")

    # Iniciar música do jogo
    pygame.mixer.music.load(join("assets-2", "game_music.mp3"))
    pygame.mixer.music.play(-1)

    block_size = 96
    player = Player(100, 100, 50, 50)

    # Criação inicial do chão e plataformas
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size)]

    offset_x = 0
    scroll_area_width = 200
    player.lives = 3  # Número inicial de vidas do jogador

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Sai do jogo e volta ao menu

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        handle_move(player, objects)

        # Gera o chão dinamicamente
        generate_floor(objects, block_size, offset_x)

        # Gera novas plataformas dinamicamente
        generate_platforms(objects, block_size, offset_x)

        # Gera inimigos dinamicamente
        generate_enemies(objects, block_size, offset_x)

        # Verifica colisões com inimigos
        game_over = check_collisions(player, objects)
        if game_over:
            run = False  # Sai do loop principal para voltar ao menu

        # Remove inimigos fora da tela
        objects = [obj for obj in objects if not (isinstance(obj, Enemy) and obj.is_off_screen())]

        # Remove objetos fora da tela
        objects = [obj for obj in objects if not (isinstance(obj, Block) and obj.rect.right < 0)]

        # Move inimigos
        for obj in objects:
            if isinstance(obj, Enemy):
                obj.move()

        # Atualiza o deslocamento da tela conforme o jogador avança
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        # Desenha o jogo
        draw(window, background, bg_image, player, objects, offset_x)

        # Desenha as vidas do jogador
        draw_lives(window, player.lives)

        pygame.display.update()

    pygame.mixer.music.stop()
    if player.lives <= 0:
        return  # Volta ao menu


if __name__ == "__main__":
    while True:  # Loop principal para reiniciar o jogo
        show_menu(window)  # Exibe o menu antes de iniciar o jogo
        main(window)  # Inicia o jogo
