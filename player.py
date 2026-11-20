from turtle import width

import pygame

from global_settings import (
    FPS,
    BAR_BG_COLOR, BAR_FILL_COLOR, BAR_BORDER_COLOR,
)
from entity import Entity

class Player(Entity):
    SPEED = 4
    MAX_HEALTH = 100
    INVINCIBLE_FRAMES = FPS  #1 sec of invincibility after taking damage
    SPRITE_PREFIX = "player"

    def reset(self):
        self.health = self.MAX_HEALTH
        self.invincible_frames = 0

    #reading movement for wasd and arrow keys
    def read_input(self):
        keys = pygame.key.get_pressed()
        dx = ((keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])) * self.SPEED
        dy = ((keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])) * self.SPEED
        return dx, dy

    def draw(self, surface):
        super().draw(surface)
        if not self.alive:
            overlay = pygame.mask.from_surface(self.images[self.facing]).to_surface(
                setcolor=(200, 0, 0, 110), unsetcolor=(0, 0, 0, 0)
            )
            surface.blit(overlay, self.rect)

    def draw_health_bar(self, surface, x=10, y=10, width=200, height=20):
        fraction = self.health / self.MAX_HEALTH
        pygame.draw.rect(surface, BAR_BG_COLOR, (x, y, width, height))
        pygame.draw.rect(surface, BAR_FILL_COLOR, (x, y, int(width * fraction), height))
        pygame.draw.rect(surface, BAR_BORDER_COLOR, (x, y, width, height), 2)
