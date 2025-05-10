import pygame
from enemy import Enemy

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

def handle_horizontal_collision(player, objects, dx):
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

def check_collisions(player, objects):
    collided_enemies = [] 
    for obj in objects:
        if isinstance(obj, Enemy):
            player_mask = player.mask
            enemy_mask = obj.mask
            offset_x = obj.rect.x - player.rect.x
            offset_y = obj.rect.y - player.rect.y
            collision_point = player_mask.overlap(enemy_mask, (offset_x, offset_y))
            if collision_point: 
                player.lives -= 1 
                collided_enemies.append(obj)
    for enemy in collided_enemies:
        objects.remove(enemy)
    return player.lives <= 0