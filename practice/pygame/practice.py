import pygame
import sys 
import math


pygame.init()

width, height = 800, 600

screen = pygame.display.set_mode((width, height)) 
pygame.display.set_caption("Disappear")
clock = pygame.time.Clock()

start_x , start_y = width // 2, height // 2  # to get the shape in the middle of the screen 
speed = 5

visibility = False # to make the shape invisible at the start
font = pygame.font.Font(None, 40)

color = (255, 255, 255)
r = 0
text = font.render("START", True, (255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                visibility = False  # Toggle visibility when spacebar is pressed
                text = font.render("RESET", True, (255, 255, 255))
            elif event.key == pygame.K_1:
                visibility = True
                color = (255, 0, 0)  # Change color to red when '1' is pressed
                r = 50
                text = font.render("FIRE", True, (255, 255, 255))
            elif event.key == pygame.K_2:
                visibility = True
                color = (0, 0, 255)  # Change color to blue when '2' is pressed
                r = 35
                text = font.render("WATER", True, (255, 255, 255))
            elif event.key == pygame.K_3:
                visibility = True
                color = (0, 255, 0)  # Change color to green when '3' is pressed
                r = 25
                text = font.render("AIR", True, (255, 255, 255))

    mouse_x, mouse_y = pygame.mouse.get_pos() # to get the position of the cursor
    mouse_x = max(50, min(width - 50, mouse_x))
    mouse_y = max(50, min(height - 50, mouse_y))

    # to get calcukate the distance between the cursor and shape 

    dx = mouse_x - start_x 
    dy = mouse_y - start_y

    distance = math.hypot(dx, dy)

    # shape starts moving towards the cursor 

    if distance > speed:
        start_x += dx / distance * speed
        start_y += dy / distance * speed
    else:
        start_x, start_y = mouse_x, mouse_y

    screen.fill((0, 0, 0))  # black background
                
    if visibility:
        pygame.draw.circle(screen, color, (start_x, start_y), r)  # circle
        
    screen.blit(text,(20,20))

    pygame.display.flip()
    clock.tick(60)

