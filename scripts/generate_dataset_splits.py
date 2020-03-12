"""Loads the svhn and saves it in multiple small splits. Ready to train from each of the different clients."""
import os
import argparse
import pickle
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds


def parse_args():
    """Parses the command line arguments and returns a dict"""
    parser = argparse.ArgumentParser()
    parser.add_argument('datasize', type=int)
    parser.add_argument('datacount', type=int)
    return parser.parse_args()



def generate_splits(arg_dict):
    """Returns the splits acording to the specified arguments."""
    size = arg_dict.datasize
    count = arg_dict.datacount
    samples = size * count

    dataset = tfds.load(name="svhn_cropped", split=tfds.Split.TRAIN)
    dataset_list = list(tfds.as_numpy(dataset))

    x, y = list(), list()
    for pair in dataset_list[:samples]:
        x.append(pair['image'])
        y.append(pair['label'])

    x = np.array(x) / 255
    y = tf.keras.utils.to_categorical(np.array(y))

    splits = list()
    for i in range(count):
        pair = x[i * size:(i + 1) * size], y[i * size:(i + 1) * size]
        splits.append(pair)

    return splits


def save_splits(splits):
    """Pickles the splits."""
    for index, split in enumerate(splits):
        save_str = 'datasplit%04d.pickle' % index
        save_path = os.path.join('datasets/split7', save_str)
        with open(save_path, 'wb') as f:
            pickle.dump(split, f)


if __name__ == "__main__":
    arg_dict = parse_args()
    splits = generate_splits(arg_dict)
    save_splits(splits)