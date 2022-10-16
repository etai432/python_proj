import os
import tensorflow as tf
from tensorflow import keras
import pandas as pd


def create_model():
    model = tf.keras.Sequential([
        keras.layers.Dense(512, activation='relu', input_shape=(784,)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])

    return model


def main():
    # dataset = pd.read_csv("pentago_dict.csv", names=["arr", "tuple"])
    # print(dataset.tail())
    # train_dataset = dataset.sample(frac=0.5, random_state=0)
    # test_dataset = dataset.drop(train_dataset.index)
    # train_features = train_dataset.copy()[1000:]
    # test_features = test_dataset.copy()[1000:]
    # train_labels = train_features.pop('arr')[1000:]
    # test_labels = test_features.pop('arr')[1000:]
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data("pentago_dict.csv")
    x_train = x_train.reshape(60000, 784).astype("float32") / 255
    x_test = x_test.reshape(10000, 784).astype("float32") / 255
    y_train = y_train.astype("float32")
    y_test = y_test.astype("float32")
    x_val = x_train[-10000:]
    y_val = y_train[-10000:]
    x_train = x_train[:-10000]
    y_train = y_train[:-10000]
    model = create_model()
    model.fit(x_train, y_train, epochs=100, verbose=0, validation_split=0.2, validation_data=(x_val, y_val))
    results = model.evaluate(x_test, y_test, batch_size=128)
    print("test loss, test acc:", results)
    print(x_test[0])
    print(model.predict(x_test[0]))
    print(model.predict(x_test[0]).shape)
    model.save('my_model.h5')


if __name__ == "__main__":
    main()
