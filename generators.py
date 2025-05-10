from os.path import join
import random
import pygame
from constants import HEIGHT, WIDTH
from enemy import Enemy
from objects import Block

def get_background(name):
    path = join("assets-2", name) 
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    _, _, width, height = image.get_rect()
    tiles = []
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

# GERAR ELEMENTOS DINAMICANTE NA TELA

def generate_platforms(objects, block_size, offset_x):
    spawn_area_start = offset_x + WIDTH
    spawn_area_end = spawn_area_start + WIDTH
    platform_count = sum(1 for obj in objects if isinstance(obj, Block) and obj.rect.y < HEIGHT - block_size)
    max_platforms = 10 
    platform_height = HEIGHT - block_size * 3

    if platform_count < max_platforms:
        platforms_in_group = random.randint(2, 3)
        start_x = random.randint(spawn_area_start, spawn_area_end - platforms_in_group * block_size)
        for i in range(platforms_in_group):
            x = start_x + i * block_size
            y = platform_height
            platform = Block(x, y, block_size)
            objects.append(platform)


def generate_enemies(objects, block_size, offset_x):
    spawn_area_start = offset_x + WIDTH 
    spawn_area_end = spawn_area_start + WIDTH 
    enemy_count = sum(1 for obj in objects if isinstance(obj, Enemy))
    max_enemies = 7
    if enemy_count < max_enemies:
        enemies_to_generate = min(4, max_enemies - enemy_count)
        for _ in range(enemies_to_generate):
            spawn_type = random.choice(["top", "right"])
            if spawn_type == "top":
                x = random.randint(spawn_area_start, spawn_area_end)
                y = -block_size 
                enemy = Enemy(x, y, block_size // 2, block_size // 2)
                enemy.y_vel = random.uniform(2, 4) 
            elif spawn_type == "right":
                x = random.randint(spawn_area_start, spawn_area_end)
                y = HEIGHT - block_size
                enemy = Enemy(x, y - (block_size // 2), block_size // 2, block_size // 2)
                enemy.x_vel = -random.uniform(3, 5)          
            objects.append(enemy)


def generate_floor(objects, block_size, offset_x):
    floor_blocks = [obj for obj in objects if isinstance(obj, Block) and obj.rect.y == HEIGHT - block_size]
    if floor_blocks:
        max_x = max(obj.rect.x for obj in floor_blocks)
    else:
        max_x = -block_size
    while max_x < offset_x + WIDTH * 1.5:
        max_x += block_size
        objects.append(Block(max_x, HEIGHT - block_size, block_size))


def draw_lives(window, lives):
    skull_image = pygame.image.load(join("assets-2", "skull.png")).convert_alpha()
    skull_image = pygame.transform.scale(skull_image, (40, 40))
    for i in range(lives):
        x = 10 + i * 50 
        y = 10
        window.blit(skull_image, (x, y))


def draw_score(window, score):
    font = pygame.font.Font(join("assets-2", "creepster.ttf"), 40)
    score_text = font.render(f"Pontuação: {score}", True, (255, 255, 0))
    window.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))