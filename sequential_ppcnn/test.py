import pickle
import tensorflow as tf

if __name__ == "__main__":
    data = None
    with open('datasets/test.pickle', 'rb') as f:
        data = pickle.load(f)

    model = tf.keras.models.load_model('temp.h5')
    model.evaluate(*data)