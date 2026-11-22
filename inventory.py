import pygame

class Inventory:
    MAX_CAPACITY = 8
    SLOT_SIZE = 40

    INV_BG_COLOR = (60, 20, 20)
    INV_SELECTED_COLOR = (200, 50, 50)
    INV_BORDER_COLOR = (230, 230, 230)

    def __init__(self):
        self.items = []
        self.selected = 0

    @property
    def selected_item(self):
        if self.selected < len(self.items):
            return self.items[self.selected]
        return None

    def add(self, item):
        if len(self.items) >= self.MAX_CAPACITY:
            return False
        self.items.append(item)
        return True

    def remove(self, item):
        self.items.remove(item)

    def select(self, index):
        if 0 <= index < self.MAX_CAPACITY:
            self.selected = index

    def draw(self, surface):
        x0 = 10
        y = surface.get_height() - self.SLOT_SIZE - 10
        for i in range(self.MAX_CAPACITY):
            slot = pygame.Rect(x0 + i * (self.SLOT_SIZE + 6), y, self.SLOT_SIZE, self.SLOT_SIZE)
            pygame.draw.rect(surface, self.INV_BG_COLOR, slot)
            if i < len(self.items):
                icon = self.items[i].icon
                surface.blit(icon, icon.get_rect(center=slot.center))
            border = self.INV_SELECTED_COLOR if i == self.selected else self.INV_BORDER_COLOR
            pygame.draw.rect(surface, border, slot, 3)