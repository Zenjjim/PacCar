import math
import numpy as np
import pygame
import road


def draw_road_with_mouse(window, draw_road, is_clicked, placing_wall):
    pygame.draw.circle(window, (255, 255, 255), (pygame.mouse.get_pos()), 5)
    if pygame.mouse.get_pressed()[0]:
        if not is_clicked:
            placing_wall = True
            is_clicked = True
            x1, y1 = pygame.mouse.get_pos()
        else:
            x2, y2 = pygame.mouse.get_pos()
            pygame.draw.line(window, (255, 255, 255), (x1, y1), (x2, y2), 5)
    else:
        if placing_wall:
            x2, y2 = pygame.mouse.get_pos()
            draw_road.append(road.RoadWall(x1, y1, x2, y2))
            placing_wall = False
        is_clicked = False
            

def get_mouse_position_with_click():
    if pygame.mouse.get_pressed()[0]:
        print(f"mouse position: {pygame.mouse.get_pos()}")
        

def euclidean_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def preprocess_input(input_data):
    position = np.array([input_data['position'].x, input_data['position'].y])
    velocity = np.array([input_data['velocity'].x, input_data['velocity'].y])
    acceleration = np.array([input_data['acceleration']])
    angle = np.array([input_data['angle']])
    turn_speed = np.array([input_data['turn_speed']])
    crashed = np.array([float(input_data['crashed'])])
    score = np.array([input_data['score']])
    rays = np.array([ray['distance_to_wall'] for ray in input_data['rays']])

    return np.concatenate((position, velocity, acceleration, angle, turn_speed, crashed, score, rays))      
