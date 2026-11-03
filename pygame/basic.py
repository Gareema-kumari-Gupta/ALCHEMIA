import pygame
import time

# 1. Initialize
pygame.init()

# 2. Create a window (width, height)
#screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)  # fullscreen(do not use it is risky goes full screen and don't have option to close it. to close use Alt+F4)
screen = pygame.display.set_mode((800,600))
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
    
    pygame.draw.circle(screen, (255, 0, 0), (150, 250), 50)  # red circle
    pygame.draw.rect(screen, (255, 255, 0), (50, 400, 450, 100))  # yellow square
    pygame.draw.line(screen, (0, 0, 255), (50, 50), (700,500), 5)  # blue line
    
    # 6. Flip the display (actually show what you drew)
    pygame.display.flip()
    # Print the current FPS
    print(f'FPS: {int(clock.get_fps())}')
    
    # 7. Limit to 60 FPS
    clock.tick(60)
    time.sleep(2)

pygame.quit()