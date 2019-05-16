from __future__ import print_function
from server import utils

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
