import pygame

from global_settings import TILE_SIZE

class Item: 
    NAME = "Item"
    IMAGE = None
    CONSUMABLE = False

    def __init__(self, col, row):
        size = TILE_SIZE - 8
        self.rect = pygame.Rect(col * TILE_SIZE + 4, row * TILE_SIZE + 4, size, size)

        image = pygame.image.load(f"assets/items/{self.IMAGE}").convert_alpha()

        self.image = pygame.transform.scale(image, (size, size))        #shown on the ground
        self.icon = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))  #shown in the inventory

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def use(self, player):
        return False


class Weapon(Item):
    DAMAGE = 10
    COOLDOWN = 20
    REACH = 32

    def get_hitbox(self, owner_rect, facing):
        hitbox = pygame.Rect(0, 0, self.REACH, self.REACH)
        if facing == "right":
            hitbox.midleft = owner_rect.midright
        elif facing == "left":
            hitbox.midright = owner_rect.midleft
        elif facing == "front":
            hitbox.midtop = owner_rect.midbottom
        else:
            hitbox.midbottom = owner_rect.midtop
        return hitbox

class Sword(Weapon):
    NAME = "Sword"
    IMAGE = "sword.png"

    DAMAGE = 10
    COOLDOWN = 20
    REACH = 32

class Potion(Item):
    NAME = "Potion"
    IMAGE = "potion.png"
    COOLDOWN = 20
    HEAL_AMOUNT = 20
    CONSUMABLE = True

    def use(self, player):
        if player.health == player.MAX_HEALTH:
            return False
        player.heal(self.HEAL_AMOUNT)
        return True

ITEM_TYPES = {
    "sword": Sword,
    "potion": Potion,
}