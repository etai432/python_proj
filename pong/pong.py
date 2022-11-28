import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
import time
import math

SCREEN = (160, 90)
FPS = 30
HM_EPISODES = 100000
SHOW_EVERY = 100001

epsilon = 0.9
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = HM_EPISODES // 2
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)


start_q_table = None #f"pong/q-table"

LEARNING_RATE = 0.1
DISCOUNT = 0.95

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
            self.posy -= 1
            if self.posy < 0:
                self.posy = 0
        elif action == 2:
            self.posy += 1
            if self.posy > SCREEN[1] - self.length:
                self.posy = SCREEN[1] - self.length
    
    def draw(self, pixels):
        for i in range(self.posy, self.posy + self.length):
            for j in range(self.posx, self.posx + self.width):
                pixels[i][j] = (255, 255, 255)

class Ball:
    def __init__(self, posx, posy, speed, angle, max, direction):
        self.posx = posx
        self.posy = posy
        self.speed = speed
        self.angle = angle
        self.max_speed = max
        self.direction = direction
    
    def move(self):
        self.posx += int(self.speed) * self.direction
        self.posy += int(math.sin(self.angle) * self.speed)
        if self.posy > SCREEN[1] - 2 or self.posy < 1:
            self.angle *= -1
        if self.posx > SCREEN[0] - 1:
            self.posx = SCREEN[0] - 1
        elif self.posx < 0:
            self.posx = 0


    def calc_angle(self, hit, length):
        self.angle = math.pi * (hit - length/2) / length * 1.8

    def change_speed(self):
        if self.speed < self.max_speed:
            self.speed += 0.2

def check_win():
    if ball.posx == 0:
        return 0
    if ball.posx == SCREEN[0] - 1:
        return 2
    return 1

start = time.time()
bat1 = Bat(16, 1, 9, 36, 1)
bat2 = Bat(16, 1, 150, 36, -1)
ball = Ball(79, 44, 1, 0, 3, 1)
if start_q_table is None:
    q_table = {}
    for dy in range(-SCREEN[1] + bat1.length, SCREEN[1]):
        for dx in range(0, bat2.posx - bat1.posx - 1):
            for speed in range(10 ,ball.max_speed*10, 2):
                for hit in range(bat1.length):
                    angle = math.pi * (hit - bat1.length/2) / bat1.length * 1.8
                    q_table[(dx, dy, speed/10, angle)] = [np.random.uniform(-5, 0) for i in range(3)]
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)
env = np.zeros((SCREEN[1], SCREEN[0], 3), dtype=np.uint8)
episode_rewards = []
for episode in range(HM_EPISODES):
    bat1 = Bat(12, 1, 9, 38, 1)
    bat2 = Bat(12, 1, 150, 38, -1)
    ball = Ball(79, 44, 1, 0, 3, 1)
    show = False
    if episode % SHOW_EVERY == 0:
        if episode > 0:
            print(f"on # {episode}, epsilon: {epsilon}")
            print(f"{SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}")
            show = True
    else:
        show = False
    
    episode_reward = 0
    while check_win() == 1:
        frame_time = time.time()
        if ball.posx > bat1.posx and ball.posx <= bat2.posx:
            obs1 = (bat1.posx - ball.posx, bat1.posy - ball.posy, ball.speed, ball.angle)
            if obs1 in q_table:
                if np.random.random() > epsilon:
                    action1 = np.argmax(q_table[obs1])
                else:
                    action1 = np.random.randint(0, 3)
            else:
                q_table[obs1] = [np.random.uniform(-5, 0) for i in range(3)]
                action1 = np.random.randint(0, 3)
            bat1.action(action1)
            obs2 = (ball.posx - bat2.posx, bat2.posy - ball.posy, ball.speed, ball.angle)
            if obs2 in q_table:
                if np.random.random() > epsilon:
                    action2 = np.argmax(q_table[obs1])
                else:
                    action2 = np.random.randint(0, 3)
            else:
                q_table[obs2] = [np.random.uniform(-5, 0) for i in range(3)]
                action2 = np.random.randint(0, 3)
            bat2.action(action2)
        ball.move()

        if ball.posx - 1 == bat1.posx:
            if ball.posy >= bat1.posy and ball.posy <= (bat1.posy + bat1.length):
                ball.calc_angle(ball.posy - bat1.posy, bat1.length)
                ball.direction = 1
                ball.change_speed()
        if ball.posx + 1 == bat2.posx:
            if ball.posy >= bat2.posy and ball.posy <= (bat2.posy + bat2.length):
                ball.calc_angle(ball.posy - bat2.posy, bat2.length)
                ball.direction = -1
                ball.change_speed()
        
        new_obs1 = (bat1.posx - ball.posx, bat1.posy - ball.posy, ball.speed, ball.angle)
        if new_obs1 in q_table:
            max_future_q = np.max(q_table[new_obs1])
            current_q = q_table[obs1][action1]

            win = check_win()
            if win == 1:
                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (episode_reward + DISCOUNT * max_future_q)
            elif win == 2:
                new_q = WIN_POINT_SCORE
            else:
                new_q = LOSE_POINT_SCORE
            
            q_table[obs1][action1] = new_q
        else:
            q_table[new_obs1] = [np.random.uniform(-5, 0) for i in range(3)]

        if show:
            env = np.zeros((SCREEN[1], SCREEN[0], 3), dtype=np.uint8)
            env[ball.posy][ball.posx] = (255, 255, 255)
            bat1.draw(env)
            bat2.draw(env)
            img = Image.fromarray(env, "RGB")
            cv2.namedWindow("Window_name", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("Window_name", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("Window_name", np.array(img))
            cv2.waitKey(int((1/FPS - time.time() + frame_time)*1000))
    if check_win() == 2:
        episode_reward += WIN_POINT_SCORE
    else:
        episode_reward += LOSE_POINT_SCORE
    episode_rewards.append(episode_reward) 
    if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
        epsilon -= epsilon_decay_value

with open(f"pong/q-table", "wb") as f:
    pickle.dump(q_table, f)
print(time.time()- start)