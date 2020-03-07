import pickle
import tensorflow as tf


def load_data(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    # Create network
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(32, 32, 3)),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()

    x_train, y_train = load_data('datasets/datasplit0000.pickle')
    model.fit(x_train, y_train, epochs=10)