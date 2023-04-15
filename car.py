import math
import random
import pygame

import numpy as np


CAR_SIZE = (50, 25)
DRIFT_FACTOR = 0.5
SPEED = 0.1
TURN_SPEED = 10
DRAG = 0.95
BREAK = 0.9
DT = 0.1

class Car:
    def __init__(self, x=200, y=200, angle=0):
        self.image = pygame.image.load("car.png")
        self.rect = pygame.Rect(x, y, CAR_SIZE[0], CAR_SIZE[1])
        self.center = pygame.math.Vector2(self.rect.centerx, self.rect.centerx)
        self.font = pygame.font.SysFont("comicsansms", 20)
        
        self.last_position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0
        self.angle = angle
        self.turn_speed = 0
        self.turn_radius = 50
        self.max_speed = 10
        self.friction = 0.95
        self.crashed = False
        self.score = 0
        
        self.gate_reward = 10
        self.crased_punishment = -10
        
        self.init_value = {
            "x": x,
            "y": y,
            "angle": angle
        }
    def ml_values(self):
        return {
            "position": self.center,
            "velocity": self.velocity,
            "acceleration": self.acceleration,
            "angle": self.angle,
            "turn_speed": self.turn_speed,
            "crashed": self.crashed,
            "score": self.score
        }
        
    def draw(self, screen, alpha=255):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        scale_factor = max(self.max.x - self.min.x, self.max.y - self.min.y) / max(rotated_image.get_width(), rotated_image.get_height())
        scaled_image = pygame.transform.scale(rotated_image, ((rotated_image.get_width() * scale_factor), (rotated_image.get_height() * scale_factor)))
        
        scaled_image.set_alpha(alpha)
        
        image_rect = scaled_image.get_rect()
        image_rect.center = (self.center.x, self.center.y)
        screen.blit(scaled_image, image_rect.topleft)
        if alpha == 255: 
            rect_cord = self.calculate_rectangle_coordinates()
            lines = [
                (rect_cord[0], rect_cord[1]),
                (rect_cord[1], rect_cord[2]),
                (rect_cord[2], rect_cord[3]),
                (rect_cord[3], rect_cord[0])
            ]
            for line in lines:
                pygame.draw.line(screen, (0, 255, 0), *line, 3)
                
        # write self.score on top of car
        text = self.font.render(str(self.score), True, (255, 255, 255))
        screen.blit(text, (self.center.x - 10, self.center.y - 30))


    def update(self):
        if self.crashed:
            self.crashed = False
        
        rect_coor = self.calculate_rectangle_coordinates()
        
        x_values = [c.x for c in rect_coor]
        y_values = [c.y for c in rect_coor]
        self.min = pygame.math.Vector2(min(x_values), min(y_values))
        self.max = pygame.math.Vector2(max(x_values), max(y_values))
        self.center = pygame.math.Vector2((self.min.x + self.max.x) / 2, (self.min.y + self.max.y) / 2)
        
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
        self.acceleration = self.acceleration * self.friction
        self.turn_speed = self.turn_speed * DRIFT_FACTOR
    
    def forward(self):
        self.acceleration = SPEED
        
    def backward(self):
        self.acceleration = -SPEED/5
        
    def left(self):
        self.turn_speed = -TURN_SPEED
        
    def right(self):
        self.turn_speed = TURN_SPEED
        
    def check_collision(self, wall):
        rect_cord = self.calculate_rectangle_coordinates()
        lines = [
            (rect_cord[0], rect_cord[1]),
            (rect_cord[1], rect_cord[2]),
            (rect_cord[2], rect_cord[3]),
            (rect_cord[3], rect_cord[0])
        ]
        
        for i, line in enumerate(lines):
            p1, p2 = line[0], line[1]
            q1, q2 = wall.start, wall.stop
            p1 = self.add_random_lambda_to_vector(p1)
            p2 = self.add_random_lambda_to_vector(p2)
            q1 = self.add_random_lambda_to_vector(q1)
            q2 = self.add_random_lambda_to_vector(q2)
            # Calculate the slope and y-intercept of each line
            m1 = (p2.y - p1.y) / (p2.x - p1.x) if p2.x - p1.x != 0 else float('inf')
            m2 = (q2.y - q1.y) / (q2.x - q1.x) if q2.x - q1.x != 0 else float('inf')
            b1 = p1.y - m1 * p1.x
            b2 = q1.y - m2 * q1.x
            # Calculate the intersection point of the two lines
            if m1 != m2:
                x = (b2 - b1) / (m1 - m2)
                y = m1 * x + b1
                
                if (min(p1.x, p2.x) <= x <= max(p1.x, p2.x) and
                    min(p1.y, p2.y) <= y <= max(p1.y, p2.y) and
                    min(q1.x, q2.x) <= x <= max(q1.x, q2.x) and
                    min(q1.y, q2.y) <= y <= max(q1.y, q2.y)):
                    return True
        return False
           
    def add_random_lambda_to_vector(self, vec):
        return vec + ((random.random())*0.001, (random.random())*0.0001)
    
    def calculate_rectangle_coordinates(self):
        _rect = self.rect
        angle_rad = math.radians(self.angle)
        x1 = _rect.x
        y1 = _rect.y
        x2 = _rect.x + _rect.width * math.cos(angle_rad)
        y2 = _rect.y + _rect.width * math.sin(angle_rad)
        x3 = x2 - _rect.height * math.sin(angle_rad)
        y3 = y2 + _rect.height * math.cos(angle_rad)
        x4 = x3 - _rect.width * math.cos(angle_rad)
        y4 = y3 - _rect.width * math.sin(angle_rad)
        return [pygame.math.Vector2(x1, y1), pygame.math.Vector2(x2, y2), pygame.math.Vector2(x3, y3), pygame.math.Vector2(x4, y4)]
    

    def reset(self):
        self.rect.x = self.init_value["x"]
        self.rect.y = self.init_value["y"] 
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0
        self.angle = self.init_value["angle"]
        self.turn_speed = 0
        self.crashed = False
        self.score = 0