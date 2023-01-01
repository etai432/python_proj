import time
import math
import numpy as np
import pygame
import tensorflow as tf
import pickle
import random
from sklearn.model_selection import train_test_split
#TODO: make a big saved memory, train a game from there


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
        return Ball(self.posx, self.posy, self.speed, self.max_speed, self.dx, self.dy, self.direction_x, self.radius, self.screen, self.extra_x, self.extra_y)
    
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
        self.max_steps = 100000
        # self.model = self.make_model()
        self.model = self.make_model('pong/pong_model.h5')
        self.show = True
        self.memory = []
        # with open(f"pong/memory.pickle", "rb") as f:
        #     self.memory = pickle.load(f)
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
        self.ball = Ball(400, 300, int(5 * 30 / self.fps), 7, num1 * 2 - 1, 0, num1 * 2 - 1, 3, self.screen)

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

    def train_network(self):
        memory_x = []
        memory_y = []
        self.new_game()
        counter = 0
        touch = 0
        running = True
        while self.paddle1.score < 10 and self.paddle2.score < 10 and running and counter < self.max_steps:
            frame_time = time.time()
            counter += 1
            if self.show:
                pygame.display.flip()
            self.ball.update()
            act = np.argmax(self.model.predict_on_batch(np.array([[self.ball.posx, self.ball.posy, self.paddle1.posy + self.paddle1.length/2, self.ball.dx, self.ball.dy]]))[0])
            # print(self.model.predict_on_batch(np.array([[self.ball.posx, self.ball.posy, self.paddle1.posy + self.paddle1.length/2, self.ball.dx, self.ball.dy]]))[0])
            a = self.get_target()
            self.paddle1.action(act)
            self.paddle2.action(self.ai2())
            # self.paddle2.posy = self.ball.posy - self.paddle2.length/2 + np.random.randint(-self.paddle2.length/2, self.paddle2.length/2)
            memory_x.append([self.ball.posx, self.ball.posy, self.paddle1.posy + self.paddle1.length/2, self.ball.dx, self.ball.dy])
            memory_y.append(a)
            # print(self.get_target())
            if self.ball.posx >= self.paddle1.posx and self.ball.posx <= self.paddle1.posx + self.ball.speed:
                if self.ball.posy >= self.paddle1.posy and self.ball.posy <= (self.paddle1.posy + self.paddle1.length):
                    self.ball.change_speed()
                    self.ball.hit_paddle(self.ball.posy - self.paddle1.posy + self.ball.radius//2, self.paddle1.length)
                    self.ball.posx = self.paddle1.posx + self.paddle1.width
                    touch += 1
            if self.ball.posx + self.ball.radius - 1 >= self.paddle2.posx and self.ball.posx + self.ball.radius - 1 <= self.paddle2.posx + self.ball.speed:
                if self.ball.posy >= self.paddle2.posy and self.ball.posy <= (self.paddle2.posy + self.paddle2.length):
                    self.ball.change_speed()
                    self.ball.hit_paddle(self.ball.posy - self.paddle2.posy + self.ball.radius//2, self.paddle2.length)
                    self.ball.posx = self.paddle2.posx - self.ball.radius
            if self.show:
                self.draw()
                for event in pygame.event.get():   
                    if event.type == pygame.QUIT:
                        running = False
            if self.check_win() == 0:
                self.paddle2.score += 1
                self.new_point()
            elif self.check_win() == 2:
                self.paddle1.score += 1
                self.new_point()
            if self.show:
                if 1/self.fps - time.time() + frame_time > 0:
                    time.sleep(1/self.fps - time.time() + frame_time)
                    pass
        print("frames:", counter)
        self.memory.append((np.array(memory_x), np.array(memory_y)))
        # batch = random.sample(self.memory, min(len(self.memory)//4 + 1, 32))
        # x_train = np.concatenate([i[0] for i in batch])
        # y_train = np.concatenate([i[1] for i in batch])
        # self.model.fit(x_train, y_train, verbose=0, epochs=1)
        print("touched:", touch)
        print("score: ", self.paddle1.score, "-", self.paddle2.score)
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

    def predict_hit_y(self):
        ball1 = self.ball.copy()
        if ball1.dx > 0:
            return 300
        else:
            while ball1.posx > self.paddle1.posx + self.paddle1.width:
                ball1.update()
        return ball1.posy

    def get_target(self):
        end1 = self.predict_hit_y()
        d = self.paddle1.posy + self.paddle1.length/2 - end1
        if d < 0 and d >= 15:
            return [0, 1, 0]
        elif d > 0 and d <= -15:
            return [0, 1, 0]
        elif d > 15:
            return [1, 0, 0]
        elif d < -15:
            return [0, 0, 1]
        return [0, 1, 0]
    
    def ai2(self):
        if self.ball.posy > self.paddle2.posy + self.paddle2.length - 8:
            return 2
        elif self.ball.posy < self.paddle2.posy + 8:
            return 0
        else:
            return np.random.randint(0, 3)
        
    def make_model(self, path=None):
        if path == None:
            model = tf.keras.Sequential()
            model.add(tf.keras.layers.Input(shape=(5,)))
            # model.add(tf.keras.layers.Dense(64, activation='relu'))
            # model.add(tf.keras.layers.Dense(64, activation='relu'))
            # model.add(tf.keras.layers.Dense(32, activation='relu'))
            model.add(tf.keras.layers.Dense(256, activation='relu'))
            model.add(tf.keras.layers.BatchNormalization())
            model.add(tf.keras.layers.Dense(256, activation='relu'))
            model.add(tf.keras.layers.BatchNormalization())
            model.add(tf.keras.layers.Dense(128, activation='relu'))
            model.add(tf.keras.layers.BatchNormalization())
            model.add(tf.keras.layers.Dense(128, activation='relu'))
            model.add(tf.keras.layers.BatchNormalization())
            model.add(tf.keras.layers.Dense(64, activation='relu'))
            model.add(tf.keras.layers.BatchNormalization())
            model.add(tf.keras.layers.Dense(64, activation='relu'))
            model.add(tf.keras.layers.BatchNormalization())
            model.add(tf.keras.layers.Dense(32, activation='relu'))
            model.add(tf.keras.layers.Dense(3, activation="softmax"))
            model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=["accuracy"])
            return model
        else:
            model = tf.keras.models.load_model(path)
            return model
    
    def train_model(self):
        x = np.concatenate([i[0] for i in self.memory])
        y = np.concatenate([i[1] for i in self.memory])
        x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.05)
        x_train = np.array_split(x_train, 100)
        y_train = np.array_split(y_train, 100)
        for i in range(100):
            print(i,"% complete")
            self.model.fit(x_train[i], y_train[i], epochs=5, validation_split=0.1)
        print(self.model.evaluate(x_test, y_test))

    def save_model(self):
        self.model.save("pong/pong_model.h5")
        with open(f"pong/memory.pickle", "wb") as f:
            pickle.dump(self.memory, f)
        with open(f"pong/memory1.pickle", "wb") as f:
            pickle.dump(self.memory, f)
        
def main():
    env = Env()
    for i in range(20000):
        env.train_network()
        print(i)
    # env.save_model()
    # env.train_model()
    # env.save_model()
    # env.train_network()


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time() - start
    print(f"the program took {int(end // 60)} minutes and {int(end % 60)} seconds to finish")
