import numpy as np
from PIL import Image
import cv2
import time
import math
#TODO: change everything to match the balls size
#TODO: learn about kivy
#TODO: add the front-end to kivy
#TODO: add a scoring system- first to 10 wins
#TODO: add a rating system
#TODO: learn about DQN
#TODO: make a neural network using tensorflow | (ball.posx, posy, ball.posy, dx, dy)


class Paddle:
    def __init__(self, length, width, posx, posy, direction, screen):
        self.length = length
        self.width = width
        self.posx = posx
        self.posy = posy
        self.dir = direction
        self.screen = screen
        self.score = 0

    def action(self, action):
        if action == 0:
            self.posy -= 5
            if self.posy < 0:
                self.posy = 0
        elif action == 2:
            self.posy += 5
            if self.posy > self.screen[1] - self.length:
                self.posy = self.screen[1] - self.length
    
    def draw(self, pixels):
        for i in range(self.posy, self.posy + self.length):
            for j in range(self.posx, self.posx + self.width):
                pixels[i][j] = (255, 255, 255)

class Ball:
    def __init__(self, posx, posy, speed, max_speed, dx, dy, direction, radius, screen):
        self.posx = posx
        self.posy = posy
        self.speed = speed
        self.max_speed = max_speed
        self.screen = screen
        self.direction_x = direction
        self.dx = dx * self.speed
        self.dy = dy * self.speed
        self.extra_x = 0
        self.extra_y = 0
        self.radius = radius
    
    def update(self):
        self.extra_x += self.dx
        self.extra_y += self.dy
        while self.extra_y > 1:
            self.extra_y -= 1
            self.posy += 1
        while self.extra_y < -1:
            self.extra_y += 1
            self.posy -= 1
        while self.extra_x > 1:
            self.extra_x -= 1
            self.posx += 1
        while self.extra_x < -1:
            self.extra_x += 1
            self.posx -= 1
        if self.posy > self.screen[1] - self.extra_y - 1:
            self.posy = self.screen[1] - 1
            self.dy *= -1
            self.extra_y *= -1
        elif self.posy < self.radius:
            self.posy = self.radius - 1
            self.dy *= -1
            self.extra_y *= -1
        if self.posx > self.screen[0] - self.radius:
            self.posx = self.screen[0] - self.radius
        elif self.posx < 0:
            self.posx = 0

    def hit_paddle(self, hit, length):
        self.direction_x *= -1
        middle = length / 2
        distance = 0
        if hit >= middle:
            distance = hit - middle
        else:
            distance = hit + 1 - middle
        angle = distance / (length-2) * math.pi * 5 / 6
        self.dx = math.cos(angle) * self.direction_x * self.speed
        self.dy = math.sin(angle) * self.speed
    
    def change_speed(self):
        if self.speed < self.max_speed:
            self.speed += 0.1

    def draw(self, pixels):
        for i in range(self.radius):
            for j in range(self.radius):
                pixels[self.posy + i - self.radius + 1][self.posx + j] = (255, 255, 255)

class Env():
    def __init__(self):
        self.screen = (800, 600)
        self.fps = 30
        self.show = False
        if self.show:
            self.hm_episodes = 10
            self.show_every = 1
            self.epsilon = 0
        else:
            self.hm_episodes = 1000
            self.show_every = 10000
            self.epsilon = 1
        self.touch_score = 10
        self.miss_penalty = -10
        self.step_penalty = -0.1
        self.paddle1 = Paddle(70, 5, 50, 265, 1, self.screen)
        self.paddle2 = Paddle(70, 5, 750, 265, -1, self.screen)
        num1 = np.random.randint(0, 2)
        self.ball = Ball(400, 300, 5, 10, num1 * 2 - 1, 0, num1 * 2 - 1, 5, self.screen)
        self.env = np.zeros((self.screen[1], self.screen[0], 3), dtype=np.uint8)
        self.score_pixel_size = 3

    def check_win(self):
        if self.ball.posx == 0:
            return 0
        if self.ball.posx == self.screen[0] - self.ball.radius:
            return 2
        return 1
    
    def show_frame(self, frame_time):
        self.env = np.zeros((self.screen[1], self.screen[0], 3), dtype=np.uint8)
        self.ball.draw(self.env)
        self.paddle1.draw(self.env)
        self.paddle2.draw(self.env)
        img = Image.fromarray(self.env, "RGB")
        cv2.namedWindow("Window_name", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Window_name", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Window_name", np.array(img))
        cv2.waitKey(int((1/self.fps - time.time() + frame_time)*1000))
    
    def return_frame(self):
        self.env = np.zeros((self.screen[1], self.screen[0], 3), dtype=np.uint8)
        self.ball.draw(self.env)
        self.paddle1.draw(self.env)
        self.paddle2.draw(self.env)
        img = Image.fromarray(self.env, "RGB")
        return img

    def random_play(self):
        while self.check_win() == 1:
            frame = time.time()
            self.ball.update()
            self.paddle1.action(np.random.randint(0, 3))
            self.paddle2.action(np.random.randint(0, 3))
            if self.ball.posx >= self.paddle1.posx and self.ball.posx <= self.paddle1.posx + self.ball.speed:
                if self.ball.posy >= self.paddle1.posy and self.ball.posy <= (self.paddle1.posy + self.paddle1.length):
                    self.ball.change_speed()
                    self.ball.hit_paddle(self.ball.posy - self.paddle1.posy, self.paddle1.length)
                    self.ball.posx = self.paddle1.posx + self.paddle1.width
            if self.ball.posx + self.ball.radius - 1 >= self.paddle2.posx and self.ball.posx + self.ball.radius - 1 <= self.paddle2.posx + self.ball.speed:
                if self.ball.posy >= self.paddle2.posy and self.ball.posy <= (self.paddle2.posy + self.paddle2.length):
                    self.ball.change_speed()
                    self.ball.hit_paddle(self.ball.posy - self.paddle2.posy, self.paddle2.length)
                    self.ball.posx = self.paddle2.posx - self.ball.radius
            self.show_frame(frame)
        return self.check_win()

def main():
    env = Env()
    env.random_play()

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time() - start
    print(f"the program took {end // 60} minutes and {int(end % 60)} seconds to finish")
