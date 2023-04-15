import pygame
import car
import road
import physics
import lidar

CAR_POSITION = pygame.math.Vector3(85, 450, -90)
LIDAR = pygame.math.Vector2(20, 500)

class Game:
    def __init__(self, idx, window):
        self.idx = idx
        self.car_obj = car.Car(*CAR_POSITION)
        self.road_obj = road.Road()
        self.lidar_obj = lidar.Lidar(self.car_obj, self.road_obj, *LIDAR)
        self.physics_obj = physics.PhysicsEngine(window, self.car_obj, self.road_obj)
        self.hidden = True
        
    def control(self, inpt):
        if inpt == "up":
            self.car_obj.forward()
        if inpt == "down":
            self.car_obj.backward()
        if inpt == "left":
            self.car_obj.left()
        if inpt == "right":
            self.car_obj.right()
        
    def update(self):
        self.car_obj.update()
        self.physics_obj.update()
        self.lidar_obj.update()
        
    def draw(self, window):
        if not self.hidden:
            self.road_obj.draw(window)
        alpha = 255 if not self.hidden else 100
        self.car_obj.draw(window, alpha)
        if not self.hidden:
            self.lidar_obj.draw(window)
        
    def reward(self):
        return self.car_obj.score
        
    def reset(self):
        self.car_obj.reset()
        self.road_obj.reset()
        self.physics_obj.reset()
        
    def ml_values(self):
        return {
            **self.car_obj.ml_values(),
            "rays": self.lidar_obj.ml_values()
        }