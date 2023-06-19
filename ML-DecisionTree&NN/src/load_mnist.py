# DDA3020 Assignment 3 - Programming 2
import os 
import numpy as np
import gzip
'''
This python script for DDA3020 Assignment 3 - Programming 2.
Load mnist data from given path and return them in numpy ndaray Uint8 (Value from [0,255])/binary {0,1} format matrix/vector(Using flatten option).
Make this python file with same path with your code.
Given the correct path which contain the mnist data.
you can simply "from load_minist import load_mnist" and use it.
eg. the "./" is the current path and contains the mnist data 4 gz files.
i) flatten = False return sample in matrix formula (28,28)
X_train,X_test,Y_train,Y_test  = load_mnist(path = './', flatten = False) 
# return X_train (60000, 28, 28), X_test (10000, 28, 28), Y_train (60000,), Y_test (10000,)
ii) flatten = True return sample in vector formula (784,) 
X_train,X_test,Y_train,Y_test  = load_mnist(path = './', flatten = True)
# return X_train (60000, 784), X_test (10000, 784), Y_train (60000,), Y_test (10000,)  
The "binary_data" option is for binary data format, default is False.
iii) X_train,X_test,Y_train,Y_test  = load_mnist(path = './', flatten = True, binary_data = False)
# return X_train (60000, 784), X_test (10000, 784), Y_train (60000,), Y_test (10000,)  
# This is coincide with sklearn.datasets fetch_openml mnist data format.
'''

def load_mnist(path ='./', flatten = False, binary_data = False):
    """
    Get mnist data from given path
    load them in binary format.

    Parameters
    ----------
    path, default = './' : str
    Make sure the path is correct and Contains the following files: 
    'train-images-idx3-ubyte.gz',
    'train-labels-idx1-ubyte.gz',
    't10k-images-idx3-ubyte.gz',
    't10k-labels-idx1-ubyte.gz'
    Return
    ------
    tuple, (train_images, test_images, train_labels,  test_labels)   ·
    tuple[0] are images (train)
    tuple[1] are images (test)
    tuple[2] are labels (train)
    tuple[3] are labels (test)

    """
    RESOURCES = [
        'train-images-idx3-ubyte.gz',
        'train-labels-idx1-ubyte.gz',
        't10k-images-idx3-ubyte.gz',
        't10k-labels-idx1-ubyte.gz']
    if binary_data:
       X,Y = get_images(path,binary_data), get_labels(path) 
    else: 
        X,Y = get_images(path), get_labels(path)
    
    X_train, X_test = X
    Y_train, Y_test = Y
    del X, Y  # free up memory
    
    assert X_train.shape == (60000, 28, 28)
    assert X_test.shape == (10000, 28, 28)
    assert Y_train.shape == (60000,)
    assert Y_test.shape == (10000,)
   
    if flatten:
        X_train = X_train.reshape(-1, 784)
        X_test = X_test.reshape(-1, 784) 
    return X_train, X_test, Y_train, Y_test


def get_images(path = './',binary_data = False):

    to_return = []

    with gzip.open(path + 'train-images-idx3-ubyte.gz', 'r') as f:
        # first 4 bytes is a magic number
        magic_number = int.from_bytes(f.read(4), 'big')
        # second 4 bytes is the number of images
        image_count = int.from_bytes(f.read(4), 'big')
        # third 4 bytes is the row count
        row_count = int.from_bytes(f.read(4), 'big')
        # fourth 4 bytes is the column count
        column_count = int.from_bytes(f.read(4), 'big')
        # rest is the image pixel data, each pixel is stored as an unsigned byte
        # pixel values are 0 to 255
        image_data = f.read()
        train_images = np.frombuffer(image_data, dtype=np.uint8)\
            .reshape((image_count, row_count, column_count))
        if binary_data:
            to_return.append(np.where(train_images > 127, 1, 0))
        else:
            to_return.append(train_images)

    with gzip.open(path + 't10k-images-idx3-ubyte.gz', 'r') as f:
        # first 4 bytes is a magic number
        magic_number = int.from_bytes(f.read(4), 'big')
        # second 4 bytes is the number of images
        image_count = int.from_bytes(f.read(4), 'big')
        # third 4 bytes is the row count
        row_count = int.from_bytes(f.read(4), 'big')
        # fourth 4 bytes is the column count
        column_count = int.from_bytes(f.read(4), 'big')
        # rest is the image pixel data, each pixel is stored as an unsigned byte
        # pixel values are 0 to 255
        image_data = f.read()
        test_images = np.frombuffer(image_data, dtype=np.uint8)\
            .reshape((image_count, row_count, column_count))
        if binary_data:
            to_return.append(np.where(test_images > 127, 1, 0))
        else:
            to_return.append(test_images)

    return to_return


def get_labels(path = './'):

    to_return = []


    with gzip.open(path + 'train-labels-idx1-ubyte.gz', 'r') as f:
        # first 4 bytes is a magic number
        magic_number = int.from_bytes(f.read(4), 'big')
        # second 4 bytes is the number of labels
        label_count = int.from_bytes(f.read(4), 'big')
        # rest is the label data, each label is stored as unsigned byte
        # label values are 0 to 9
        label_data = f.read()
        train_labels = np.frombuffer(label_data, dtype=np.uint8)
        to_return.append(train_labels)

    with gzip.open(path + 't10k-labels-idx1-ubyte.gz', 'r') as f:
        # first 4 bytes is a magic number
        magic_number = int.from_bytes(f.read(4), 'big')
        # second 4 bytes is the number of labels
        label_count = int.from_bytes(f.read(4), 'big')
        # rest is the label data, each label is stored as unsigned byte
        # label values are 0 to 9
        label_data = f.read()
        test_labels = np.frombuffer(label_data, dtype=np.uint8)
        to_return.append(test_labels)

    return to_return


if __name__ == "__main__":
        X_train,X_test,Y_train,Y_test  = load_mnist(path = './', flatten = False,binary_data = True)
        assert X_train.shape == (60000, 28, 28)
        assert X_test.shape == (10000, 28, 28)
        assert Y_train.shape == (60000,)
        assert Y_test.shape == (10000,)
        X_train,X_test,Y_train,Y_test  = load_mnist(path = './', flatten = True,binary_data = True) 
        assert X_train.shape == (60000, 784)
        assert X_test.shape == (10000, 784)
        assert Y_train.shape == (60000,)
        assert Y_test.shape == (10000,)
        X_train,X_test,Y_train,Y_test  = load_mnist(path = './', flatten = True, binary_data=False) 
        assert X_train.shape == (60000, 784)
        assert X_test.shape == (10000, 784)
        assert Y_train.shape == (60000,)
        assert Y_test.shape == (10000,)
        print("Test passed and data loaded successfully.")