
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split


def main():
    df1 = pd.read_csv("pong\data1.csv")
    df1.columns = ["ball x", "ball y", "pos y", "dx", "dy", "score"]
    print(df1)
    X = df1.drop("score", axis=1).to_numpy()
    y = df1["score"].to_numpy()
    X_train1, X_test1, y_train1, y_test1 = train_test_split(X,y,test_size=0.2)

    df2 = pd.read_csv("pong\data2.csv")
    df2.columns = ["ball x", "ball y", "pos y", "dx", "dy", "score"]
    print(df2)
    X = df2.drop("score", axis=1).to_numpy()
    y = df2["score"].to_numpy()
    X_train2, X_test2, y_train2, y_test2 = train_test_split(X,y,test_size=0.2)

if __name__ == "__main__":
    main();
    