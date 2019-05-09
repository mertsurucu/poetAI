from __future__ import print_function

import gc
import time
import string
import re
import json

start = time.time()
file_path = "data/Aşk/Aşk.json"
remove_punc = '"#$%&\'()*+''/:;<=>@[\\]^_`{|}~'
f = open("isimler.txt", "r", encoding='utf-8')
isim = f.read()
isim = isim.split('\n')
f = open("soyisimler.txt", "r", encoding='utf-8')
soyisimler = f.read()
soyisimler = soyisimler.split('\n')


def is_match(regex, text):
    pattern = re.compile(regex)
    return pattern.search(text) is not None


with open(file_path, encoding='utf-8') as json_file:
    data = json.load(json_file)
    poems = []
    for datum in data:
        add_line = True
        poem = str(data[datum]["poem"])
        new_poem = ''
        for i in poem.split("\n"):
            if len(i) > 70:
                break
            # deletes the punctuations
            i = re.sub(r'[#$%&*+''/:;<=>@[\\]^_`{|()}~\']', '', i)
            words = i.lower().split(' ')
            if len(words) == 2 or len(words) == 3:
                for k in words:
                    if k in isim or k in soyisimler:
                        add_line = False

            # deletes the dates
            if is_match(r'(\d+[/.\\]\d+[/.\\]\d+)', i):
                add_line = False
            # if there is no problem to add it
            if add_line:
                new_poem += i + '\n'

        new_poem += "<s>"
        poems.append(new_poem)

print("finished in %r" % (time.time() - start))
