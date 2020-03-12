import pickle
import tensorflow as tf
import numpy as np

NODES = 5
ITERATIONS = 20
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

def get_max_delta(deltas):
    max_deltas = []
    deltas_count = len(deltas)     # Numero de deltas de distintos nodos
    layer_count = len(deltas[0])  # Numero de capas
    for layer_index in range(layer_count):
        layer_max_delta = deltas[0][layer_index]
        for node_index in range(1, deltas_count):
            layer_max_delta = np.maximum(layer_max_delta, deltas[node_index][layer_index])
        max_deltas.append(layer_max_delta)
    return max_deltas

if __name__ == "__main__":
    # Create network
    model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(256, kernel_size=(3, 3), activation='relu', input_shape=(32, 32, 3)),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
            tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(10, activation='softmax')])

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
            x_train, y_train = load_data('datasets/split5/datasplit%04d.pickle' % i)

            # Train network
            print("training network")
            iteration_model.fit(x_train, y_train, epochs=EPOCHS)

            # Save delta
            final_weights = iteration_model.get_weights()
            iteration_deltas = save_gradient(initial_weights, final_weights)
            deltas.append(iteration_deltas)

        # Calculate gradient max
        max_deltas = get_max_delta(deltas)

        # Apply deltas
        model = tf.keras.models.load_model(MODEL_SAVE_PATH)
        new_weights = []
        for layer_weights, layer_deltas in zip(model.get_weights(), max_deltas):
            new_weights.append(layer_weights + layer_deltas)
        model.set_weights(new_weights)

        # Save final model
        model.save(MODEL_SAVE_PATH)
        
        metrics = model.evaluate(*test_data)
        with open("sequential_ppcnn/training_log_cnn_rep.csv", 'a') as f:
            f.write(','.join([str(val) for val in list(metrics)]))
        del model
        print(iteration, " model trained")