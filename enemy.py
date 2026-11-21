import pygame

from entity import Entity
from global_settings import TILE_SIZE, FPS

class Enemy(Entity):
    SPRITE_PREFIX = "enemy"
    TOUCH_DAMAGE = 10
    SPEED = 1.5
    VIEW_RANGE = 6 * TILE_SIZE
    ALERT_SECS = 3 #how long till entity loses sight

    def __init__(self, col, row):
        super().__init__()
        self.place_at(col, row)
        self.target = None #last seen location of player
        self.alert_frames = 0

    def can_see(self, player, walls):
        start, end = self.rect.center, player.rect.center
        if pygame.Vector2(start).distance_to(end) > self.VIEW_RANGE:
            return False
        return not any(wall.clipline(start, end) for wall in walls)

    def update(self, player, walls):
        super().update()
        if not self.alive:
            return

        #looking for player
        if self.can_see(player, walls):
            self.target = player.rect.center
            self.alert_frames = self.ALERT_SECS * FPS
        elif self.target is not None:
            self.alert_frames -=1 
            if self.alert_frames <= 0:
                self.target = None #loses chase

        #move towards last known pos
        if self.target is not None: 
            offset = pygame.Vector2(self.target) - pygame.Vector2(self.rect.center)
            if offset.length() <= self.SPEED:
                self.target = None #nothing there
            else:
                self.move(offset.x, offset.y, walls)

        if self.rect.colliderect(player.rect):
            player.take_damage(self.TOUCH_DAMAGE)
    