import pygame

#setting up
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lagoon")
clock = pygame.time.Clock()

player = pygame.Rect(100, 100, 32, 32)
walls = [pygame.Rect(0, 0, 800, 12), pygame.Rect(0, 0, 12, 600), pygame.Rect(0, 588, 800, 12), pygame.Rect(788, 0, 12, 600)]
SPEED = 4

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

    screen.fill((30, 30, 30))
    for wall in walls:
        pygame.draw.rect(screen, (120, 120, 120), wall)
    pygame.draw.rect(screen, (80, 200, 120), player)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()