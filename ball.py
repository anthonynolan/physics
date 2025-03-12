import pygame
import sys
import random
import numpy as np

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

t = pygame.time.get_ticks() / 1000


def update(body1, with_sound=False):
    y = body1.y
    t = pygame.time.get_ticks() / 1000
    y1 = y + v * t + 0.5 * g * t**2
    body1.y = y1

    if with_sound:
        sound = generate_tone(y + 440, 0.06)
        sound.play()


def generate_tone(frequency, duration=1.0, amplitude=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    # Convert to 16-bit integers
    sound_data = (wave * 32767).astype(np.int16)
    # Make it 2D for stereo and ensure it's C-contiguous
    sound_data = np.column_stack((sound_data, sound_data))
    # Ensure the array is C-contiguous
    sound_data = np.ascontiguousarray(sound_data)
    return pygame.sndarray.make_sound(sound_data)


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
