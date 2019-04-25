

from __future__ import print_function
from keras.callbacks import LambdaCallback, Callback
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import io
import os
import utils
import time
from datetime import datetime

text = utils.load_doc("combined_ask_mutluluk.txt")

print('corpus length:', len(text))

chars = sorted(list(set(text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 100
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

sentences.clear()
# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(1024, input_shape=(maxlen, len(chars))))
model.add(Dense(512, activation='relu'))
model.add(Dense(len(chars), activation='softmax'))

optimizer = RMSprop(lr=0.001)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


t = str(datetime.today())
file_time = "out/" + t[:t.index('.')] + ".txt"
file_time = file_time.replace(':', '_')


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def generate_text(diversity=0.5, range_=1000):

    start_index = random.randint(0, len(text) - maxlen - 1)
    sentence = text[start_index: start_index + maxlen]
    generated = ""
    for i in range(range_):
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_indices[char]] = 1.

        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char
    return generated



def on_epoch_end(epoch, logs):
    log = open(file_time, "a", encoding='utf-8')
    print(logs)
    # Function invoked at end of each epoch. Prints generated text.
    print("-------------- EPOCH --------- %d --------------- loss: %f" % (epoch, logs.get('loss')), file=log)

    start_index = random.randint(0, len(text) - maxlen - 1)
    for diversity in [0.1, 0.2, 0.5, 1.0, 1.2, 1.5]:
        print('----- diversity:', diversity, file=log)

        sentence = text[start_index: start_index + maxlen]
        generated = ""
        print("****************************************************", file=log)
        for i in range(1000):
            x_pred = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, char_indices[char]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char

        print(generated, file=log)
        print("----------------------------------------------------\n", file=log)
    print("***************************************************\n\n\n", file=log)
    log.close()


if os.path.exists(file_time):
    os.remove(file_time)
with open(file_time, "w") as f:
    def p(s):
        print(s, file=f)
    model.summary(print_fn=p)


print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

history_callback = model.fit(x, y,
          batch_size=128,
          epochs=100,
          callbacks=[print_callback])


weights_time = "weights/" + t[:t.index('.')] + ".h5"
weights_time = weights_time.replace(':', '_')

model.save(weights_time)





