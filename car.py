import pygame as py
import math

"""
Dry Asphalt:
Typical values range from 0.6 to 0.9.
A good average for most simulations might be around 0.7.
Wet Asphalt:
When wet, μ decreases, typically ranging from 0.2 to 0.5.
An average value could be around 0.3.
Snow or Ice Covered Roads:
On snow, μ might be around 0.1 to 0.3.
On ice, it can be even lower, sometimes below 0.1.
Gravel or Off-road:
On gravel roads, μ can vary widely but is generally in the range of 0.5 to 0.8.
Off-road conditions can have a wide range depending on the terrain.
"""


class Car():
    def __init__(self, pos = (100, 100), size = (15, 30), vel = 0, acc = 0, angle = 0):
        self.size = py.math.Vector2(size)

        self.pos = py.math.Vector2(pos)
        self.vel = vel
        self.acc = acc
        
        self.fric = 0.98
        self.drive_acc = .2
        self.turn_acc = .1
        self.turn_speed = 4.0

        self.angle = angle
        self.color = "GREEN"
        self.corners = []
        self.mask = None
        self.car_img = py.transform.scale(py.image.load("car.png"), size)

    def update(self):
        self.vel *= self.fric
        self.pos.x += math.sin(math.radians(self.angle)) * self.vel
        self.pos.y += math.cos(math.radians(self.angle)) * self.vel

    def check_collision(self, mask):
        if self.mask is None:
            return False
        col =  self.mask.overlap(mask, (int(self.pos.x), int(self.pos.y)))
        if col:
            self.color = "RED"
        else:
            self.color = "GREEN"
        return col

    def move(self, direction):
        self.vel += self.drive_acc * direction

    def turn(self, direction):
        self.vel += -self.turn_acc
        self.angle += self.turn_speed * direction
   
    def draw(self, screen):
        car_img = py.transform.rotate(self.car_img, self.angle)
        car_rect = car_img.get_rect()
        car_rect.center = self.pos
        self.mask = py.mask.from_surface(car_img)
        screen.blit(car_img, car_rect)
        # corners = []
        # radius = math.sqrt((self.size.y / 2)**2 + (self.size.x / 2)**2)
        # angle = math.atan2(self.size.y / 2, self.size.x / 2)
        # angles = [angle, -angle + math.pi, angle + math.pi, -angle]
        # rot_radians = math.radians(self.angle)
        # for angle in angles:
        #     y_offset = -1 * radius * math.sin(angle + rot_radians)
        #     x_offset = radius * math.cos(angle + rot_radians)
        #     corners.append((self.pos.x + x_offset, self.pos.y + y_offset))
        # self.corners = corners
        # rect = py.draw.polygon(screen, self.color, corners)
        # for angle in [-math.pi/2-6, -math.pi/2+6]:
        #     y_offset = -1 * radius * math.sin(angle + rot_radians)
        #     x_offset = radius * math.cos(angle + rot_radians)
        #     py.draw.circle(screen, "RED", (int(self.pos.x + x_offset), int(self.pos.y + y_offset)), 4)

        

        


