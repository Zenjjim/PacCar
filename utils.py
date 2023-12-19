import math
import pygame
import matplotlib.pyplot as plt
from IPython import display 

plt.ion()
def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)

def key_hand(car):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car.move(-1)
    if keys[pygame.K_DOWN]:
        car.move(1)
    if keys[pygame.K_RIGHT]:
        car.turn(-1)
    if keys[pygame.K_LEFT]:
        car.turn(1)


def euchlidean_distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def intersection_line(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den
    if 0 < t < 1 and 0 < u < 1:
        return (x1 + t * (x2 - x1),
                    y1 + t * (y2 - y1))

def make_outline_loops(outline):
    loops = []

    def find_next_point(point):
        neighbors = [(point[0] + 1, point[1]), (point[0] - 1, point[1]), (point[0], point[1] + 1), (point[0], point[1] - 1)]
        for i in range(len(outline)):
            if point != outline[i] and outline[i] in neighbors:
                return outline.pop(i)

    while outline:
        loop = []
        first = outline.pop(0)
        loop.append(first)
        while True:
            next_point = find_next_point(loop[-1])
            if next_point:
                loop.append(next_point)
            else:
                break
        loops.append(loop)
    return loops

def tranform_points_to_lines(loops):
    new_loops = []
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for loop in loops:
        lines = []
        start_point = loop.pop(0)
        direction = None
        prev_point = start_point
        while len(loop) > 0:
            next_point = loop.pop(0)
            new_direction = (next_point[0] - prev_point[0], next_point[1] - prev_point[1])
            
            if direction == None:
                direction = new_direction
                prev_point = next_point
                continue
                
            if direction == new_direction:
                prev_point = next_point
                continue

            else:
                lines.append((start_point, prev_point))
                start_point = next_point
                prev_point = next_point
                direction = new_direction
                continue
            
        new_loops.append(lines)   
    return new_loops

            

def apply_kernel(mask, x, y):
    kernel = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    w, h = mask.get_size()
    for dx, dy in kernel:
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h:
            if not mask.get_at((nx, ny)):
                return True
    return False


def get_mask_outline(mask):
    outline = []
    w, h = mask.get_size()
    for x in range(w):
        for y in range(h):
            if mask.get_at((x, y)) and apply_kernel(mask, x, y):
                outline.append((x, y))
    return outline
