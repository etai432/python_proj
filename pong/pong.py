import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
import time
import math

SCREEN = (160, 90)
FPS = 30
HM_EPiSODES = 10
SHOW_EVERY = 1

epsilon = 0.9
EPS_DECAY = 0.9998

start_q_table = None # or filename

LEARNING_RATE = 0.1
DISCOUNT = 0.95

TOUCH_SCORE = 1
WIN_POINT_SCORE = 25
LOSE_POINT_SCORE = -25

class Bat:
    def __init__(self, length, width, posx, posy, direction):
        self.length = length
        self.width = width
        self.posx = posx
        self.posy = posy
        self.dir = direction
    
    def __sub__(self, other):
        return ((self.posx - other.posx) * self.dir, self.posy - other.posy)

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
        self.posx += int(math.cos(self.angle) * self.speed) * self.direction
        self.posy += int(math.sin(self.angle) * self.speed)
        if self.posy > SCREEN[1] - 2:
            self.posy = SCREEN[1] - 2

    def calc_angle(self, hit, length):
        self.angle = math.pi * (hit - length/2) / length * 1.8

    def change_speed(self, change):
        if self.speed < self.max_speed:
            self.speed += 0.2

def check_win(pixel_arr):
    for i in range(0, SCREEN[1], 2):
        if list(pixel_arr[i][0]) == [255, 255, 255]:
            return 0
        if list(pixel_arr[i][SCREEN[0]-1]) == [255, 255, 255]:
            return 2
    return 1

start = time.time()
bat1 = Bat(16, 2, 9, 36, 1)
bat2 = Bat(16, 2, 150, 36, -1)
ball = Ball(79, 44, 1, 0, 3, 1)
if start_q_table is None:
    q_table = {}
    for dy in range(-SCREEN[1] + bat1.length, SCREEN[1]-1):
        for dx in range(1, bat2.posx - bat1.posx - 1):
            for speed in range(10 ,ball.max_speed*10, 2):
                for hit in range(bat1.length):
                    angle = math.pi * (hit - bat1.length/2) / bat1.length * 1.8
                    q_table[(dx, dy, speed/10, angle)] = [np.random.uniform(-5, 0) for i in range(3)]
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)
pixels = np.zeros((SCREEN[1], SCREEN[0], 3), dtype=np.uint8)
episode_rewards = []
for episode in range(HM_EPiSODES):
    bat1 = Bat(16, 2, 9, 36, 1)
    bat2 = Bat(16, 2, 150, 36, -1)
    ball = Ball(79, 44, 1, 0, 3, 1)

    if episode % SHOW_EVERY == 0:
        print(f"on # {episode}, epsilon: {epsilon}")
        print(f"{SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}")
        show = True
    else:
        show = False
    
    episode_reward = 0
    while check_win(pixels) == 1:
        frame_time = time.time()
        obs1 = (abs(bat1.posx - ball.posx), bat1.posy - ball.posy, ball.speed, ball.angle)
        if np.random.random() > epsilon:
            action = np.argmax(q_table[obs1])
        else:
            action = np.random.randint(0, 4)
        bat1.action(action)
        obs2 = (abs(bat2.posx - ball.posx), bat2.posy - ball.posy, ball.speed, ball.angle)
        if np.random.random() > epsilon:
            action = np.argmax(q_table[obs1])
        else:
            action = np.random.randint(0, 4)
        bat1.action(action)
        #TODO: move ball

        #TODO: check touch

        #TODO: reward

        #TODO: new obs and qlearning

        if show:
            env = np.zeros((SCREEN[1], SCREEN[0], 3), dtype=np.uint8)
            #TODO: draw functions on bats and ball, use here

            img = Image.fromarray(env, "RGB")
            cv2.namedWindow("Window_name", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("Window_name", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("Window_name", np.array(img))
            if cv2.waitKey(int((1/FPS - time.time() + frame_time)*1000)) & 0xFF == ord("q"):
                    break
    episode_rewards.append(episode_reward) 
    epsilon *= EPS_DECAY

with open(f"pong/q-table", "wb") as f:
    pickle.dump(q_table, f)
print(time.time()- start)