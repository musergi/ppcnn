import pickle
import tensorflow as tf


NODES = 5
EPOCHS = 100
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


    deltas = []
    for i in range(NODES):
        #Load data
        x_train, y_train = load_data('datasets/datasplit%04d.pickle' % i)

        # Copy net
        iteration_model = tf.keras.models.load_model(MODEL_SAVE_PATH)
        initial_weights = iteration_model.get_weights()
        
        # Train network
        iteration_model.fit(x_train, y_train, epochs=EPOCHS)

        # Save delta
        final_weights = iteration_model.get_weights()
        iteration_deltas = save_gradient(initial_weights, final_weights)
        deltas.append(iteration_deltas)

    # Calculate deltas mean
    mean_deltas = []
    for layer in range(len(deltas[0])):
        mean_layer_deltas = None
        for node_deltas in deltas:
            if mean_layer_deltas is None:
                mean_layer_deltas = node_deltas[layer] / len(deltas)
            else:
                mean_layer_deltas = mean_layer_deltas + (node_deltas[layer] / len(deltas))
        mean_deltas.append(mean_layer_deltas)

    # Apply deltas
    model = tf.keras.models.load_model(MODEL_SAVE_PATH)
    new_weights = []
    for layer_weights, layer_deltas in zip(model.get_weights(), mean_deltas):
        new_weights.append(layer_weights + layer_deltas)
    model.set_weights(new_weights)

    # Save final model
    model.save('final.h5')

