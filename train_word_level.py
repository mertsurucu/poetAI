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

utils.create_sequences("a_tenth_data.txt", "a_tenth_data_sequences.txt")
lines = utils.load_doc("a_tenth_data_sequences.txt").split('\n')

tokenizer = Tokenizer()
tokenizer.fit_on_texts(lines)
sequences = tokenizer.texts_to_sequences(lines)

vocab_size = len(tokenizer.word_index) + 1

sequences = array(sequences)
X, y = sequences[:, :-1], sequences[:, -1]

y = to_categorical(y, num_classes=vocab_size)  # ------- MemoryError bu satırda

seq_length = X.shape[1]

#
# model = Sequential()
# model.add(Embedding(vocab_size, 50, input_length=seq_length))
# model.add(LSTM(100, return_sequences=True))
# model.add(LSTM(100))
# model.add(Dense(100, activation='relu'))
# model.add(Dense(vocab_size, activation='softmax'))
# print(model.summary())
#
#
# # compile model
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# # fit model
# model.fit(X, y, batch_size=128, epochs=5)
# # compile model
# model.save('model.h5')
# save the tokenizer
dump(tokenizer, open('tokenizer.pkl', 'wb'))

