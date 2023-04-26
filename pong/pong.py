import time
import math
import numpy as np
import pygame
import tensorflow as tf
import pickle
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


class Paddle:
    def __init__(self, length, width, posx, posy, direction, screen):
        # constructor function, the function gets the position and messurements of the paddle
        # the function builds the paddle object
        self.start_y = (posx, posy)  # starting position
        self.length = length  # the length of the paddle
        self.width = width  # the width of the paddle
        self.posx = posx  # position x of the paddle
        self.posy = posy  # position y of the paddle
        self.screen = screen  # the size of the screen
        self.score = 0  # the score of the player playing the paddle
        # paddle hitbox (for graphics)
        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.length)

    def reset(self):
        # the function is called when a new point starts
        # the function returns the paddle to its original state
        self.posx = self.start_y[0]
        self.posy = self.start_y[1]

    def action(self, action):
        # the function gets an action: 0, 1 or 2
        # the function moves the paddle based on the action, 0 up and 2 down
        if action == 0:  # check if the action is 0
            self.posy -= 5  # move the paddle up
            if self.posy < 0:  # return the paddle in bounds of the screen
                self.posy = 0
        elif action == 2:  # check if the action is 2
            self.posy += 5  # move the paddle down
            # return the paddle in bounds of the screen
            if self.posy > self.screen[1] - self.length:
                self.posy = self.screen[1] - self.length

    def update_rect(self):
        # the function updates the hitbox of the paddle
        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.length)


class Ball:
    def __init__(self, posx, posy, speed, max_speed, dx, dy, direction, radius, screen, extra_x=0, extra_y=0):
        # constructor function, the function gets the position and messurements of the ball
        # the function builds the ball object
        # the starting state of the ball
        self.starting_state = (posx, posy, speed)
        self.posx = posx  # the position x of the ball
        self.posy = posy  # the position y of the ball
        self.speed = speed  # the current size of the speed
        self.max_speed = max_speed  # the max speed of the ball
        self.screen = screen  # the size of the playing screen
        self.direction_x = direction  # the direction the ball is going to on the x axis
        self.dx = dx  # speed in the x axis
        self.dy = dy  # speed in the y axis
        self.extra_x = extra_x  # the location x of the ball inside the pixel
        self.extra_y = extra_y  # the location y of the ball inside the pixel
        self.radius = radius  # the radius of the ball

    def copy(self):
        # the function creates a copy of the ball object
        return Ball(self.posx, self.posy, self.speed, self.max_speed, self.dx, self.dy, self.direction_x, self.radius, self.screen, self.extra_x, self.extra_y)

    def reset(self):
        # the function is called when a new point starts
        # the function returns the ball to its original state and starts moving it in a random direction (left/right)
        self.posx = self.starting_state[0]
        self.posy = self.starting_state[1]
        self.speed = self.starting_state[2]
        self.direction_x = np.random.randint(0, 2) * 2 - 1
        self.dx = self.direction_x * self.speed
        self.dy = 0
        self.extra_x = 0
        self.extra_y = 0

    def update(self):
        # the function updates the location of the ball based on its speed
        # adds the speed to the location inside the pixel
        self.extra_x += self.dx
        self.extra_y += self.dy
        # check if the ball is outside the pixel, if it is, move the location of the ball
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
        # check if the ball hit the side of the screen
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
        # the function gets the index of the pixel of the paddle that the ball hit and the length of the paddle
        # the function calculates the new speed and angle of the ball
        self.direction_x *= -1  # the ball switches direction
        middle = length / 2  # get the middle
        # find the distance of the pixel from the middle
        distance = 0
        if hit >= middle:
            distance = hit - middle
        else:
            distance = hit + 1 - middle
        # calculates the angle out of 90 degrees
        angle = distance / (length-2) * math.pi * 1 / 2
        # devide the speed to the x and y axises
        self.dx = math.cos(angle) * self.direction_x * self.speed
        self.dy = math.sin(angle) * self.speed

    def change_speed(self):
        # the function accelerates the ball, as long as its not faster than the max speed
        if self.speed < self.max_speed:
            self.speed += 0.2


class Env():
    def __init__(self):
        # constructor, the function builds an env object that handles the backend of the game
        # the size of the screen the game is played on
        self.screen = (800, 600)
        self.max_steps = 25000  # the max amount of frames a training game can last
        # the model that the ai uses
        self.model = self.make_model('python_proj\pong\pong_model.h5')
        # self.model = self.make_model()
        self.memory = []  # load the data to train the model on
        # with open(f"pythong_proj/pong/memory1.pickle", "rb") as f:
        # self.memory = pickle.load(f)
        with open(f"python_proj\pong\scaler.pickle", "rb") as f:  # load the scaler of the model
            self.scaler = pickle.load(f)
        # create the paddles
        self.paddle1 = Paddle(100, 5, 50, 265, 1, self.screen)
        self.paddle2 = Paddle(100, 5, 750, 265, -1, self.screen)
        # create a random direction for the ball
        num1 = np.random.randint(0, 2)
        self.ball = Ball(400, 300, 5, 10, num1 * 2 - 1,
                         0, num1 * 2 - 1, 3, self.screen)  # create the ball

    def check_win(self):
        # the function checks if someone won the point, returns 1 otherwise
        # check if the ball reached the left side of the screen
        if self.ball.posx == self.ball.radius:
            return 0
        # check if the ball reached the right side of the screen
        if self.ball.posx == self.screen[0] - self.ball.radius:
            return 2
        return 1

    def new_point(self):
        # the function starts a new point by reseting the ball and the paddles
        self.ball.reset()
        self.paddle1.reset()
        self.paddle2.reset()

    def new_game(self):
        # the function starts a new game
        self.new_point()
        self.paddle1.score = 0
        self.paddle2.score = 0

    def collect_data(self):
        # the function simulates a pong game and collects labels and inputs to train the network on
        memory_x = []  # the inputs
        memory_y = []  # the labels
        self.new_game()
        counter = 0  # amount of frames ran in the game
        # loop stops when a paddle win or when we reached the max amount of frames
        while self.paddle1.score < 10 and self.paddle2.score < 10 and counter < self.max_steps:
            counter += 1  # count the frame
            self.ball.update()  # update the ball's position
            state = [self.ball.posx, self.ball.posy, self.paddle1.posy + self.paddle1.length /
                     2, self.ball.dx, self.ball.dy, self.ball.extra_x, self.ball.extra_y]  # get the state (input for the network)
            if counter % 3 == 0:  # once every 3 frames, collect the frame, dont collect 80% of the frames when the network needs to stay in place
                if self.get_target() != [0, 1, 0] or np.random.rand() > 0.8:
                    # append the state and the label to the memory
                    memory_x.append(state)
                    memory_y.append(self.get_target())
            # move the paddle to keep to collect natural data
            self.paddle1.action(np.argmax(self.get_moves()))
            # move the oppesite paddle
            self.teleport2()
            # check for collisions with the paddles
            if self.ball.posx >= self.paddle1.posx and self.ball.posx <= self.paddle1.posx + self.ball.speed:
                if self.ball.posy >= self.paddle1.posy and self.ball.posy <= (self.paddle1.posy + self.paddle1.length):
                    self.ball.change_speed()  # add the speed from the hit
                    self.ball.hit_paddle(
                        self.ball.posy - self.paddle1.posy + self.ball.radius//2, self.paddle1.length)  # change the angle of the ball
                    # move the ball to the hit point with the paddle
                    self.ball.posx = self.paddle1.posx + self.paddle1.width
            if self.ball.posx + self.ball.radius - 1 >= self.paddle2.posx and self.ball.posx + self.ball.radius - 1 <= self.paddle2.posx + self.ball.speed:
                if self.ball.posy >= self.paddle2.posy and self.ball.posy <= (self.paddle2.posy + self.paddle2.length):
                    self.ball.change_speed()  # add the speed from the hit
                    self.ball.hit_paddle(
                        self.ball.posy - self.paddle2.posy + self.ball.radius//2, self.paddle2.length)  # change the angle of the ball
                    # move the ball to the hit point with the paddle
                    self.ball.posx = self.paddle2.posx - self.ball.radius
            # check if someone won the point, start a new point if someone won
            if self.check_win() == 0:
                self.paddle2.score += 1
                self.new_point()
            elif self.check_win() == 2:
                self.paddle1.score += 1
                self.new_point()
        # add the collected data to the data collected so far
        self.memory.append((np.array(memory_x), np.array(memory_y)))
        # return which paddle won
        if self.paddle1.score == 10:
            return 0
        return 2

    def teleport2(self):
        # the function moves the 2nd paddle to hit the ball, the function generates harder hits with steeper angles most of the time
        if np.random.rand() > 0.5:  # 50% of the time, the paddle will hit the ball randomly
            self.paddle2.posy = self.ball.posy - self.paddle2.length/2 + \
                np.random.randint(-self.paddle2.length/2,
                                  self.paddle2.length/2)  # move the paddle to hit the ball
        else:  # in the other 50% of the time, the paddle will hit the ball with its side, causing a steeper angle of the ball
            if np.random.rand() > 0.5:
                self.paddle2.posy = self.ball.posy - self.paddle2.length/2 + \
                    np.random.randint(self.paddle2.length /
                                      2 - 10, self.paddle2.length/2)  # hit the ball using the last 10 pixels of the paddle, causing a steep ball angle
            else:
                self.paddle2.posy = self.ball.posy - self.paddle2.length/2 + \
                    np.random.randint(-self.paddle2.length /
                                      2, -self.paddle2.length/2 + 10)  # hit the ball using the first 10 pixels of the paddle, causing a steep ball angle

    def update_env(self, game_type):
        # the function gets the game type
        # the fucntion moves the environment 1 frame forward
        self.ball.update()  # update the ball's location
        state = [self.ball.posx, self.ball.posy, self.paddle1.posy + self.paddle1.length /
                 2, self.ball.dx, self.ball.dy, self.ball.extra_x, self.ball.extra_y]  # generate the input for the model
        norm_state = self.scaler.transform([state])  # scale the input
        if game_type == 1:  # check if the ai play
            # generate the action of the model and play it
            act = np.argmax(self.model.predict_on_batch(norm_state)[0])
            self.paddle1.action(act)
        elif game_type == 3:  # check if the 2nd paddle is also controlled by the model
            # generate the action of the model and play it
            act = np.argmax(self.model.predict_on_batch(norm_state)[0])
            self.paddle1.action(act)
            state = [self.screen[0] - self.ball.posx, self.ball.posy, self.paddle2.posy +
                     self.paddle2.length/2, -self.ball.dx, self.ball.dy, -self.ball.extra_x, self.ball.extra_y]  # generate the input for the 2nd paddle, the oppesite of the 1st paddle's input
            norm_state = self.scaler.transform([state])  # scale the input
            # generate the action of the model and play it
            act = np.argmax(self.model.predict_on_batch(norm_state)[0])
            self.paddle2.action(act)
        if self.ball.posx >= self.paddle1.posx and self.ball.posx <= self.paddle1.posx + self.ball.speed:
            if self.ball.posy >= self.paddle1.posy and self.ball.posy <= (self.paddle1.posy + self.paddle1.length):
                self.ball.change_speed()  # add the speed from the hit
                self.ball.hit_paddle(
                    self.ball.posy - self.paddle1.posy + self.ball.radius//2, self.paddle1.length)  # change the angle of the ball
                # move the ball to the hit point with the paddle
                self.ball.posx = self.paddle1.posx + self.paddle1.width
        if self.ball.posx + self.ball.radius - 1 >= self.paddle2.posx and self.ball.posx + self.ball.radius - 1 <= self.paddle2.posx + self.ball.speed:
            if self.ball.posy >= self.paddle2.posy and self.ball.posy <= (self.paddle2.posy + self.paddle2.length):
                self.ball.change_speed()  # add the speed from the hit
                self.ball.hit_paddle(
                    self.ball.posy - self.paddle2.posy + self.ball.radius//2, self.paddle2.length)  # change the angle of the ball
                # move the ball to the hit point with the paddle
                self.ball.posx = self.paddle2.posx - self.ball.radius
        # check if someone won the point, start a new point if someone won
        if self.check_win() == 0:
            self.paddle2.score += 1
            self.new_point()
        elif self.check_win() == 2:
            self.paddle1.score += 1
            self.new_point()
        # update the hitboxes of the paddles
        self.paddle1.update_rect()
        self.paddle2.update_rect()

    def predict_hit_y(self):
        # the function returns the y position of the ball when it gets to the x position of the ai's paddle
        ball1 = self.ball.copy()  # make a copy of the ball
        if ball1.dx > 0:  # if the ball is moving away from the paddle, return the middle of the screen, so the paddle would return to the middle
            return 300
        else:
            # loop ends when the ball reaches the x position of the 1st paddle
            while ball1.posx > self.paddle1.posx + self.paddle1.width:
                ball1.update()  # update the position of the ball
        # return the y position of the ball when it gets to the x position of the ai's paddle
        return ball1.posy

    def get_target(self):
        # the function uses the frame inputs from the env
        # the fucntion returns the wanted output of the network
        # get the y position of the ball when it gets to the x position of the ai's paddle
        end1 = self.predict_hit_y()
        # calculates the distance from it to the middle of the paddle
        d = self.paddle1.posy + self.paddle1.length/2 - end1
        if d > 5:  # if the ball will end up above the middle, go up
            return [1, 0, 0]
        elif d < -5:  # if the ball will end up below the middle, go down
            return [0, 0, 1]
        return [0, 1, 0]  # else dont move

    def get_moves(self):
        # the function uses the frame inputs from the env
        # the fucntion moves the ai, but slows down its progress to create more states of moving, which happeneds less than not moving
        # get the y position of the ball when it gets to the x position of the ai's paddle
        end1 = self.predict_hit_y()
        # calculates the distance from it to the middle of the paddle
        d = self.paddle1.posy + self.paddle1.length/2 - end1
        if np.random.rand() > 0.65:  # 35% of the time, dont move
            return [0, 1, 0]
        elif d > 5:  # if the ball will end up above the middle, go up
            return [1, 0, 0]
        elif d < -5:  # if the ball will end up below the middle, go down
            return [0, 0, 1]
        return [0, 1, 0]  # else dont move

    def make_model(self, path=None):
        # the function gets a path
        # the function loads a model from the path or creates a new model
        if path == None:
            model = tf.keras.Sequential()  # create a new sequential model
            # add the input layer that gets 7 inputs: ball's position, position y of the paddle, ball's speed, and ball's location inside the pixel
            model.add(tf.keras.layers.Input(shape=(7,)))
            # add a fully connected layer with 256 neurons, with a RELU activation
            model.add(tf.keras.layers.Dense(256, activation='relu'))
            # add a fully connected layer with 256 neurons, with a RELU activation
            model.add(tf.keras.layers.Dense(256, activation='relu'))
            # add a fully connected layer with 128 neurons, with a RELU activation
            model.add(tf.keras.layers.Dense(128, activation='relu'))
            # add a fully connected layer with 128 neurons, with a RELU activation
            model.add(tf.keras.layers.Dense(128, activation='relu'))
            # add a fully connected layer with 64 neurons, with a RELU activation
            model.add(tf.keras.layers.Dense(64, activation='relu'))
            # add a fully connected layer with 64 neurons, with a RELU activation
            model.add(tf.keras.layers.Dense(64, activation='relu'))
            # add a fully connected layer with 32 neurons, with a RELU activation
            model.add(tf.keras.layers.Dense(32, activation='relu'))
            # add the output layer with activation of softmax
            model.add(tf.keras.layers.Dense(3, activation="softmax"))
            model.compile(optimizer=tf.keras.optimizers.Adam(
                learning_rate=0.0001), loss='categorical_crossentropy')  # compile the model with 0.0001 learning rate and categorical crossentropy loss function
            return model
        else:
            model = tf.keras.models.load_model(
                path)  # load the model from the path
            return model

    def train_model(self):
        # the function takes the collected data
        # the function creates a scaler and trains the model
        scaler = MinMaxScaler()  # create a new scaler
        # transform the memory to inputs and labels
        x = np.concatenate([i[0] for i in self.memory])
        y = np.concatenate([i[1] for i in self.memory])
        # scale the inputs and adjust the new scaler
        x = scaler.fit_transform(x)
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.1)  # split into test data
        # split the data into 100 batches
        x_train = np.array_split(x_train, 100)
        y_train = np.array_split(y_train, 100)
        for i in range(100):
            print(i, "% complete")
            self.model.fit(x_train[i], y_train[i],
                           epochs=2, validation_split=0.05)  # train the model twice on each batch
            # save the model, to allow stopping mid training
            self.model.save("python_proj/pong/pong_model.h5")
        # evaluate the model at the end of the training
        print(self.model.evaluate(x_test, y_test))
        with open(f"python_proj/pong/scaler.pickle", "wb") as f:
            pickle.dump(scaler, f)  # save the scaler

    def save_model(self):
        # the function saves the model and the data
        self.model.save("python_proj/pong/pong_model.h5")  # save the model
        with open(f"pong/memory2.pickle", "wb") as f:
            pickle.dump(self.memory, f)  # save the data


def main():
    env = Env()  # create a new env object
    for i in range(300):  # collect data of 300 matches
        env.collect_data()
    env.train_model()  # train the model
    env.save_model()  # save the model


if __name__ == "__main__":
    start = time.time()  # messure the time of the training
    main()
    end = time.time() - start
    print(
        f"the program took {int(end // 60)} minutes and {int(end % 60)} seconds to finish")
