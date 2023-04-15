import math
import random
import pygame

from utils import euclidean_distance


class Lidar:
    def __init__(self, car, road, nr_of_rays=5, max_distance=100):
        self.car = car
        self.road = road
        self.nr_of_rays = int(nr_of_rays)
        self.max_distance = max_distance
        
        self.ray_angles = []
        ray_angle_increment = 360 / (self.nr_of_rays-1)
        for i in range(self.nr_of_rays):
            self.ray_angles.append(ray_angle_increment * i)
            
        self.rays = []
        for i in range(self.nr_of_rays):
            self.rays.append(Ray(i, pygame.math.Vector2(self.car.center.x, self.car.center.y), pygame.math.Vector2(0, 0), self.ray_angles[i], self.max_distance))
    
    def ml_values(self):
        return [{
            "idx": ray.idx, 
            "angle": ray.angle,
            "intersection_point": ray.intersection_point,
            "distance_to_wall": ray.distance_to_wall
                } for ray in self.rays]
        
    def update(self):
        for ray in self.rays:
            ray.update(self.car, self.road.road_walls)

    def draw(self, window):
        for ray in self.rays:
            ray.draw(window)  


class Ray:
    def __init__ (self, idx, start, stop, angle, max_distance):
        self.idx = idx
        self.start = start
        self.stop = stop
        self.angle = angle
        self.max_distance = max_distance
        self.intersection_point = None
        self.distance_to_wall = float("inf")
        
    def update(self, car, road_walls):
        self.start = pygame.math.Vector2(car.center.x, car.center.y)
        self.stop = pygame.math.Vector2(car.center.x + self.max_distance * math.cos(math.radians(self.angle + car.angle - 90)),
                                        car.center.y + self.max_distance * math.sin(math.radians(self.angle + car.angle - 90)))
        self.intersection_point = None
        self.distance_to_wall = float("inf")
        for wall in road_walls:
            if self.check_collision(wall):
                if self.intersection_point is None:
                    self.intersection_point = wall.intersection_point
                    self.distance_to_wall = euclidean_distance(car.center, wall.intersection_point)
                else:
                    distance_new = euclidean_distance(car.center, wall.intersection_point)
                    if distance_new < self.distance_to_wall:
                        self.intersection_point = wall.intersection_point
                        self.distance_to_wall = distance_new
                
    def draw(self, window):
        if self.intersection_point:
            pygame.draw.circle(window, (255, 0, 0), self.intersection_point, 5)
            pygame.draw.line(window, (0, 255, 0), self.start, self.intersection_point, 1)
        else:
            pygame.draw.line(window, (255, 0, 0), self.start, self.stop, 1)
            
    def check_collision(self, wall):
        p1, p2 = self.start, self.stop
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
            # Check if the intersection point lies within the range of both lines
            if (min(p1.x, p2.x) <= x <= max(p1.x, p2.x) and
                min(p1.y, p2.y) <= y <= max(p1.y, p2.y) and
                min(q1.x, q2.x) <= x <= max(q1.x, q2.x) and
                min(q1.y, q2.y) <= y <= max(q1.y, q2.y)):
                wall.intersection_point = pygame.math.Vector2(x, y)
                return True
        return False
    def add_random_lambda_to_vector(self, vec):
        return vec + ((random.random())*0.001, (random.random())*0.0001)
    
