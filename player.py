import pygame

from main import TILE_SIZE
class Player: 
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 24, 24)
        self.speed = 4
        self.max_health = 100
        self.health = self.max_health

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
