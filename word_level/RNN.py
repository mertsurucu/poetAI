from __future__ import print_function
import time
from collections import Counter, defaultdict
import random
import math
import sys
import dynet as dy
import numpy as np
import json

start = time.time()
w2i = defaultdict(lambda: len(w2i))


def read_json(fname):
    with open(fname) as json_file:
        data = json.load(json_file)
        for datum in data:
            poem = datum["poem"].replace("\n", "\n ")
            sent = [w2i[x] for x in poem.strip().split()]
            sent.append(w2i["<s>"])
            yield sent


data = list(read_json("../data/unim_poem.json"))
train = data[:65284]
nwords = len(w2i)
test = data[65285:]

S = w2i["<s>"]
assert (nwords == len(w2i))

# DyNet Starts
model = dy.ParameterCollection()
trainer = dy.AdamTrainer(model)

# Lookup parameters for word embeddings
EMBED_SIZE = 64
HIDDEN_SIZE = 128
WORDS_LOOKUP = model.add_lookup_parameters((nwords, EMBED_SIZE))

# Word-level LSTM (layers=1, input=64, output=128, model)
RNN = dy.LSTMBuilder(1, EMBED_SIZE, HIDDEN_SIZE, model)

# Softmax weights/biases on top of LSTM outputs
W_exp = model.add_parameters((nwords, HIDDEN_SIZE))
b_exp = model.add_parameters(nwords)


# Build the language model graph
def calc_lm_loss(sent):
    dy.renew_cg()
    # parameters -> expressions

    # initialize the RNN
    f_init = RNN.initial_state()

    # get the wids and masks for each step
    tot_words = len(sent)

    # start the rnn by inputting "<s>"
    s = f_init.add_input(WORDS_LOOKUP[S])

    # feed word vectors into the RNN and predict the next word
    losses = []
    for wid in sent:
        # calculate the softmax and loss
        score = W_exp * s.output() + b_exp
        loss = dy.pickneglogsoftmax(score, wid)
        losses.append(loss)
        # update the state of the RNN
        wemb = WORDS_LOOKUP[wid]
        s = s.add_input(wemb)

    return dy.esum(losses), tot_words


def sample(first=1, nchars=0, stop=-1):
    res = [first]
    dy.renew_cg()
    state = RNN.initial_state()

    cw = first
    while True:
        x_t = WORDS_LOOKUP[cw]
        state = state.add_input(x_t)
        y_t = state.output()
        r_t = b_exp + (W_exp * y_t)
        ydist = dy.softmax(r_t)
        dist = ydist.vec_value()
        rnd = random.random()
        for i, p in enumerate(dist):
            rnd -= p
            if rnd <= 0: break
        res.append(i)
        cw = i
        if cw == stop: break
        if nchars and len(res) > nchars: break
    return res


# Sort training sentences in descending order and count minibatches
train_order = list(range(len(train)))

print("startup time: %r" % (time.time() - start))
# Perform training
start = time.time()
i = all_time = dev_time = all_tagged = this_words = this_loss = 0
for ITER in range(1000):
    random.shuffle(train_order)
    for sid in train_order:
        i += 1
        if i % int(500) == 0:
            trainer.status()
            print(this_loss / this_words, file=sys.stderr)
            all_tagged += this_words
            this_loss = this_words = 0
            all_time = time.time() - start
        if i % int(10000) == 0:
            dev_start = time.time()
            dev_loss = dev_words = 0
            for sent in test:
                loss_exp, mb_words = calc_lm_loss(sent)
                dev_loss += loss_exp.scalar_value()
                dev_words += mb_words
            dev_time += time.time() - dev_start
            train_time = time.time() - start - dev_time
            print("nll=%.4f, ppl=%.4f, words=%r, time=%.4f, word_per_sec=%.4f" % (
                dev_loss / dev_words, math.exp(dev_loss / dev_words), dev_words, train_time, all_tagged / train_time))
        # train on the minibatch
        loss_exp, mb_words = calc_lm_loss(train[sid])
        this_loss += loss_exp.scalar_value()
        this_words += mb_words
        loss_exp.backward()
        trainer.update()
    print("epoch %r finished" % ITER)
trainer.update_epoch(1.0)

samplesentence = sample(first=w2i["<s>"], stop=w2i["\n"])

print(samplesentence)
