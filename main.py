import pygame
import car
import physics

# Define game window dimensions

WIDTH, HEIGHT = 800, 600
FPS = 60

# Initialize Pygame
pygame.init()

# Create Pygame window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up physics engine
physics_obj = physics.PhysicsEngine(window=window)
# Set up car object
car_obj = car.Car()

physics_obj.add_object(car_obj)

clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    dt = clock.tick(60) / 500
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    car_obj.control(keys)
    # Update game objects
    car_obj.update()
    # physics_obj.update()

    # Draw game objects
    window.fill((255, 255, 255))
    car_obj.draw(window)

    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)

# Clean up Pygame
pygame.quit()
