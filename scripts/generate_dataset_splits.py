"""Loads the svhn and saves it in multiple small splits. Ready to train from each of the different clients."""


def parse_args():
    """Parses the command line arguments and returns a dict"""
    return None


def generate_splits(arg_dict):
    """Returns the splits acording to the specified arguments."""
    return None


def save_splits(splits):
    """Pickles the splits."""
    pass


if __name__ == "__main__":
    arg_dict = parse_args()
    splits = generate_splits(arg_dict)
    save_splits(splits)