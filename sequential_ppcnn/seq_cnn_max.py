import pickle
import tensorflow as tf


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


    for iteration in range(int(ITERATIONS)):
        deltas = []
        for i in range(NODES):
            
            # Copy net
            print("Copying net")
            iteration_model = tf.keras.models.load_model(MODEL_SAVE_PATH)
            initial_weights = iteration_model.get_weights()
            
            # Load data
            print("Loading data")
            x_train, y_train = load_data('datasets/datasplit%04d.pickle' % i)

            # Train network
            print("training network")
            iteration_model.fit(x_train, y_train, epochs=EPOCHS)

            # Save delta
            final_weights = iteration_model.get_weights()
            iteration_deltas = save_gradient(initial_weights, final_weights)
            deltas.append(iteration_deltas)

        # Calculate gradient max
        max_deltas = []
        for layer in range(len(deltas[0])):
            max_deltas.append(max(deltas[layer]))

        # Apply deltas
        model = tf.keras.models.load_model(MODEL_SAVE_PATH)
        new_weights = []
        for layer_weights, layer_deltas in zip(model.get_weights(), mean_deltas):
            new_weights.append(layer_weights + layer_deltas)
        model.set_weights(new_weights)

        # Save final model
        model.save(MODEL_SAVE_PATH)
        del model
        print(iteration, " model trained")