import pygame

#setting up
pygame.init()

TILE_SIZE = 32
SPEED = 4
MAP_FILES = ["maps/map1.txt", "maps/map2.txt", "maps/map3.txt"]

screen = pygame.display.set_mode((25 * TILE_SIZE, 18 * TILE_SIZE))
pygame.display.set_caption("Lagoon")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

MAPS = {
    "map1": {"file": "maps/map1.txt", "doors": {"1": "map2", "2": "map3"}},
    "map2": {"file": "maps/map2.txt", "doors": {"1": "map1"}},
    "map3": {"file": "maps/map3.txt", "doors": {"1": "map1"}},
}

#reading a map file and returning the layout
def load_map(name):
    file_path = MAPS[name]["file"]
    walls = []
    doors = []
    start = (TILE_SIZE, TILE_SIZE)  # Default start position if not specified in the map
    with open(file_path) as map_file:
        for row, line in enumerate(map_file): 
            for col, char in enumerate(line.strip("\n")):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if char == "#":
                    walls.append(rect)
                elif char.isdigit():
                    doors.append((rect, char))
                elif char == "P":
                    start = (col * TILE_SIZE, row * TILE_SIZE)
    return walls, doors, start

#loads a map and spawns player
def start_map(name, came_from=None): 
    walls, doors, start = load_map(name)
    spawn = start 

    for rect, digits in doors: 
        if MAPS[name]["doors"].get(digits) == came_from:
            spawn = rect.topleft
    player.topleft = (spawn[0], spawn[1] + 4)
    return walls, doors

player = pygame.Rect(0, 0, 24, 24)
current_map = "map1"
walls, doors = start_map(current_map)
ignore_doors = True

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
    for wall in walls:
        if player.colliderect(wall):
            if dx > 0:
                player.right = wall.left
            elif dx < 0:
                player.left = wall.right

    player.y += dy
    for wall in walls:
        if player.colliderect(wall):
            if dy > 0:
                player.bottom = wall.top
            elif dy < 0:
                player.top = wall.bottom

    #door handling
    touching = [digit for rect, digit in doors if player.colliderect(rect)]
    if ignore_doors:
        if not touching:
            ignore_doors = False
    elif touching:
        target_map = MAPS[current_map]["doors"].get(touching[0])
        if target_map: 
            previous_map = current_map
            current_map = target_map
            walls, doors = start_map(current_map, previous_map)
            ignore_doors = True

    screen.fill((30, 30, 30))
    for wall in walls:
        pygame.draw.rect(screen, (120, 120, 120), wall)
    for rect, digit in doors:
        pygame.draw.rect(screen, (0, 255, 0), rect)
        label = font.render(digit, True, (0, 0, 0))
        screen.blit(label, label.get_rect(center=rect.center))
    pygame.draw.rect(screen, (80, 200, 120), player)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()