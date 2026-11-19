
import pygame

from global_settings import TILE_SIZE

class Entity: 
    SIZE = TILE_SIZE - 4
    SPEED = 2
    MAX_HEALTH = 50
    INVINCIBLE_FRAMES = 30
    SPRITE_PREFIX = None

    def __init__(self):
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)
        self.health = self.MAX_HEALTH
        self.invincible_frames = 0
        self.facing = "front"
        self.images = {}
        self.hit_images = {}

        self.load_sprites()

    def load_sprites(self):
        if self.SPRITE_PREFIX is None:
            return
        for direction in {"front", "back", "left", "right"}:
            path = f"assets/{self.SPRITE_PREFIX}/{self.SPRITE_PREFIX}_{direction}.png"
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (self.SIZE, self.SIZE))
            self.images[direction] = image
            self.hit_images[direction] = pygame.mask.from_surface(self.images[direction]).to_surface(
                setcolor=(255, 255, 255, 110), unsetcolor=(0, 0, 0, 0)
            )

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

    def draw(self, surface):
        image = self.images[self.facing]
        if self.alive and self.invincible_frames > 0 and (self.invincible_frames // 5) % 2 == 0:
            image = self.hit_images[self.facing]
        surface.blit(image, self.rect)