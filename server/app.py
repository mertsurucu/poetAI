import numpy as np
from server import utils
import time
import pickle
import requests


from keras.models import load_model

import random


from flask import Flask, jsonify
from flask_restful import Api

from flask import request
import tensorflow as tf
from model import Model

spell_checker_server = "http://localhost:8080/"


def get_ngram_model(path):
    file = open(path, "rb")
    t = pickle.load(file)
    file.close()
    return t


def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def generate_akrostis_poem(name):
    pass


def generate_poem(diversity, range_, n_line, th=200, model=None):
    sentences = _generate_sentences(diversity=diversity, range_=range_, model=model)
    return  "<br>".join(sentences)
    if is_spell_working():  # if spell server working
        sentences = correct_sentences(sentences)

    perp_sent_pair_norm = _calculate_perplexity(sentences, model)

    indices = np.arange(len(perp_sent_pair_norm))
    np.random.shuffle(indices)
    poem = ""
    c = 0
    for i in indices:
        if perp_sent_pair_norm[i][0] < th:
            poem += perp_sent_pair_norm[i][1].capitalize() + '\n'
            c += 1
        if c % 4 == 0:
            poem += '\n'
        if c >= n_line:
            break
    poem = poem.replace('\n', "<br>")
    return poem


def _calculate_perplexity(sentences, model):

    perp_sent_pair_norm = []
    for s in sentences:
        if len(s.split()) >= 3:
            perp_sent_pair_norm.append((model.trigram_model.perplexity(s) / len(s.split()), s))
        # print(lm.perplexity(s), ":", s)

    perp_sent_pair_norm = sorted(perp_sent_pair_norm)

    return perp_sent_pair_norm


def _generate_sentences(diversity=0.5, range_=500, model=None):
    global graph
    with graph.as_default():
        start_index = random.randint(0, len(model.text) - maxlen - 1)
        sentence = model.text[start_index: start_index + maxlen]
        generated = ""
        for i in range(range_):
            x_pred = np.zeros((1, maxlen, len(model.chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, model.char_indices[char]] = 1.

            preds = model.keras_model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = model.indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char
        sentences = [s.capitalize() for s in generated.split('\n')[1:]]
        return sentences


def generate_acrostic(name, diversity=0.5, model=None):
    global graph
    with graph.as_default():
        start_index = random.randint(0, len(model.text) - maxlen - 1)
        sentence = model.text[start_index: start_index + maxlen]
        generated = ""
        name += "\n"
        for letter in name:
            while True:
                x_pred = np.zeros((1, maxlen, len(model.chars)))
                for t, char in enumerate(sentence):
                    x_pred[0, t, model.char_indices[char]] = 1.

                preds = model.keras_model.predict(x_pred, verbose=0)[0]
                next_index = sample(preds, diversity)
                next_char = model.indices_char[next_index]
                generated += next_char
                if next_char == '\n':
                    sentence = sentence[2:] + next_char + letter
                    generated += letter
                    break
                sentence = sentence[1:] + next_char
        sentences = [s.capitalize() for s in generated.split('\n')[1:]]
        return "<br>".join(sentences)


def load_category_model(text_path, network_path, trigram_path):
    text = utils.load_doc(text_path)
    trigram = get_ngram_model(trigram_path)
    keras_model = load_model(network_path)
    chars = sorted(list(set(text)))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))
    model = Model(text, trigram, keras_model, chars, char_indices, indices_char)
    return model


def load_models():
    global graph
    with graph.as_default():
        print("Models loading..")
        s = time.time()
        text1 = "./clean_poems/category_1.txt"
        text2 = "./clean_poems/category_2.txt"
        text3 = "./clean_poems/category_3.txt"

        category_1_model_path = "./models/category_1/2019-05-20 16_43_17_category_1.txt_tr_20.h5"
        category_2_model_path = "./models/category_2/2019-05-13 18_05_13.h5"
        category_3_model_path = "./models/category_3/2019-05-11 01_58_50.hdf"

        cat1_trigram_path = "./models/category_1/category_1_trigram_model.pkl"
        cat2_trigram_path = "./models/category_2/category_2_trigram_model.pkl"
        cat3_trigram_path = "./models/category_3/category_3_trigram_model.pkl"

        cat1_model = load_category_model(text1, category_1_model_path, cat1_trigram_path)
        cat2_model = load_category_model(text2, category_2_model_path, cat2_trigram_path)
        cat3_model = load_category_model(text3, category_3_model_path, cat3_trigram_path)
        print("Models loaded in", time.time()-s)
        return cat1_model, cat2_model, cat3_model


app = Flask(__name__)
api = Api(app)

maxLen = None

models = {1: None, 2: None, 3: None}

graph = tf.get_default_graph()  # required since flask runs threads


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


def is_spell_working():
    try:
        requests.post(spell_checker_server, json={'value': ""})
    except:
        return False
    return True


def correct_sentences(sentences):
    corrected = []
    for s in sentences:
        corrected.append(correct_sentence(s))
    return corrected


def correct_sentence(sentence):
    dictToSend = {'value': sentence}
    res = requests.post(spell_checker_server, json=dictToSend)
    return res.text


@app.route('/', methods=['POST', 'GET'])
def get():
    print("****************")

    model_idx = int(request.args['category'])
    model = models[model_idx]
    type = request.args['type']
    if type == "Akrostic":
        poem = generate_acrostic(name=request.args['name'], diversity=0.5, model=model)
    else:
        poem = generate_poem(diversity=0.5, range_=500, n_line=12, model=model)
    print(poem)
    response = jsonify(poem=poem)
    return response


if __name__ == '__main__':
    maxlen = 20
    cat1_model, cat2_model, cat3_model = load_models()
    models[1] = cat1_model
    models[2] = cat2_model
    models[3] = cat3_model
    app.run(host='0.0.0.0', debug=True)

