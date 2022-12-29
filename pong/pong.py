import time
import math
import numpy as np
import pygame
import tensorflow as tf
#1. predict best action
#2. do the action
#3.rate the wanted actions (0, 0.5, 1)
#4. update the model - model.fit(state, vec[action], epochs=1, verbose=0)
#TODO: hard code ai for paddle 2 (right paddle)
#TODO: make a training model function
#TODO: rewrite the rewarding system
#TODO: make a neural network using tensorflow | input = (ball.posx, posy, ball.posy, dx, dy) | output = (action 0, action 1, action 2)
#TODO: train against the hard coded paddle


class Paddle:
    def __init__(self, length, width, posx, posy, direction, screen):
        self.starting_state = (posx, posy)
        self.length = length
        self.width = width
        self.posx = posx
        self.posy = posy
        self.dir = direction
        self.screen = screen
        self.score = 0
        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.length)
    
    def reset(self):
        self.posx = self.starting_state[0]
        self.posy = self.starting_state[1]
    
    def action(self, action):
        if action == 0:
            self.posy -= 5
            if self.posy < 0:
                self.posy = 0
        elif action == 2:
            self.posy += 5
            if self.posy > self.screen[1] - self.length:
                self.posy = self.screen[1] - self.length
    
    def update_rect(self):
        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.length)


class Ball:
    def __init__(self, posx, posy, speed, max_speed, dx, dy, direction, radius, screen, extra_x=0, extra_y=0):
        self.starting_state = (posx, posy, speed)
        self.posx = posx
        self.posy = posy
        self.speed = speed
        self.max_speed = max_speed
        self.screen = screen
        self.direction_x = direction
        self.dx = dx * self.speed
        self.dy = dy * self.speed
        self.extra_x = extra_x
        self.extra_y = extra_y
        self.radius = radius
    
    def copy(self):
        return Ball(self.posx, self.posy, self.speed, self.max_speed, self.dx, self.dy, self.direction_x, self.radius, self.screen)
    
    def reset(self):
        self.posx = self.starting_state[0]
        self.posy = self.starting_state[1]
        self.speed = self.starting_state[2]
        self.direction_x = np.random.randint(0, 2) * 2 - 1
        self.dx = self.direction_x * self.speed
        self.dy = 0
        self.extra_x = 0
        self.extra_y = 0

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
        angle = distance / (length-2) * math.pi * 2 / 3
        self.dx = math.cos(angle) * self.direction_x * self.speed
        self.dy = math.sin(angle) * self.speed
    
    def change_speed(self):
        if self.speed < self.max_speed:
            self.speed += 0.1

class Env():
    def __init__(self):
        self.screen = (800, 600)
        self.fps = 24
        self.dict1 = {}
        self.dict2 = {}
        self.model = self.make_model()
        self.show = True
        if self.show:
            pygame.init()
            self.background = (0, 0, 0)
            self.game_screen = pygame.display.set_mode((800, 600))
            pygame.display.set_caption('pong')
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
        self.ball = Ball(400, 300, 5, 10, num1 * 2 - 1, 0, num1 * 2 - 1, 3, self.screen)
        self.score_pixel_size = 3

    def check_win(self):
        if self.ball.posx == 0:
            return 0
        if self.ball.posx == self.screen[0] - self.ball.radius:
            return 2
        return 1
    
    def new_point(self):
        self.ball.reset()
        self.paddle1.reset()
        self.paddle2.reset()
        if self.show:
            self.draw()
    
    def new_game(self):
        self.new_point()
        self.paddle1.score = 0
        self.paddle2.score = 0

    def random_play(self):
        # pos_arr1 = []
        # pos_arr2 = []
        self.new_game()
        running = True
        while self.paddle1.score < 10 and self.paddle2.score < 10 and running:
            frame_time = time.time()
            if self.show:
                pygame.display.flip()
            self.ball.update()
            start = time.time()
            pred = self.model.predict([self.ball.posx, self.ball.posy, self.paddle1.posy, self.ball.dx, self.ball.dy], verbose=0)[0]
            print(time.time() - start)
            # print(pred)
            self.paddle1.action(np.argmax(pred))
            self.paddle2.action(np.random.randint(0, 3))
            if self.ball.posx >= self.paddle1.posx and self.ball.posx <= self.paddle1.posx + self.ball.speed:
                if self.ball.posy >= self.paddle1.posy and self.ball.posy <= (self.paddle1.posy + self.paddle1.length):
                    # pos_arr1 = self.rate(pos_arr1, 10)
                    # self.save_to_dict(pos_arr1, self.dict1)
                    # pos_arr1 = []
                    self.ball.change_speed()
                    self.ball.hit_paddle(self.ball.posy - self.paddle1.posy + self.ball.radius//2, self.paddle1.length)
                    self.ball.posx = self.paddle1.posx + self.paddle1.width
            if self.ball.posx + self.ball.radius - 1 >= self.paddle2.posx and self.ball.posx + self.ball.radius - 1 <= self.paddle2.posx + self.ball.speed:
                if self.ball.posy >= self.paddle2.posy and self.ball.posy <= (self.paddle2.posy + self.paddle2.length):
                    # pos_arr2 = self.rate(pos_arr2, 10)
                    # self.save_to_dict(pos_arr2, self.dict2)
                    # pos_arr2 = []
                    self.ball.change_speed()
                    self.ball.hit_paddle(self.ball.posy - self.paddle2.posy + self.ball.radius//2, self.paddle2.length)
                    self.ball.posx = self.paddle2.posx - self.ball.radius
            if self.show:
                self.draw()
                for event in pygame.event.get():   
                    if event.type == pygame.QUIT:
                        running = False
            # pos_arr1.append((self.ball.posx, self.ball.posy, self.paddle1.posy, self.ball.dx, self.ball.dy))
            # pos_arr2.append((self.ball.posx, self.ball.posy, self.paddle2.posy, self.ball.dx, self.ball.dy))
            if self.check_win() == 0:
                self.paddle2.score += 1
                self.new_point()
                # pos_arr1 = self.rate(pos_arr1, -10)
                # self.save_to_dict(pos_arr1, self.dict1)
                # pos_arr1 = []
            elif self.check_win() == 2:
                self.paddle1.score += 1
                self.new_point()
                # pos_arr2 = self.rate(pos_arr2, -10)
                # self.save_to_dict(pos_arr2, self.dict2)
                # pos_arr2 = []
            if self.show:
                # time.sleep(1/self.fps - time.time() + frame_time)
                pass
            # print(1/self.fps - time.time() + frame_time)
        if self.paddle1.score == 10:
            return 0
        return 2

    def draw(self):
        self.game_screen.fill(self.background)
        pygame.draw.line(self.game_screen, (100, 100, 100), (self.screen[0] // 2, 0), (self.screen[0] // 2, self.screen[1]), 2)
        self.display((310, 20), self.paddle1.score)
        self.display((460, 20), self.paddle2.score)
        self.paddle1.update_rect()
        self.paddle2.update_rect()
        pygame.draw.rect(self.game_screen, (255, 255, 255), self.paddle1.rect)
        pygame.draw.rect(self.game_screen, (255, 255, 255), self.paddle2.rect)
        pygame.draw.circle(self.game_screen, (255, 255, 255), (self.ball.posx, self.ball.posy), self.ball.radius)

    def display(self, position, text, color=(255, 255, 255)):
        font = pygame.font.SysFont("Arial", 50, 50)
        text = font.render(str(text), True, color)
        self.game_screen.blit(text, position)

    def rate(self, boards, reward):
        rated = [(boards[0], reward)]
        current = reward
        for i in range(0, len(boards) - 1):
            if boards[i][2] != boards[i + 1][2]:
                current -= 0.1
            rated.append((boards[i + 1], current))
        return rated
    
    def save_to_dict(self, rated, dict1):
        for i in rated:
            if i[0] in dict1:
                dict1[i[0]] = ((dict1[i[0]][0] * dict1[i[0]][1] + i[1]) / (dict1[i[0]][1] + 1), dict1[i[0]][1] + 1)
            else:
                dict1[i[0]] = (i[1], 1)

    def save_dict(self):
        with open('pong/data1.csv', 'w') as output_file:
            for key in self.dict1:
                keys = list(key)
                for i in keys:
                    output_file.write("%s," % i)
                output_file.write("%s\n" % (self.dict1[key][0]))
        output_file.close()
        with open('pong/data2.csv', 'w') as output_file:
            for key in self.dict2:
                keys = list(key)
                for i in keys:
                    output_file.write("%s," % i)
                output_file.write("%s\n" % (self.dict2[key][0]))
        output_file.close()

    def predict_hit_y(self):
        ball1 = self.ball.copy()
        counter = 0
        if ball1.dx > 0:
            while ball1.posx < self.paddle2.posx:
                ball1.update()
                counter += 1
        else:
            while ball1.posx > self.paddle1.posx:
                ball1.update()
                counter += 1
        return (ball1.posy, counter)

    def get_target(self):
        (end, counter) = self.predict_hit_y()
        d = self.paddle1.posx - end + self.paddle1.length/2
        if d < 0 and d > -self.paddle1.length/2:
            return [0, 1, 0]
        if d > 0 and d > self.paddle1.length/2:
            return [0, 1, 0]
        if d > 0 and d // 5 + 1 < counter * 1.5:
            return [0, 1, 0.5]
        elif d > 0 and d // 5 + 1 > counter * 1.5:
            return [0, 0.3, 1]
        elif d < 0 and d // 5 - 1 > counter * 1.5:
            return [0.5, 1, 0]
        elif d < 0 and d // 5 - 1 < counter * 1.5:
            return [1, 0.3, 0]
        
    def make_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Input(shape=(1,)))
        model.add(tf.keras.layers.Dense(8))
        model.add(tf.keras.layers.Dense(3))
        model.compile(optimizer='Adam', loss='mse')
        return model
        
def main():
    env = Env()
    for i in range(100):
        env.random_play()
        if i % 1000 == 0:
            print(int(i / 100), "%")
    env.save_dict()

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time() - start
    print(f"the program took {int(end // 60)} minutes and {int(end % 60)} seconds to finish")
