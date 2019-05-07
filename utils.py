#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata
import json
import os
import codecs
import unicodedata
import string


def save_all_data():
    all_data = {}
    dir_list = [unicodedata.normalize('NFC', f) for f in os.listdir(u'./data/')]

    i = 0
    for topic in dir_list:
        j = open("./data/" + topic + "/" + topic + ".json", "rb")
        data = json.load(j)
        for d in data:
            all_data[i] = data[d]
            i += 1
            print(topic, i)
        # if i > 5:
        #     break
    data = codecs.open("all_data.json", 'w', encoding='utf-8')
    data.write(json.dumps(all_data, ensure_ascii=False))
    data.close()


def load_doc(filename):
    file = open(filename, 'rb')
    text = file.read().decode()
    file.close()
    return text


def clean_doc(doc):
    doc = doc.replace('--', ' ')
    tokens = doc.split()
    table = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word.lower() for word in tokens]
    return tokens


def create_sequences(tokens):
    length = 50 + 1
    sequences = list()
    for i in range(length, len(tokens)):
        seq = tokens[i-length:i]
        line = ' '.join(seq)
        sequences.append(line)
    return sequences


def save_doc(lines, filename):
    data = '\n'.join(lines)
    file = codecs.open(filename, 'w', encoding='utf-8')
    file.write(data)
    file.close()


def split_data(data, split_ratio):
    ln = len(data)
    splitted_data = []
    for i in range(0, ln//split_ratio):
        splitted_data.append(data[i])

    return splitted_data


def combine_txt(txt1, txt2, combined):
    txt_file1 = load_doc(txt1)
    txt_file2 = load_doc(txt2)
    combined = codecs.open(combined, 'w', encoding='utf-8')

    combined.write(txt_file1+txt_file2)
    combined.close()


def json_to_txt(path, out_path):
    txt_file = codecs.open(out_path, 'w', encoding='utf-8')
    with open(path, "rb") as json_file:
        x = json.load(json_file)
        for i in x:
            poem = x[i]['poem']
            a = []
            for k in poem.split("\n"):
                a.append(k.strip())

            txt_file.write("\n".join(a) + "\n\n")
    txt_file.close()


def load_json(path):
    j = open(path, "rb")
    x = json.load(j)
    j.close()
    return x

"""
data = load_doc("all_data.txt").split('\n')

splitted_data = split_data(data, 4)
save_doc(splitted_data, "quarter_data.txt")

splitted_data = split_data(data, 2)
save_doc(splitted_data, "half_data.txt")

splitted_data = split_data(data, 10)
save_doc(splitted_data, "a_tenth_data.txt")
"""

# data = load_doc("combined_ask_mutluluk.txt")
# d = clean_doc(data)
# save_doc(d, "cleaned_combined_ask_mutluluk.txt")
# 
# def a(js):
#     js = js.split('\n')
#     for i in js:
#         if len(i.split()) > 15:
#             return True
#     return False
#
# j = load_json("data/Aşk/Aşk.json")
#
# k = []
# for i in j:
#     p = j[i]['poem']
#     if a(p):
#         k.append(p)
#
#
#
# # json_to_txt("data/Mutluluk/Mutluluk.json", "data/Mutluluk/Mutluluk.txt")
# combine_txt("data/Mutluluk/Mutluluk.txt", "data/Mutluluk/Mutluluk.txt", "clean_combined_mutluluk_ask.txt")
#


