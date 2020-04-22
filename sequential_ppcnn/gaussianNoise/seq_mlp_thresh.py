import pickle
import tensorflow as tf
import numpy as np
import random

NODES = 5
ITERATIONS = 100
EPOCHS = 1
MODEL_SAVE_PATH = 'temp_mlp.h5'


def load_data(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def save_gradient(weights, gradient):
    iteration_deltas = []
    for inital_layer_weights, final_layer_weights in zip(weights, gradient):
        iteration_deltas.append(final_layer_weights - inital_layer_weights)
    return iteration_deltas

def get_thresh_delta(delta):
    median_deltas = []
    max_deltas = []
    thresh_deltas = []
    nodes = range(0, len(deltas))
    layers = range(0, len(deltas[0]))
    for layer in layers:
        layer_weights = list()
        layer_max_delta = deltas[0][layer]
        for node in nodes:
            layer_weights.append(deltas[node][layer])
            layer_max_delta = np.maximum(layer_max_delta, deltas[node][layer])
        thresh_deltas.append(random.uniform(np.median(layer_weights, axis=0), layer_max_delta))
    return thresh_deltas

def get_min_delta(deltas):
    min_deltas = []
    deltas_count = len(deltas)     # Numero de deltas de distintos nodos
    layer_count = len(deltas[0])  # Numero de capas
    for layer_index in range(layer_count):
        layer_min_delta = deltas[0][layer_index]
        for node_index in range(1, deltas_count):
            layer_min_delta = np.minimum(layer_min_delta, deltas[node_index][layer_index])
        min_deltas.append(layer_min_delta)
    return min_deltas

if __name__ == "__main__":
    # Create network
    model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(32, 32, 3)),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
    model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    model.save(MODEL_SAVE_PATH)
    del model

    test_data = load_data('datasets/test.pickle')


    for iteration in range(int(ITERATIONS)):
        deltas = []
        for i in range(NODES):
            
            # Copy net
            print("Copying net")
            iteration_model = tf.keras.models.load_model(MODEL_SAVE_PATH)
            initial_weights = iteration_model.get_weights()
            
            # Load data
            print("Loading data")
            x_train, y_train = load_data('datasets/split5/datasplit%04d.pickle' % (i%5))

            # Train network
            print("training network")
            iteration_model.fit(x_train, y_train, epochs=EPOCHS)

            # Save delta
            final_weights = iteration_model.get_weights()
            iteration_deltas = save_gradient(initial_weights, final_weights)
            deltas.append(iteration_deltas)

        
        #Calculate gradient min
        #min_delta = get_min_delta(deltas)

        #Define threshold and apply it
        thresh_delta = get_thresh_delta(deltas)

        
        # Apply deltas
        model = tf.keras.models.load_model(MODEL_SAVE_PATH)
        new_weights = []
        for layer_weights, layer_deltas in zip(model.get_weights(), thresh_delta):
            new_weights.append(layer_weights + layer_deltas)
        model.set_weights(new_weights)

        # Save final model
        model.save(MODEL_SAVE_PATH)
        
        metrics = model.evaluate(*test_data)
        with open("sequential_ppcnn/training_log_mlp.csv", 'a') as f:
            f.write(','.join([str(val) for val in list(metrics)]))
        del model
        print(iteration, " model trained")