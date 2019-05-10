from __future__ import print_function

import gc
import time
import string
import re
import json
import os


# writes into json file
def to_json(_poems):
    poem_dic = {}
    for _, _poem in enumerate(_poems):
        poem_dic[_] = _poem
    with open('clean_poems/' + topic + '.json', 'w', encoding="utf-8") as f_js:
        json.dump(poem_dic, f_js, sort_keys=True, indent=4, ensure_ascii=False)


# if there is match with the regex
def is_match(regex, text):
    pattern = re.compile(regex)
    return pattern.search(text) is not None


def clean(file_path):
    with open(file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
        poems = []
        for datum in data:
            poem = str(data[datum]['poem'])
            new_poem = ''
            # replace more than 2 \n to 2 n
            poem = re.sub(r'\n{3,}', '\n\n', poem)
            # removes unnecessary indents
            _list = poem.split('\n\n')
            poem = ''
            for i in _list:
                if len(re.findall('\n', i)) == 0 and i != '':
                    poem += i
                    poem += '\n'
                elif len(re.findall('\n', i)) > 0:
                    poem += '\n'
                    poem += i
                    poem += '\n'
            poem = poem.rstrip()
            poem = poem.lstrip()
            # checks each line
            for i in poem.split('\n'):
                add_line = True
                i = i.lstrip()
                # replace ........ to ...
                i = re.sub(r'\.{3,}', "...", i)
                # i = re.sub('...br', "", i)
                # i = re.sub(r'\bbr\b', "", i)
                i = re.sub(r'\.\.\.br(.)*', "", i)

                # ... sonra yeni satira geç?
                if len(i) > 75:
                    add_line = False
                # deletes the punctuations
                i = re.sub(r'[#$%&*+''/:;<=>@[\\]^_`{|()}~\']', '', i)
                words = i.lower().split(' ')
                if len(words) < 2:
                    add_line = False
                # deletes the names
                if len(words) == 2 or len(words) == 3:
                    for k in words:
                        if k in isim or k in soyisimler:
                            add_line = False

                # deletes the dates
                if is_match(r'(\d+[/.\\]\d+[/.\\]\d+)', i):
                    add_line = False
                # if there is a date or whatever with ex: 12.
                if is_match(r'(\d+[/.\\])', i):
                    add_line = False
                if add_line:
                    new_poem += i + '\n'
            new_poem = new_poem.rstrip()
            new_poem += '<s>'
            if len(new_poem) > 10:
                poems.append(new_poem)


    to_json(poems)


if __name__ == '__main__':
    f = open('isimler.txt', 'r', encoding='utf-8')
    isim = f.read()
    isim = isim.split('\n')
    f = open('soyisimler.txt', 'r', encoding='utf-8')
    soyisimler = f.read()
    soyisimler = soyisimler.split('\n')

    for i in os.listdir(u'./data/'):
        topic = i
        start = time.time()
        clean('data/' + topic + '/' + topic + '.json')
        print('finished in %r' % (time.time() - start))
