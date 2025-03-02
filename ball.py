import pygame
import sys

pygame.init()

width = 800
height = 600

radius = 25

gravity = 9.8

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

body1 = pygame.Rect(0+radius, 0+radius, 50, 50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    time = pygame.time.get_ticks()
    body1.y = body1.y + time/1000 
    if body1.y>(height-radius):
        body1.y = height-radius

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (body1.x, body1.y), radius)
    
    pygame.display.flip()
    clock.tick(60)
