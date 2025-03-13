import pygame
import sys
import random
import numpy as np
from utils import generate_tone

pygame.init()

width = 800
height = 600

radius = 25

g = 9.8

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

x_offset = 100

body1 = pygame.Rect(0 + radius, 0 + radius, 50, 50)
body2 = pygame.Rect(0 + radius + x_offset, 0 + radius + random.randint(0, 150), 50, 50)
cathal = pygame.Rect(2 * x_offset, 0, 50, 50)

t0 = 0
def reset_time():
    global t0
    t0 = pygame.time.get_ticks() / 1000
reset_time()

sound = False

def update(body1, with_sound=False):
    global sound
    y = body1.y
    t = pygame.time.get_ticks() / 1000 -t0
    y1 = y + v * t + 0.5 * g * t**2
    body1.y = y1

    if with_sound and sound:
        sound = generate_tone(y + 440, 0.06)
        sound.play()



pygame.mixer.init(16000, -16, 2, 2048)

# Example: Play an A4 note (440 Hz) for 1 second
frequency = 440  # Hz (A4 note)
# duration = 1.0  # seconds


v = 0
counter = 0
freeze = False


while all([body1.y < height - radius, body2.y < height - radius]):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # print(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space bar was pressed")
                freeze = not freeze
                if not freeze:
                    reset_time()

    if not freeze:
        counter += 1
        update(body1, True if not counter % 10 else False)
        update(body2)
        update(cathal)

        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (255, 0, 0), (body1.x, body1.y), radius)
        pygame.draw.circle(screen, (0, 0, 0), (body2.x, body2.y), radius)
        pygame.draw.circle(screen, (255, 95, 7), (cathal.x, cathal.y), radius)

        pygame.display.flip()
        clock.tick(60)
