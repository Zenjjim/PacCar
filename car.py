import pygame

import numpy as np


CAR_SIZE = (50, 25)
DRIFT_FACTOR = 0.94
DRAG = 0.95
BREAK = 0.9
DT = 0.1

class Car:
    def __init__(self, x=200, y=200):
        self.image = pygame.transform.scale(pygame.image.load("car.png"), CAR_SIZE)
        self.rect = pygame.Rect(x, y, CAR_SIZE[0], CAR_SIZE[1])
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0
        self.angle = 0
        self.turn_speed = 0
        self.turn_radius = 50
        self.max_speed = 10
        self.friction = 0.95

    
    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)

        pivot = pygame.math.Vector2(self.rect.x, self.rect.y + self.rect.height / 2)
        offset = pygame.math.Vector2(0, -self.rect.height / 2).rotate(self.angle)
        rotated_topleft = pivot + offset

        screen.blit(rotated_image, rotated_topleft)


    def update(self):
        self.velocity += (np.cos(np.radians(self.angle)) * self.acceleration, 
                          np.sin(np.radians(self.angle)) * self.acceleration)
        self.velocity *= self.friction

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.turn_speed != 0:
            self.angle += self.turn_speed * (self.velocity.length() / self.turn_radius)
            self.angle %= 360
            
    def control(self, keys):
        self.acceleration = self.acceleration * DRAG
        self.turn_speed = 0
        if keys[pygame.K_UP]:
            self.acceleration = 1
        if keys[pygame.K_DOWN]:
            self.acceleration = -0.1
        if keys[pygame.K_LEFT]:
            self.turn_speed = -25
        if keys[pygame.K_RIGHT]:
            self.turn_speed = 25
        
    