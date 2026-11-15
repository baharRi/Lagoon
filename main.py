import pygame
import json
from pathlib import Path

#setting up
pygame.init()

TILE_SIZE = 32
SPEED = 4

FLOOR_COLOR = (150, 130, 117)
WALL_COLOR = (33, 21, 21)
WARP_COLOR = (233, 220, 182)
PLAYER_COLOR = (120, 30, 30)

screen = pygame.display.set_mode((25 * TILE_SIZE, 18 * TILE_SIZE))
pygame.display.set_caption("Lagoon")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

#reading a JSON map and building the layout
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

    #draw the map
    background = pygame.Surface((len(tiles[0]) * TILE_SIZE, len(tiles) * TILE_SIZE))
    background.fill(FLOOR_COLOR)

    for wall in walls: 
        pygame.draw.rect(background, WALL_COLOR, wall)
    for rect, _ in warps:
        pygame.draw.rect(background, WARP_COLOR, rect, 3)

    return {"walls": walls, "warps": warps, "start": data["start"], "background": background}

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
    player.topleft = (col * TILE_SIZE + 4, row * TILE_SIZE + 4) 
    return map_data

player = pygame.Rect(0, 0, 24, 24)
map = start_map("map1")

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #movement for wasd and arrow keys
    keys = pygame.key.get_pressed()
    dx = ((keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])) * SPEED
    dy = ((keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])) * SPEED

    player.x += dx
    for wall in map["walls"]:
        if player.colliderect(wall):
            if dx > 0:
                player.right = wall.left
            elif dx < 0:
                player.left = wall.right

    player.y += dy
    for wall in map["walls"]:
        if player.colliderect(wall):
            if dy > 0:
                player.bottom = wall.top
            elif dy < 0:
                player.top = wall.bottom

    #warps
    for rect, warp in map["warps"]:
        if player.colliderect(rect) and warp["to"] in MAPS:
            map = start_map(warp["to"], warp.get("to_x"), warp.get("to_y"))
            break

    screen.blit(map["background"], (0, 0))
    pygame.draw.rect(screen, PLAYER_COLOR, player)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()