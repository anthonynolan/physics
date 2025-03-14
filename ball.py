import pygame
import sys
import numpy as np

pygame.init()

width = 1600
height = 1200

radius = 25

g = 200.0  # Increased by 10x for faster movement

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Center of the screen (source of gravity)
center = np.array([width//2, height//2])

# Initial position of the ball
pos = np.array([0 + radius, 0 + radius])
vel = np.array([150.0, 20.0])  # Initial velocity vector (not pointed at the center)

t0 = 0
prev_t = 0


def reset_time():
    global t0, prev_t
    t0 = pygame.time.get_ticks() / 1000
    prev_t = 0
reset_time()


def update():
    global pos, vel, prev_t
    
    current_t = pygame.time.get_ticks() / 1000 - t0
    dt = current_t - prev_t
    
    # Calculate direction vector from ball to center (gravity source)
    r = center - pos
    
    # Calculate distance
    distance = np.linalg.norm(r)
    
    # Normalize the direction vector
    if distance > 0:
        r_hat = r / distance
    else:
        r_hat = np.array([0, 0])
    
    # Calculate gravitational force (stronger when closer)
    # Using inverse square law but with a minimum distance to prevent extreme forces
    min_distance = 50  # Prevent extreme forces when very close
    effective_distance = max(distance, min_distance)
    force = g * r_hat / (effective_distance / 100)**2
    
    # Update velocity using force and time step
    vel = vel + force * dt
    
    # Update position using velocity and time step
    pos = pos + vel * dt
    
    prev_t = current_t
counter = 0
freeze = False


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space bar was pressed")
                freeze = not freeze
                if not freeze:
                    reset_time()

    if not freeze:
        counter += 1
        update()
        
        # Check if ball is out of bounds
        if (pos[0] < radius or pos[0] > width - radius or 
            pos[1] < radius or pos[1] > height - radius):
            # Reset position to top left
            pos = np.array([0 + radius, 0 + radius])
            vel = np.array([50.0, 20.0])  # Same initial velocity on reset
            reset_time()
            prev_t = 0

        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (255, 0, 0), (int(pos[0]), int(pos[1])), radius)
        pygame.draw.circle(screen, (0, 255, 0), (width//2, height//2), radius)
        pygame.display.flip()
        clock.tick(60)
