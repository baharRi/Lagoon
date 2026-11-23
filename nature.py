import pygame

from global_settings import TILE_SIZE

class Tree:
    WIDTH_TILES = 2
    HEIGHT_TILES = 3

    def __init__(self, col, row):
        image = pygame.image.load("assets/environment/tree.png").convert_alpha()
        self.image = pygame.transform.scale(
            image, (self.WIDTH_TILES * TILE_SIZE, self.HEIGHT_TILES * TILE_SIZE)
        )
        self.rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.draw_rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def draw(self, surface):
        surface.blit(self.image, self.draw_rect)