import pygame

# 1. Initialize
pygame.init()

# 2. Create a window (width, height)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

running = True
while running:
    # 3. Handle events (clicks, keys, quit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 4. Update game logic here
    
    # 5. Draw everything
    screen.fill((0, 0, 0))  # black background
    
    pygame.draw.circle(screen, (255, 0, 0), (400, 300), 50)  # red circle
    
    # 6. Flip the display (actually show what you drew)
    pygame.display.flip()
    
    # 7. Limit to 60 FPS
    clock.tick(60)

pygame.quit()