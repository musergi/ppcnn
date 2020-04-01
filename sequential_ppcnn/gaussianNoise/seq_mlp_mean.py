import pickle
import tensorflow as tf


NODES = 7
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


if __name__ == "__main__":
    # Create network
    model = tf.keras.Sequential([
    tf.keras.layers.GaussianNoise(0.01, input_shape=(32, 32, 3)),
    tf.keras.layers.Flatten(),
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
            x_train, y_train = load_data('datasets/split7/datasplit%04d.pickle' % i)

            # Train network
            print("training network")
            iteration_model.fit(x_train, y_train, epochs=EPOCHS)

            # Save delta
            final_weights = iteration_model.get_weights()
            iteration_deltas = save_gradient(initial_weights, final_weights)
            deltas.append(iteration_deltas)

        # Calculate gradient mean
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
        model.save(MODEL_SAVE_PATH)
        
        metrics = model.evaluate(*test_data)
        with open("sequential_ppcnn/training_log_mlp.csv", 'a') as f:
            f.write(','.join([str(val) for val in list(metrics)]))
            f.write('\n')
        del model
        print(iteration, " model trained")