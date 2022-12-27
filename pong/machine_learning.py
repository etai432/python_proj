from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from six.moves import urllib
import tensorflow as tf
from tensorflow import keras


def main():
    fashion_mnist = keras.datasets.fashion_mnist  # load dataset

    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()  # split into tetsing and training
    print(train_images[0, 23, 23])

if __name__ == "__main__":
    main();