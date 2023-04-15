import pygame
import game
import road
import ml

WIDTH, HEIGHT = 1500, 800
FPS = 60

import pygame
class MyGame:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.ml_obj = ml.ML([game.Game(i, self.window) for i in range(3)])
        self.is_clicked = False
        self.placing_wall = False
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
  
    def draw_road_gates(self):
        pygame.draw.circle(self.window, (255, 0, 0), (pygame.mouse.get_pos()), 5)
        if pygame.mouse.get_pressed()[0]:
            if not self.is_clicked:
                self.placing_wall = True
                self.is_clicked = True
                self.x1, self.y1 = pygame.mouse.get_pos()
            else:
                self.x2, self.y2 = pygame.mouse.get_pos()
                pygame.draw.line(self.window, (255, 255, 0), (self.x1, self.y1), (self.x2, self.y2), 5)
        else:
            if self.placing_wall:
                self.x2, self.y2 = pygame.mouse.get_pos()
                self.ml_obj.games[0].road_obj.gates.append(road.RoadGate(self.x1, self.y1, self.x2, self.y2))
                self.placing_wall = False
            self.is_clicked = False

        
    def update(self):
        self.ml_obj.update()
        pass

    def draw(self):
        self.window.fill((51, 51, 51))
        self.ml_obj.draw(self.window)
        # self.draw_road_gates()
        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        # print(self.ml_obj.games[0].road_obj.gates)

    def reset(self):
        self.ml_obj.reset()
        
if __name__ == "__main__":
    pygame.init()
    game = MyGame()
    game.run()
    pygame.quit()
