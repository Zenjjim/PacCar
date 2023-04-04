

import pygame
from pygame.math import Vector2
from math import sin, cos, tan, radians, degrees, copysign, pi, sqrt
from random import randint

""" Global Parameters """
SCALE = 4
CAR_SIZE = (50, 25)
""" Screen Parameters """
SCREEN_WIDTH = 128*SCALE
SCREEN_HEIGHT = 128*SCALE
GAME_TICKS = 60

""" Game Parameters """
NUM_OBSTACLES = 0

""" Map Parameters """
MAP_WIDTH = 254*SCALE
MAP_HEIGHT = 254*SCALE
BORDER = 4*SCALE

""" Vehicle Parameters """
VEHICLE_LENGTH = 11*SCALE     #(0.1m)
VEHICLE_WIDTH  = 5.5*SCALE     #(0.1m)
MASS   = 650/SCALE   #(kg)
C_DRAG_ROAD = 50     #0.4257
C_DRAG_GRASS = 50
C_BRAKE = 1000000
POS_BUFFER_LENGTH = 60

""" Obstacle Parameters """
OBSTACLE_LENGTH = 20*SCALE
OBSTACLE_WIDTH = 10*SCALE

DT = 1.0/GAME_TICKS

class Car:
    def __init__(self,x=100, y=100, orient=180, max_steer=0, max_speed=5, max_accel=5.0):
        self.position = Vector2(x,y)
        self.velocity = Vector2(0.0,0.0)
        self.acceleration = Vector2(0.0,0.0)
        self.engine_force = 0.0
        self.steer_angle = 0.0
        self.orient = orient
        self.brake_b = 0
        self.gear = 1
        self.prev_pos = Vector2(0,0)
        self.pos_buf = Vector2(0,0)
        self.terrain = 0
        self.drag = C_DRAG_ROAD
        self.RR = 30*self.drag
        self.ang_vel = 0

        self.image = pygame.transform.scale(pygame.image.load("car.png"), CAR_SIZE)
        self.rect = self.image.get_rect()
        self.rotated_image = self.image

        # Threshold Constants
        self.max_steer = max_steer
        self.max_speed = max_speed
        self.max_accel = max_accel
        
    def draw(self, screen):
        x = self.position.x - self.rect.size[0]/2
        y = self.position.y - self.rect.size[1]/2
        screen.blit(self.rotated_image, (x, y))

        
    ''' Calculate vehicle position '''
    def calculate(self, dt):
        pos_local  = Vector2(0.0,0.0)
        vel_local = Vector2(0.0,0.0)
        speed=sqrt(self.velocity.x*self.velocity.x + self.velocity.y*self.velocity.y)

        if(self.terrain == 1):
            self.steer_angle += randint(-2,2)

        self.ang_vel = 0

        if(self.steer_angle):
            circ_radius = VEHICLE_LENGTH / (sin(self.steer_angle))
            ang_vel = speed / circ_radius
            self.ang_vel = ang_vel
            # print("angular velocity = ", ang_vel)
            self.orient = (self.orient + ang_vel)%360

        heading = Vector2(cos(self.orient*pi/180.0),sin(-self.orient*pi/180.0))

        F_tract = self.engine_force*heading

        if( ((self.velocity.x>=0 and heading.x>=0)or(self.velocity.x<=0 and heading.x<=0)) and\
            ((self.velocity.y>=0 and heading.y>=0)or(self.velocity.y<=0 and heading.y<=0)) and\
             self.brake_b and (self.gear == 1) ):
            F_tract = -heading*C_BRAKE
        if( ((self.velocity.x<=0 and heading.x>=0)or(self.velocity.x>=0 and heading.x<=0)) and\
            ((self.velocity.y<=0 and heading.y>=0)or(self.velocity.y>=0 and heading.y<=0)) and\
             self.brake_b and (self.gear == 2) ):
            F_tract = heading*C_BRAKE
        F_drag = -self.drag*self.velocity
        self.RR = 30*self.drag
        F_rr = -self.RR*self.velocity                   #Rolling Resistance C_rr ~= 30*C_drag
        F_long = F_tract + F_drag + F_rr

        accel = F_long / MASS
        vel_local.x = self.velocity.x + (accel.x*dt)
        vel_local.y = self.velocity.y + (accel.y*dt)
        pos_local.x = self.position.x + (vel_local.x*dt)
        pos_local.y = self.position.y + (vel_local.y*dt)

        info = { "pos": pos_local, "vel": vel_local }
        return info


    ''' Update the vehicle information '''
    def update(self):
        car_info = self.calculate(DT)
        self.position.x = car_info["pos"].x
        self.velocity.x = car_info["vel"].x
        
        self.position.y = car_info["pos"].y
        self.velocity.y = car_info["vel"].y
        
        self.rotated_image = pygame.transform.rotate(self.image, -(self.steer_angle))

    def control(self, pressed):
        if pressed[pygame.K_LEFT]:
            self.setSteerAngle(-10)
        elif pressed[pygame.K_RIGHT]:
            self.setSteerAngle(10)
        else:
            self.setSteerAngle(0)
        if pressed[pygame.K_UP]:
            self.setEngineForce(-200000)
            self.setGear(2)
        elif pressed[pygame.K_DOWN]:
            self.setEngineForce(500000)
            self.setGear(1)
        elif pressed[pygame.K_b]:
            self.setBraking(1)
        else:
            self.setEngineForce(0)
            self.setBraking(0)

    def setGear(self,gear):
        self.gear=gear

    def setEngineForce(self,f):
        self.engine_force = f

    def setSteerAngle(self,a):
        self.steer_angle = a

    def setBraking(self,b):
        self.brake_b = b

    def getLength(self):
        return VEHICLE_LENGTH

    def getWidth(self):
        return VEHICLE_WIDTH

    def getPosition(self):
        return self.position

    def getVel(self):
        return self.velocity

    def getPrevPos(self):
        return self.prev_pos

    def getAccel(self):
        return self.acceleration

    def getOrientation(self):
        return self.orient

    def getAngVel(self):
        return self.ang_vel
