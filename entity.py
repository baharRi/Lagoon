
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
        self.pos = pygame.Vector2(self.rect.topleft) #exact fractal pos of entity
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
        self.pos.update(self.rect.topleft)
    
    def take_damage(self, amount):
        if self.invincible_frames > 0 or not self.alive:
            return
        self.health = max(0, self.health - amount)
        self.invincible_frames = self.INVINCIBLE_FRAMES

    def heal(self, amount):
        if self.alive:
            self.health = min(self.MAX_HEALTH, self.health + amount)

    def update(self):
        if self.invincible_frames > 0:
            self.invincible_frames -= 1

    def draw(self, surface):
        image = self.images[self.facing]
        if self.alive and self.invincible_frames > 0 and (self.invincible_frames // 5) % 2 == 0:
            image = self.hit_images[self.facing]
        surface.blit(image, self.rect)

    def move(self, dx, dy, walls):
        direction = pygame.Vector2(dx, dy)
        if direction.length_squared() > 0:
            direction = direction.normalize() * self.SPEED

        #x axis, horizontal
        self.pos.x += direction.x
        self.rect.x = round(self.pos.x)
        if direction.x > 0:
            self.facing = "right"
        elif direction.x < 0:
            self.facing = "left"
        for wall in walls:
            if self.rect.colliderect(wall):
                if direction.x > 0:
                    self.rect.right = wall.left
                elif direction.x < 0:
                    self.rect.left = wall.right
                self.pos.x = self.rect.x
        
        #y axis, vertical
        self.pos.y += direction.y
        self.rect.y = round(self.pos.y)
        if direction.y > 0:
            self.facing = "front"
        elif direction.y < 0:
            self.facing = "back"
        for wall in walls:
            if self.rect.colliderect(wall):
                if direction.y > 0:
                    self.rect.bottom = wall.top
                elif direction.y < 0:
                    self.rect.top = wall.bottom
                self.pos.y = self.rect.y