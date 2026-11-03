import pygame 
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("move the square")
clock = pygame.time.Clock()

speed = 5
x_cord = 50
y_cord = 400

running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT]:
        x_cord -= speed
    if key[pygame.K_RIGHT]:
        x_cord += speed

    screen.fill((0, 0, 0))  # black background
    pygame.draw.rect(screen, (255, 255, 0), (x_cord, y_cord, 200, 100))  # yellow shape

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
