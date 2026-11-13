import pygame

#setting up
pygame.init()

TILE_SIZE = 32
SPEED = 4
MAP_FILES = ["maps/map1.txt", "maps/map2.txt", "maps/map3.txt"]

screen = pygame.display.set_mode((25 * TILE_SIZE, 18 * TILE_SIZE))
pygame.display.set_caption("Lagoon")
clock = pygame.time.Clock()

#reading a map file and returning the layout
def load_map(file_path):
    walls = []
    exits = []
    start = (TILE_SIZE, TILE_SIZE)  # Default start position if not specified in the map
    with open(file_path, "r") as map_file:
        for row, line in enumerate(map_file): 
            for col, char in enumerate(line.strip("\n")):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if char == "#":
                    walls.append(rect)
                elif char == "E":
                    exits.append(rect)
                elif char == "P":
                    start = (col * TILE_SIZE, row * TILE_SIZE)
    return walls, exits, start

def start_map(index): 
    walls, exits, start = load_map(MAP_FILES[index])
    player.topleft = (start[0], start[1] + 4)
    return walls, exits

player = pygame.Rect(100, 100, 24, 24)
current_map_index = 0
walls, exits = start_map(current_map_index)

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

    if player.collidelist(exits) != -1:
        current_map_index = (current_map_index + 1) % len(MAP_FILES)
        walls, exits = start_map(current_map_index)

    screen.fill((30, 30, 30))
    for wall in walls:
        pygame.draw.rect(screen, (120, 120, 120), wall)
    for exit in exits: 
        pygame.draw.rect(screen, (0, 255, 0), exit)
    pygame.draw.rect(screen, (80, 200, 120), player)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()