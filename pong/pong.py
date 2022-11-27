import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time
import math

SCREEN = (512, 256)
HM_EPiSODES = 10
SHOW_EVERY = 1

epsilon = 0.9
EPS_DECAY = 0.9998

start_q_table = None # or filename

LEARNING_RATE = 0.1
DISCOUNT = 0.95

class Bat:
    def __init__(self, length, width, posx, posy, direction):
        self.length = length
        self.width = width
        self.posx = posx
        self.posy = posy
        self.dir = direction
    
    def __sub__(self, other):
        return ((self.posx - other.posx) * self.dir, (self.posy - other.posy) * self.dir)

    def action(self, action):
        if action == 0:
            self.posy -= 4
            if self.posy < 0:
                self.posy = 0
        elif action == 2:
            self.posy += 4
            if self.posy > SCREEN[1] - self.length:
                self.posy = SCREEN[1] - self.length

class Ball:
    def __init__(self, posx, posy, speed, angle, max, direction):
        self.posx = posx
        self.posy = posy
        self.speed = speed
        self.angle = angle
        self.max_speed = max
        self.direction = direction
    
    def move(self):
        self.posx += int(math.cos(self.angle) * self.speed)
        self.posy += int(math.sin(self.angle) * self.speed)
        if self.posy > SCREEN[1] - 2:
            self.posy = SCREEN[1] - 2

    def calc_angle(self, hit, length):
        self.angle = math.pi * (hit - length/2) / length * 1.8

    def change_speed(self, change):
        if self.speed < self.max_speed:
            self.speed += 0.1

bat1 = Bat(28, 2, 9, 113, 1)
bat2 = Bat(28, 2, 501, 113, -1)
ball = Ball(255, 127, 1, 0, 10, 1)
counter=0
if start_q_table is None:
    q_table = {}
    for dx in range(2-SCREEN[1] + bat1.length, SCREEN[1]-2):
        for dy in range(2-SCREEN[0]+bat1.posy, 0):
            for speed in range(10 ,ball.max_speed*10, 1):
                for hit in range(bat1.length):
                    # angle = math.pi * (hit - bat1.length/2) / bat1.length * 1.8
                    # q_table[(dx, dy, speed/10, angle)] = [np.random.uniform(-5, 0) for i in range(4)]
                    counter+=1
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)
print(counter)