import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
import time
import math
import copy

SCREEN = (160, 90)
FPS = 30
HM_EPISODES = 10
SHOW_EVERY = 1

epsilon = 0.99
DECAY = 0.99998

start_q_table = f"pong/q-table" 
start_q_table = None
start_q_table1 = f"pong/q-table" 

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
        self.hit = 0
        self.extra_y = 0
    
    def move(self):
        self.posx += int(self.speed) * self.direction
        self.extra_y += math.sin(self.angle) * self.speed
        if self.angle > 0:
            while self.extra_y > 1:
                self.extra_y -= 1
                self.posy += 1
        if self.angle < 0:
            while self.extra_y < -1:
                self.extra_y += 1
                self.posy -= 1
        if self.posy > SCREEN[1] - abs(self.extra_y) - 1 or self.posy < abs(self.extra_y):
            self.angle *= -1
            self.extra_y *= -1
        if self.posy == 90:
            self.posy -= 1
        if self.posx > SCREEN[0] - 1:
            self.posx = SCREEN[0] - 1
        elif self.posx < 0:
            self.posx = 0


    def calc_angle(self, hit, length):
        self.hit = hit
        self.angle = math.pi * (hit - length/2) / length * 1.8
        print(hit - length/2)
        print(self.angle)

    def change_speed(self):
        if self.speed < self.max_speed:
            self.speed += 0.2

def check_win():
    if ball.posx == 0:
        return 0
    if ball.posx == SCREEN[0] - 1:
        return 2
    return 1

def rate_obs(obs_list, score):
    list1 = []
    for i in range(len(obs_list)):
        list1.append((str(obs_list[i]).replace(" ","").replace(",","")[1:].replace(")",""), score * (0.9 ** (len(obs_list) - i - 1))))
    return list1

start = time.time()
bat1 = Bat(16, 1, 9, 36, 1)
bat2 = Bat(16, 1, 150, 36, -1)
ball = Ball(79, 44, 1, 0, 3, 1)
if start_q_table is None:
    q_table = {}
    q_table1 = {}
    # for dy in range(-SCREEN[1] + bat1.length, SCREEN[1]):
    #     for dx in range(0, bat2.posx - bat1.posx - 1):
    #         for hit in range(bat1.length):
    #             angle = math.pi * (hit - bat1.length/2) / bat1.length * 1.8
    #             q_table[(dx, dy, angle)] = [np.random.uniform(-5, 0) for i in range(3)]
    # q_table1 = copy.deepcopy(q_table)
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)
    with open(start_q_table1, "rb") as f:
        q_table1 = pickle.load(f)
env = np.zeros((SCREEN[1], SCREEN[0], 3), dtype=np.uint8)
episode_rewards = []
for episode in range(HM_EPISODES):
    bat1 = Bat(12, 1, 9, 38, 1)
    bat2 = Bat(12, 1, 150, 38, -1)
    num1 = np.random.randint(0, 2)
    ball = Ball(79, 44, 1, 0, 3, num1 * 2 - 1)
    show = False
    if episode % SHOW_EVERY == 0:
        if episode > 0:
            print(f"on # {episode}, epsilon: {epsilon}")
            print(f"{SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}")
            show = True
    else:
        show = False
    
    obs_list1 = []
    obs_list2 = []
    episode_reward = 0
    while check_win() == 1:
        frame_time = time.time()
        if ball.posx > bat1.posx and ball.posx <= bat2.posx:
            obs1 = (bat1.posx - ball.posx, bat1.posy - ball.posy, ball.hit)
            obs_list1.append(copy.deepcopy(obs1))
            str1 = str(obs1).replace(" ","").replace(",","")[1:].replace(")","")
            if str1 in q_table:
                if np.random.random() > epsilon:
                    pass
                    #TODO: make him choose the best option
                else:
                    action1 = np.random.randint(0, 3)
            else:
                # q_table[obs1] = [np.random.uniform(-5, 0) for i in range(3)]
                action1 = np.random.randint(0, 3)
            bat1.action(action1)
            obs2 = (bat2.posx - ball.posx, bat2.posy - ball.posy, ball.hit)
            obs_list2.append(copy.deepcopy(obs2))
            str1 = str(obs2).replace(" ","").replace(",","")[1:].replace(")","")
            if str1 in q_table1:
                if np.random.random() > epsilon:
                    pass
                    #TODO: make him choose the best option
                else:
                    action2 = np.random.randint(0, 3)
            else:
                # q_table1[obs2] = [np.random.uniform(-5, 0) for i in range(3)]
                action2 = np.random.randint(0, 3)
            bat2.action(action2)
        ball.move()

        if ball.posx - 1 == bat1.posx:
            if ball.posy >= bat1.posy and ball.posy <= (bat1.posy + bat1.length):
                ball.calc_angle(ball.posy - bat1.posy, bat1.length)
                ball.direction = 1
                ball.extra_y = 0
        if ball.posx + 1 == bat2.posx:
            if ball.posy >= bat2.posy and ball.posy <= (bat2.posy + bat2.length):
                ball.calc_angle(ball.posy - bat2.posy, bat2.length)
                ball.direction = -1
                ball.extra_y = 0
        

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
        obs_list1 = rate_obs(obs_list1, WIN_POINT_SCORE)
        obs_list2 = rate_obs(obs_list2, LOSE_POINT_SCORE)
    else:
        episode_reward += LOSE_POINT_SCORE
        obs_list2 = rate_obs(obs_list2, WIN_POINT_SCORE)
        obs_list1 = rate_obs(obs_list1, LOSE_POINT_SCORE)
    for i in obs_list1:
        if i[0] in q_table:
            q_table[i[0]] = ((q_table[i[0]][0] * q_table[i[0]][1] + i[1]) / (q_table[i[0]][1] + 1), q_table[i[0]][1] + 1)
        else:
            q_table[i[0]] = (i[1], 1)
    for i in obs_list2:
        if i[0] in q_table1:
            q_table1[i[0]] = ((q_table1[i[0]][0] * q_table1[i[0]][1] + i[1]) / (q_table1[i[0]][1] + 1), q_table1[i[0]][1] + 1)
        else:
            q_table1[i[0]] = (i[1], 1)
    episode_rewards.append(episode_reward) 
    epsilon *= DECAY
    print(episode)

with open(f"pong/q-table", "wb") as f:
    pickle.dump(q_table, f)
with open(f"pong/q-table1", "wb") as f:
    pickle.dump(q_table1, f)
print(time.time()- start)