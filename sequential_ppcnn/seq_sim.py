import pickle
import tensorflow as tf


NODES = 5
MAX_EPOCHS = 10
EPOCHS = 1
MODEL_SAVE_PATH = 'temp.h5'


def load_data(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def save_gradient(weights, gradient):
    iteration_deltas = []
    for inital_layer_weights, final_layer_weights in zip(weights, gradient):
        iteration_deltas.append(final_layer_weights - inital_layer_weights)
    return iteration_deltas


if __name__ == "__main__":
    # Create network
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(32, 32, 3)),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    model.save(MODEL_SAVE_PATH)
    del model

    for i in range(NODES):
        #Load data
        print("Loading data in ", i)
        x_train, y_train = load_data('../datasets/datasplit%04d.pickle' % i)


    for epochs in range(int(MAX_EPOCHS/EPOCHS)):
        deltas = []
        for i in range(NODES):
            
            # Copy net
            print("Copying net")
            iteration_model = tf.keras.models.load_model(MODEL_SAVE_PATH)
            initial_weights = iteration_model.get_weights()
            
            # Train network
            print("training network")
            iteration_model.fit(x_train, y_train, epochs=EPOCHS)

            # Save delta
            final_weights = iteration_model.get_weights()
            model = tf.keras.models.load_model(MODEL_SAVE_PATH)
            model.set_weights(final_weights)
            
        # Save final model
        model.save(MODEL_SAVE_PATH)
        del model
        print(epochs)
        print(" model trained")