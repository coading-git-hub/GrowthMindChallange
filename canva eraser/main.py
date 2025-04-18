import pygame
import time

pygame.init()

# Canvas and Grid Configuration
CANVA_WIDTH = 400
CANVA_HEIGHT = 400
CELL_SIZE = 40
ERASER_SIZE = 20

# Colors
BLUE = (0, 0, 225)
WHITE = (255, 255, 255)
PINK = (225, 182, 193)

# Initialize Screen
screen = pygame.display.set_mode((CANVA_WIDTH, CANVA_HEIGHT))
pygame.display.set_caption("Enter effect in pygame")

# Creating the Grid
grid = []
for row in range(0, CANVA_WIDTH, CELL_SIZE):
    for col in range(0, CANVA_HEIGHT, CELL_SIZE):  
        rect = pygame.Rect(col, row, CELL_SIZE, CELL_SIZE)
        grid.append(rect)

# Initialize Eraser
eraser = pygame.Rect(200, 200, ERASER_SIZE, ERASER_SIZE)

# Game Loop
running = True
while running:
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw Grid
    for rect in grid:
        pygame.draw.rect(screen, BLUE, rect)

    # Eraser Logic
    mouse_x, mouse_y = pygame.mouse.get_pos()
    eraser.topleft = (mouse_x, mouse_y)

    # Remove intersecting grid cells
    grid = [rect for rect in grid if not eraser.colliderect(rect)]  

    # Draw Eraser
    pygame.draw.rect(screen, PINK, eraser)

    # Update Display
    pygame.display.flip()
    time.sleep(0.05)  

pygame.quit()
