import pygame

pygame.init()

CELL = 50
COLS, ROWS = 16, 12
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blue Square")
clock = pygame.time.Clock()

col, row = COLS // 2, 0

pygame.key.set_repeat(200, 80)

fall_interval = 2000   # milliseconds between automatic moves down
fall_timer = 0         # milliseconds accumulated since the last move down

running = True
while running:
    # Milliseconds since the previous frame
    dt = clock.tick(60)
    fall_timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_a:
                col -= 1
            elif event.key == pygame.K_d:
                col += 1
            elif event.key == pygame.K_s:
                row += 1       # soft drop: move down faster

    # Automatic fall
    if fall_timer >= fall_interval:
        row += 1
        fall_timer -= fall_interval   # keep the leftover time, so no drift

    col = max(0, min(col, COLS - 1))
    row = max(0, min(row, ROWS - 1))

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (0, 0, 255), (col * CELL, row * CELL, CELL, CELL))
    pygame.display.flip()

pygame.quit()