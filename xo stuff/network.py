import random
import csv
import numpy as np

class Network:
    
    def __init__(self, input1):
        self.input = input1
        self.input_arr = []
        self.output = 0
        self.p1 = Perceptron(self, 9)
        self.sum = 0
    
    def train_network(self):
        for i in range(0, len(self.input)):
            self.output = float(self.input[i][1])
            arr = list(np.fromstring(self.input[i][0][1:len(self.input[i][0])-1:], dtype=int, sep=' '))
            for j in arr:
                self.input_arr.append(Input_neuron(j))
            self.sum = self.p1.sum()
            self.p1.tweak_weights(self.output - self.sum)
            
    def predict(self, input):
        print(self.p1.pred(list(input)))
            
    def activation(self, value):
        return max(0, value)
    
    def input_arr1(self):
        return self.input_arr
    

class Input_neuron:
    
    def __init__(self, value):
        self.value = value
    

class Perceptron:
    
    def __init__(self, network, input_num):
        self.network = network
        self.bias = 0
        self.weights = []
        self.sum1 = 0
        self.result = 0
        for i in range(0, input_num):
            self.weights.append(0)
    
    def sum(self):
        arr = self.network.input_arr1()
        self.sum1 = self.bias
        for i in range(0, len(self.weights)):
            self.sum1 += arr[i].value * self.weights[i]
        self.result = self.network.activation(self.sum1)
        return self.sum1
        
    def tweak_weights(self, diff):
        arr = self.network.input_arr1()
        sum2 = 0
        for i in arr:
            sum2 += i.value
        tweak = diff/sum2 * 3
        add = 0
        self.bias += random.uniform(-abs(tweak), abs(tweak))
        l = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(l)
        for i in l:
            if self.weights[i] <= 1 and self.weights[i] >= 0:
                num1 = random.randint(0,2)
                if tweak > 0:
                    add = random.uniform(0, tweak)
                    tweak -= add
                    self.weights[i] += add * arr[i].value
                else:
                    add = random.uniform(tweak, 0)
                    tweak -= add
                    self.weights[i] += add * arr[i].value
    
    def pred(self, arr):
        self.sum1 = self.bias
        for i in range(0, len(self.weights)):
            self.sum1 += arr[i] * self.weights[i]
        self.result = self.network.activation(self.sum1)
        return self.sum1


file = open(r"xo stuff\xo_dict.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()
n1 = Network(data)
n1.train_network()
n1.predict([2, 0, 2, 0, 1, 2, 1, 0, 2])