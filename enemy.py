import pygame

from entity import Entity
import player

class Enemy(Entity):
    SPRITE_PREFIX = "enemy"
    TOUCH_DAMAGE = 10
    SPEED = 1.5

    def __init__(self, col, row):
        super().__init__()
        self.place_at(col, row)

    def update(self, player, walls):
        super().update()
        if not self.alive:
            return

        dx = (player.rect.centerx > self.rect.centerx) - (player.rect.centerx < self.rect.centerx)
        dy = (player.rect.centery > self.rect.centery) - (player.rect.centery < self.rect.centery)
        self.move(dx * self.SPEED, dy * self.SPEED, walls)

        if self.rect.colliderect(player.rect):
            player.take_damage(self.TOUCH_DAMAGE)
    