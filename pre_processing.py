from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import io
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
import utils

from numpy import array
from pickle import dump
import time


def create_sequences(data_path, output_path):
    s = time.time()
    print("load")
    doc = utils.load_doc(data_path)
    print("load", time.time()-s)
    s1 = time.time()

    print("clean")
    tokens = utils.clean_doc(doc)
    print("clean", time.time()-s1)
    s2 = time.time()

    print("create")
    sequences = utils.create_sequences(tokens)
    print("create", time.time()-s2)
    s3 = time.time()

    print("save")
    utils.save_doc(sequences, output_path)
    print("save", time.time()-s3)


# create_sequences("a_tenth_data.txt", "a_tenth_data_sequences.txt")
