import pygame
import sys
import numpy as np
import math
import random

pygame.init()

SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 1000
DASHBOARD_WIDTH = 200
SIMULATION_WIDTH = SCREEN_WIDTH - DASHBOARD_WIDTH

radius = 20

g = 200.0  

font = pygame.font.Font(None, 24)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

center = np.array([SCREEN_WIDTH//2, SCREEN_HEIGHT//2])

def reset():
    print('resetting')
    global t0, prev_t, path, pos, vel
    t0 = pygame.time.get_ticks() / 1000
    prev_t = 0
    path = []
    pos = np.array([0 , 0])
    vel = np.array([random.randint(10, 150), random.randint(10, 150)])

reset()


def draw_dashboard(screen, g, t, vel):
    info_lines = [
        f"g: {g:.2f}",
        f"t: {t:.2f}",
        f"velocity: {math.sqrt(vel[0]**2 + vel[1]**2):.1f}"
    ]
    for i, line in enumerate(info_lines):
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (SIMULATION_WIDTH + 10, 10 + i * 30))


def update():
    global pos, vel, prev_t
    
    current_t = pygame.time.get_ticks() / 1000 - t0
    dt = current_t - prev_t
    
    # Calculate direction vector from ball to center (gravity source)
    r = center - pos
    
    # Calculate distance
    distance = np.linalg.norm(r)
    
    # Normalize the direction vector
    r_hat = r / distance
    
    # Calculate gravitational force (stronger when closer)
    # Using inverse square law but with a minimum distance to prevent extreme forces
    min_distance = 50  # Prevent extreme forces when very close
    effective_distance = max(distance, min_distance)
    force = g * r_hat / (effective_distance / 100)**2

# Update velocity using force and time step
    vel = vel + force * dt

# Update position using velocity and time step
    pos = pos + vel * dt
    path.append(pos)

    prev_t = current_t

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                g+=10
            elif event.key == pygame.K_DOWN:
                g-=10    
            elif event.key == pygame.K_LEFT:
                vel = vel *.9
            elif event.key == pygame.K_RIGHT:
                vel = vel /.9

    update()
    
    screen.fill((255, 255, 255))

    
    pygame.draw.circle(screen, (1, 0, 254), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), radius)

    pygame.draw.line(screen, (200, 200, 200), (SIMULATION_WIDTH, 0), (SIMULATION_WIDTH, SCREEN_HEIGHT))

    # Check if ball is out of bounds
    if (pos[0] < 0 or pos[0] > SIMULATION_WIDTH or 
        pos[1] < 0 or pos[1] > SCREEN_HEIGHT ):
        reset()
    
    pygame.draw.circle(screen, (0,255,0), (int(pos[0]), int(pos[1])), radius)
    for point in path:
        pygame.draw.circle(screen, (255, 0, 0), point, 1)  
    draw_dashboard(screen, g, prev_t, vel)
    pygame.display.flip()
    clock.tick(60)
