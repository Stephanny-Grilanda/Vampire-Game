import pygame
from os.path import isfile, join
from collisions import handle_horizontal_collision, handle_vertical_collision
from constants import GRAVITY, PLAYER_VEL


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(join("assets-2", "player.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(width * 1.8), int(height * 1.8)))  # Redimensiona o vampiro
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x_vel = 0
        self.y_vel = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.lives = 3  
        self.score = 0  
        self.is_attacking = False
        self.attack_images = self.load_attack_images()
        self.attack_frame = 0

    def load_attack_images(self):
        attack_images = []
        player_width, player_height = self.image.get_size() 
        for i in range(2, 14): 
            img_path = join("assets-2", "attack", f"hit_{i}.png")
            if isfile(img_path):
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (int(player_width * 2.8), int(player_height * 1.2)))
                attack_images.append(img)
        return attack_images

    def jump(self):
        self.y_vel = -GRAVITY * 8
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

    def attack(self):
        """Inicia o ataque."""
        if not self.is_attacking:  # Evita reiniciar a animação no meio do ataque
            self.is_attacking = True
            self.attack_frame = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        if self.is_attacking:
            self.animation_count += 1
            if self.animation_count >= fps // 10:  # Controla a velocidade da animação
                self.animation_count = 0
                self.attack_frame += 1
                if self.attack_frame >= len(self.attack_images):
                    self.is_attacking = False  # Finaliza o ataque
                    self.attack_frame = 0

        self.fall_count += 1

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.y_vel *= -1

    def draw(self, win, offset_x):
        if self.is_attacking:
            # Obtém a imagem de ataque atual
            attack_image = self.attack_images[self.attack_frame]
            attack_rect = attack_image.get_rect(midbottom=self.rect.midbottom)  # Alinha a base da imagem com o chão
            win.blit(attack_image, (attack_rect.x - offset_x, attack_rect.y))
        else:
            win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = handle_horizontal_collision(player, objects, -PLAYER_VEL * 2)
    collide_right = handle_horizontal_collision(player, objects, PLAYER_VEL * 2)

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not collide_left:
        if player.rect.x > 0:
            player.move_left(PLAYER_VEL)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]