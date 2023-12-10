import pygame
from car import Car

pygame.init()

screen = pygame.display.set_mode((1600, 900))

car = Car()

track = pygame.image.load("track.png")
track = pygame.transform.scale(track, (1600, 900))
track_mask = pygame.mask.from_surface(track)
mask_image = track_mask.to_surface()



running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds
    drifting = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car.move(-1)
    if keys[pygame.K_DOWN]:
        car.move(1)
    if keys[pygame.K_RIGHT]:
        car.turn(-1)
    if keys[pygame.K_LEFT]:
        car.turn(1)

    car.update()
    car.check_collision(track_mask)

    # Render
    screen.fill("WHITE")  # Clear screen
    screen.blit(mask_image, (0, 0))
    car.draw(screen)
    pygame.display.flip()

pygame.quit()