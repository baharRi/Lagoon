from turtle import width

import pygame

from global_settings import (
    FPS,
    TILE_SIZE, 
    BAR_BG_COLOR, BAR_FILL_COLOR, BAR_BORDER_COLOR,
)
from entity import Entity

class Player(Entity):
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 28, 28)
        self.speed = 4
        self.invincible_frames = 0
        self.max_health = 100
        self.health = self.max_health

        self.images = {}
        self.hit_images = {}
        for direction in {"front", "back", "left", "right"}:
            image = pygame.image.load(f"assets/player/player_{direction}.png").convert_alpha()
            self.images[direction] = pygame.transform.scale(image, (28, 28))
            self.hit_images[direction] = pygame.mask.from_surface(self.images[direction]).to_surface(
                setcolor=(255, 255, 255, 110), unsetcolor=(0, 0, 0, 0)
            )

        self.facing = "front"

    def take_damage(self, amount):
        if self.invincible_frames > 0 or not self.alive:
            return
        self.health -= amount
        self.invincible_frames = FPS  #set invincibility frames

    def reset(self):
        self.health = self.max_health
        self.invincible_frames = 0

    def update(self):
        if self.invincible_frames > 0:
            self.invincible_frames -= 1

    #reading movement for wasd and arrow keys
    def read_input(self):
        keys = pygame.key.get_pressed()
        dx = ((keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])) * self.speed
        dy = ((keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])) * self.speed
        return dx, dy

    def move(self, dx, dy, walls):
        self.rect.x += dx
        if dx > 0:
            self.facing = "right"
        elif dx < 0:
            self.facing = "left"
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right

        self.rect.y += dy
        if dy > 0:
            self.facing = "front"
        elif dy < 0:
            self.facing = "back"
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                elif dy < 0:
                    self.rect.top = wall.bottom

    def draw(self, surface):
        image = self.images[self.facing]
        if not self.alive:
            overlay = pygame.mask.from_surface(image).to_surface(
                setcolor=(200, 0, 0, 110), unsetcolor=(0, 0, 0, 0)
            )
            surface.blit(overlay, self.rect)
        elif self.invincible_frames > 0 and (self.invincible_frames // 5) % 2 == 0:
            image = self.hit_images[self.facing]
        else: surface.blit(image, self.rect)

    def draw_health_bar(self, surface, x=10, y=10, width=200, height=20):
        fraction = self.health / self.max_health
        pygame.draw.rect(surface, BAR_BG_COLOR, (x, y, width, height))
        pygame.draw.rect(surface, BAR_FILL_COLOR, (x, y, int(width * fraction), height))
        pygame.draw.rect(surface, BAR_BORDER_COLOR, (x, y, width, height), 2)
