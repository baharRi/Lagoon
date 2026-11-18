
import pygame

from global_settings import TILE_SIZE

class Entity: 
    SIZE = TILE_SIZE - 4
    SPEED = 2
    MAX_HEALTH = 100

    def __init__(self):
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)
        self.health = self.MAX_HEALTH
        self.invincible_frames = 0
        self.images = {}

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
        if self.alive:
            self.health = min(self.MAX_HEALTH, self.health + amount)