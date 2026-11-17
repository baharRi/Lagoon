from turtle import width

import pygame

from global_settings import (
    TILE_SIZE, 
    BAR_BG_COLOR, BAR_FILL_COLOR, BAR_BORDER_COLOR,
)

class Player: 
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 24, 24)
        self.speed = 4
        self.max_health = 100
        self.health = self.max_health

        self.images = {}
        for direction in {"front", "back", "left", "right"}:
            image = pygame.image.load(f"assets/player/player_{direction}.png").convert_alpha()
            self.images[direction] = pygame.transform.scale(image, (28, 28))

        self.facing = "front"

    @property
    def alive(self): 
        return self.health > 0
    
    def place_at(self, col, row):
        self.rect.topleft = (col * TILE_SIZE + 4, row * TILE_SIZE + 4)

    def take_damage(self, amount):
        if not self.alive:
            return
        self.health -= amount

    def heal(self, amount): 
        if self.alive: self.health = min(self.max_health, self.health + amount)

    def reset(self):
        self.health = self.max_health

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
        surface.blit(image, self.rect)

    def draw_health_bar(self, surface, x=10, y=10, width=200, height=20):
        fraction = self.health / self.max_health
        pygame.draw.rect(surface, BAR_BG_COLOR, (x, y, width, height))
        pygame.draw.rect(surface, BAR_FILL_COLOR, (x, y, int(width * fraction), height))
        pygame.draw.rect(surface, BAR_BORDER_COLOR, (x, y, width, height), 2)
