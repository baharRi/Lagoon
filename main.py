import pygame
import json
from pathlib import Path

from enemy import Enemy
from player import Player
from global_settings import (
    FPS,
    TILE_SIZE, 
    FLOOR_COLOR, WALL_COLOR, WARP_COLOR,
)
from items import ITEM_TYPES

#setting up
pygame.init()

screen = pygame.display.set_mode((25 * TILE_SIZE, 18 * TILE_SIZE))
pygame.display.set_caption("Lagoon")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

#reading a json map and building the layout
def load_map(path):
    data = json.loads(path.read_text())
    tiles = data["tiles"]

    walls = []
    for row, line in enumerate(tiles):
        for col, char in enumerate(line):
            if char == "#": 
                walls.append(pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    warps = []
    for warp in data.get("warps", []):
        rect = pygame.Rect(warp["x"] * TILE_SIZE, warp["y"] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        warps.append((rect, warp))

    enemies = []
    for enemy in data.get("enemies", []):
        enemies.append(Enemy(enemy["x"], enemy["y"]))

    items = []
    for entry in data.get("items", []):
        item_class = ITEM_TYPES.get(entry["type"])
        if item_class is None:
            print(f"Unknown item type")
        else:
            items.append(item_class(entry["x"], entry["y"]))

    #draw the map
    background = pygame.Surface((len(tiles[0]) * TILE_SIZE, len(tiles) * TILE_SIZE))
    background.fill(FLOOR_COLOR)

    for wall in walls: 
        pygame.draw.rect(background, WALL_COLOR, wall)
    for rect, _ in warps:
        pygame.draw.rect(background, WARP_COLOR, rect, 3)

    return {"walls": walls, "warps": warps, "start": data["start"], "background": background, "enemies": enemies, "items": items}

#load the json files
MAPS = {path.stem: load_map(path) for path in sorted(Path("maps").glob("*.json"))}
for name, map_data in MAPS.items():
    for _, warp in map_data["warps"]:
        if warp["to"] not in MAPS:
            print(f"Warning: Warp in {name} points to unknown map {warp['to']}")

#opens a map and spawns player
def start_map(name, col=None, row=None):
    map_data = MAPS[name]
    if col is None: 
        col, row = map_data["start"]
    player.place_at(col, row)
    return map_data

player = Player()
map = start_map("map1")

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                player.take_damage(10)
            elif event.key == pygame.K_k:
                player.heal(10)
            elif pygame.K_1 <= event.key <= pygame.K_8:
                player.inventory.select(event.key - pygame.K_1)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button ==  1:
            player.attack(map["enemies"])

    map["enemies"] = [e for e in map["enemies"] if e.alive]

    if player.alive:
        dx, dy = player.read_input()
        player.move(dx, dy, map["walls"])

        for item in map["items"][:]:
            if player.rect.colliderect(item.rect) and player.inventory.add(item):
                map["items"].remove(item)

    #warps
    for rect, warp in map["warps"]:
        if player.rect.colliderect(rect) and warp["to"] in MAPS:
            map = start_map(warp["to"], warp.get("to_x"), warp.get("to_y"))
            break

    player.update()
    
    #drawing everything
    screen.blit(map["background"], (0, 0))
    player.draw(screen)
    player.draw_health_bar(screen)
    player.inventory.draw(screen)
    for item in map["items"]:
        item.draw(screen)
    for enemy in map["enemies"]:
        enemy.update(player, map["walls"])
        enemy.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()