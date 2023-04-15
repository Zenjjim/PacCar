import pygame

# Define game physics constants
GRAVITY = 9.81  # m/s^2

class PhysicsEngine:
    def __init__(self, window, car, road):
        # Set up physics engine properties
        self.window = window  # Pygame window object
        self.car = car # Car object
        self.road = road # Road wall object
        self.counter = 0 # Counter for physics updates
        self.old_score = 0
        self.is_reset = False
        
    def reset(self):
        self.old_score = 0
        self.counter = 0
        self.is_reset = False
        
    def update(self):
        scale = 2.1
        for wall in self.road.road_walls:
            if self.car.check_collision(wall):
                self.car.last_position = pygame.math.Vector2(self.car.rect.x-self.car.velocity.x*scale, self.car.rect.y-self.car.velocity.y*scale)
                self.car.velocity = pygame.math.Vector2(0, 0)
                self.car.acceleration = 0
                self.car.rect.x = self.car.last_position.x
                self.car.rect.y = self.car.last_position.y
                self.car.crashed = True
                wall.color = (255, 0, 0)
                wall.stroke = 10
                self.car.score += wall.point
                self.is_reset = True
            else:
                wall.color = wall.main_color
                wall.stroke = wall.main_stroke
        
        for gate in self.road.gates:
            if self.car.check_collision(gate):
                gate.touching = True
                if gate.active:
                    self.car.score += self.car.gate_reward
                    gate.active = False
            else:
                gate.touching = False
        
        punish = False
        if self.car.check_collision(self.road.finish_line):
            if not punish and not self.road.finish_line.touching:
                for gate in self.road.gates:
                    if gate.active:
                        punish = True
            self.road.finish_line.touching = True
        else:
            if self.road.finish_line.touching:
                if not punish:
                    for gate in self.road.gates:
                        gate.reset()
                    self.car.score += self.road.finish_line.point
            self.road.finish_line.touching = False
        
        if punish:
            self.car.score += -1 * self.road.finish_line.point
            self.is_reset = True
        
        if self.car.score > self.old_score:
            self.old_score = self.car.score
            self.counter = 0
            
        if self.counter >= 1000:
            self.car.score += -20
            self.is_reset = True
        
        self.counter += 1
        
  