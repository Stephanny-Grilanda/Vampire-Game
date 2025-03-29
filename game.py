import pygame
import random
from player import Player
from platforms import Platform
from enemy import Enemy
from score import Score
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('assets/bg_game.png')
        
        # Inicializa o jogador
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
        
        # Grupos de sprites
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.score = Score()
        self.camera_offset = 0
        
        # Música de fundo
        pygame.mixer.music.load('assets/game_music.mp3')
        pygame.mixer.music.play(-1)
        
        # Criar chão fixo
        self.ground = Platform(0, SCREEN_HEIGHT - 50, is_ground=True)
        self.platforms.add(self.ground)
        
        # Criar plataformas iniciais
        for i in range(5):
            x = random.randint(0, SCREEN_WIDTH - 100)
            y = SCREEN_HEIGHT - 200 - (i * 120)
            platform = Platform(x, y)
            self.platforms.add(platform)

    def spawn_platforms(self):
        """Gera novas plataformas quando necessário."""
        while len(self.platforms.sprites()) < 7:
            x = random.randint(0, SCREEN_WIDTH - 100)
            y = min([platform.rect.y for platform in self.platforms.sprites() if not platform.is_ground]) - random.randint(50, 100)
            platform = Platform(x, y)
            self.platforms.add(platform)

    def spawn_enemies(self):
        """Gera inimigos aleatoriamente."""
        if random.randint(1, 100) == 1:  # Chance de 1% de gerar um inimigo por frame
            x = random.randint(0, SCREEN_WIDTH - 50)
            enemy = Enemy(x)
            self.enemies.add(enemy)

    def update(self, keys):
        """Atualiza o estado do jogo."""
        # Movimento do jogador
        self.player.move(keys)
        self.player.check_boundary(SCREEN_WIDTH)

        # Pulo do jogador
        if keys[pygame.K_SPACE]:
            self.player.jump()
        else:
            self.player.reset_jump()

        # Atualiza o jogador e a câmera
        self.player.update()
        self.update_camera()

        # Atualiza os inimigos
        for enemy in self.enemies:
            enemy.update()  # Certifique-se de que a classe Enemy possui um método update()

        # Interações com plataformas
        self.handle_platform_collisions()

        # Interações com inimigos
        self.handle_enemy_collisions()

        # Remover plataformas fora da tela
        self.cleanup_platforms()

        # Verificar se o jogador caiu
        self.check_player_fall()

        # Gerar novos elementos
        self.spawn_platforms()
        self.spawn_enemies()

        # Atualizar pontuação
        self.score.update(-self.player.rect.y)

    def update_camera(self):
        """Ajusta a câmera com base na posição do jogador."""
        if self.player.rect.centery < SCREEN_HEIGHT // 2:
            self.camera_offset = SCREEN_HEIGHT // 2 - self.player.rect.centery
        else:
            self.camera_offset = 0

    def handle_platform_collisions(self):
        """Gerencia colisões entre o jogador e as plataformas."""
        self.player.on_ground = False
        for platform in self.platforms:
            if not platform.is_ground:
                platform.rect.y += self.camera_offset
            
            if platform.rect.colliderect(self.player.rect) and self.player.velocity_y > 0:
                self.player.velocity_y = 0
                self.player.rect.bottom = platform.rect.top
                self.player.on_ground = True
                self.player.can_jump = True

    def handle_enemy_collisions(self):
        """Gerencia colisões entre o jogador e os inimigos."""
        for enemy in self.enemies:
            enemy.rect.y += self.camera_offset
            
            if self.player.rect.colliderect(enemy.rect):
                self.player.lives -= 1
                enemy.kill()

    def cleanup_platforms(self):
        """Remove plataformas que saíram da tela."""
        for platform in list(self.platforms):
            if not platform.is_ground and platform.rect.top > SCREEN_HEIGHT:
                platform.kill()

    def check_player_fall(self):
        """Verifica se o jogador caiu da tela."""
        if self.ground not in self.platforms:
            if self.player.rect.bottom >= SCREEN_HEIGHT:
                self.player.lives -= 1

    def render(self):
        """Renderiza todos os elementos na tela."""
        self.screen.blit(self.background, (0, 0))
        self.platforms.draw(self.screen)
        self.enemies.draw(self.screen)
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        
        # Renderizar vidas
        skull_img = pygame.image.load('assets/skull.png')
        for i in range(self.player.lives):
            self.screen.blit(skull_img, (10 + i * 30, 10))
        
        # Renderizar pontuação
        self.score.render(self.screen)

        pygame.display.flip()
