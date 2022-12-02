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
show = False
if show:
    HM_EPISODES = 10
    SHOW_EVERY = 1

    epsilon = 0
    START_EPSILON_DECAYING = 1
    END_EPSILON_DECAYING = HM_EPISODES * 2 // 3
    epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

    start_q_table = f"pong/q-table" 
    # start_q_table = None
    start_q_table1 = f"pong/q-table1" 
else:
    HM_EPISODES = 1000000
    SHOW_EVERY = 10000000

    epsilon = 1
    START_EPSILON_DECAYING = 1
    END_EPSILON_DECAYING = HM_EPISODES * 2 // 3
    epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

    start_q_table = f"pong/q-table" 
    start_q_table = None
    start_q_table1 = f"pong/q-table1" 

TEACH_MAIN = False

LEARNING_RATE = 0.1
DISCOUNT = 0.95

WIN_POINT_SCORE = 2
LOSE_POINT_SCORE = -2

class Bat:
    def __init__(self, length, width, posx, posy, direction):
        self.length = length
        self.width = width
        self.posx = posx
        self.posy = posy
        self.dir = direction
    
    def clone(self):
        return Bat(self.length, self.width, self.posx, self.posy, self.dir)
    
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
    
    def clone(self):
        return Ball(self.posx, self.posy, self.speed, self.angle, self.max_speed, self.direction)
    
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

    def change_speed(self):
        if self.speed < self.max_speed:
            self.speed += 0.2

def check_win(ball):
    if ball.posx == 0:
        return 0
    if ball.posx == SCREEN[0] - 1:
        return 2
    return 1

def rate_obs(obs_list, score):
    list1 = []
    for i in range(len(obs_list)):
        list1.append((str(obs_list[i]).replace(" ","").replace(",","")[1:].replace(")",""), score * (0.99 ** (len(obs_list) - i - 1))))
    return list1

def better_ai(bat, ball):
    if ball.posy > bat.posy + bat.length - 2:
        return 2
    elif ball.posy < bat.posy + 2:
        return 0
    else:
        return np.random.randint(0, 3)


def choose_next_turn(bat, ball1, q_table):
    best_action = -1
    max1 = -30
    copy_ball = ball1.clone()
    copy_ball.move()
    for used_action in range(3):
        copy_bat = bat.clone()
        copy_bat.action(used_action)
        obs = (copy_bat.posx - copy_ball.posx, copy_bat.posy - copy_ball.posy, copy_ball.hit)
        str2 = str(obs).replace(" ","").replace(",","")[1:].replace(")","")
        if str2 in q_table:
            if q_table[str2][0] > max1:
                best_action = used_action
                max1 = q_table[str2][0]
    if best_action == -1:
        best_action = np.random.randint(0, 3)
    return best_action
    
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

def play_2ai(epsilon):
    env = np.zeros((SCREEN[1], SCREEN[0], 3), dtype=np.uint8)
    for episode in range(HM_EPISODES):
        bat1 = Bat(12, 1, 9, 38, 1)
        bat2 = Bat(12, 1, 150, 38, -1)
        num1 = np.random.randint(0, 2)
        ball = Ball(79, 44, 1, 0, 3, num1 * 2 - 1)
        touch = 0
        touch1 = 0
        show = False
        if episode % SHOW_EVERY == 0:
            if episode > 0 or SHOW_EVERY == 1:
                print(f"on # {episode}, epsilon: {epsilon}")
                show = True
        else:
            show = False      
        obs_list1 = []
        obs_list2 = []
        while check_win(ball) == 1:
            frame_time = time.time()
            if ball.posx > bat1.posx and ball.posx <= bat2.posx:
                obs1 = (bat1.posx - ball.posx, bat1.posy - ball.posy, ball.hit)
                if ball.posx < SCREEN[0]/2:
                    obs_list1.append(copy.deepcopy(obs1))
                str1 = str(obs1).replace(" ","").replace(",","")[1:].replace(")","")
                if str1 in q_table:
                    if np.random.random() > epsilon:
                        action1 = choose_next_turn(bat1, ball, q_table)
                    else:
                        action1 = np.random.randint(0, 3)
                else:
                    action1 = np.random.randint(0, 3)
                bat1.action(action1)
                if not TEACH_MAIN:
                    obs2 = (bat2.posx - ball.posx, bat2.posy - ball.posy, ball.hit)
                    if ball.posx > SCREEN[0]:
                        obs_list2.append(copy.deepcopy(obs2))
                    str1 = str(obs2).replace(" ","").replace(",","")[1:].replace(")","")
                    if str1 in q_table1:
                        if np.random.random() > epsilon:
                            action2 = choose_next_turn(bat2, ball, q_table1)
                        else:
                            action2 = np.random.randint(0, 3)
                    else:
                        action2 = np.random.randint(0, 3)
                    bat2.action(action2)
                else:
                    bat2.action(better_ai(bat2, ball))
            ball.move()

            if ball.posx - 1 == bat1.posx:
                if ball.posy >= bat1.posy and ball.posy <= (bat1.posy + bat1.length):
                    touch += 1
                    ball.calc_angle(ball.posy - bat1.posy, bat1.length)
                    ball.direction = 1
                    ball.extra_y = 0
                    obs_list1 = rate_obs(obs_list1, 1)
                    for i in obs_list1:
                        if i[0] in q_table:
                            q_table[i[0]] = ((q_table[i[0]][0] * q_table[i[0]][1] + i[1]) / (q_table[i[0]][1] + 1), q_table[i[0]][1] + 1)
                        else:
                            q_table[i[0]] = (i[1], 1)
            if ball.posx + 1 == bat2.posx:
                if ball.posy >= bat2.posy and ball.posy <= (bat2.posy + bat2.length):
                    touch1 += 1
                    ball.calc_angle(ball.posy - bat2.posy, bat2.length)
                    ball.direction = -1
                    ball.extra_y = 0
                    obs_list2 = rate_obs(obs_list2, 1)
                    for i in obs_list2:
                        if i[0] in q_table1:
                            q_table1[i[0]] = ((q_table1[i[0]][0] * q_table1[i[0]][1] + i[1]) / (q_table1[i[0]][1] + 1), q_table1[i[0]][1] + 1)
                        else:
                            q_table1[i[0]] = (i[1], 1)
            

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
        if check_win(ball) != 1:
            obs_list1 = rate_obs(obs_list1, -2)
            obs_list2 = rate_obs(obs_list2 , -2)
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
        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
            epsilon -= epsilon_decay_value
        print(episode)

    with open(f"pong/q-table", "wb") as f:
        pickle.dump(q_table, f)
    if not TEACH_MAIN:
        with open(f"pong/q-table1", "wb") as f:
            pickle.dump(q_table1, f)
    print(time.time()- start)
    print(epsilon)

def main():
    play_2ai(epsilon)

if __name__ == "__main__":
    main()