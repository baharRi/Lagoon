from turtle import width

import pygame

from global_settings import (
    FPS,
    BAR_BG_COLOR, BAR_FILL_COLOR, BAR_BORDER_COLOR,
)
from entity import Entity
from inventory import Inventory
from items import Weapon

class Player(Entity):
    SPEED = 4
    MAX_HEALTH = 100
    INVINCIBLE_FRAMES = FPS  #1 sec of invincibility after taking damage
    SPRITE_PREFIX = "player"

    def __init__(self):
        super().__init__()
        self.inventory = Inventory()
        self.attack_cooldown = 0
        self.slash_frames = 0
        self.slash_rect = None

    def reset(self):
        self.health = self.MAX_HEALTH
        self.invincible_frames = 0

    #reading movement for wasd and arrow keys
    def read_input(self):
        keys = pygame.key.get_pressed()
        dx = ((keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT]))
        dy = ((keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP]))
        return dx, dy

    def draw(self, surface):
        super().draw(surface)
        if self.slash_frames > 0:
            pygame.draw.rect(surface, (255, 255, 255), self.slash_rect, 2) #hitbox. TODO: add anim/sword slash
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

    def attack(self, enemies):
        weapon = self.inventory.selected_item
        if not isinstance(weapon, Weapon) or self.attack_cooldown > 0:
            return
        hitbox = weapon.get_hitbox(self.rect, self.facing)
        for enemy in enemies:
            if hitbox.colliderect(enemy.rect):
                enemy.take_damage(weapon.DAMAGE)
            self.attack_cooldown = weapon.COOLDOWN
            self.slash_rect = hitbox
            self.slash_frames = 6
    
    def use_item(self):
        item = self.inventory.selected_item
        if item is None or not self.alive:
            return
        if item.use(self) and item.CONSUMABLE:
            self.inventory.consume(item)

    def update(self):
        super().update()
        if self.attack_cooldown > 0:
            self.attack_cooldown -=1
        if self.slash_frames > 0:
            self.slash_frames -= 1