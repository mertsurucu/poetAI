import time
import re
import json
import os
from turkishnlp import detector
start = time.time()
obj = detector.TurkishNLP()
obj.download()
obj.create_word_set()


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
            if len(poem) < 30:
                continue
            if not obj.is_turkish(poem):
                continue

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
            for line in poem.split('\n'):
                line = line.lstrip()
                # replace ........ to ...
                line = re.sub(r'\.{3,}', "...", line)
                # line = re.sub('...br', "", line)
                # line = re.sub(r'\bbr\b', "", line)
                line = re.sub(r'\.\.\.br(.)*', "", line)

                # ... sonra yeni satira geç?
                if len(line) > 75:
                    continue
                # deletes the punctuations
                line = re.sub(r'[#$%&*+''/:;•<=>@[\\]^_`{|()}~\']', '', line)
                words = line.lower().split(' ')
                # if len(words) < 2:
                #     continue
                # deletes the names
                if len(words) == 2 or len(words) == 3:
                    for k in words:
                        if k in isim or k in soyisimler:
                            continue

                # deletes the dates
                if is_match(r'(\d+[/.\\]\d+[/.\\]\d+)', line):
                    continue
                # if there is a date or whatever with ex: 12.
                # if is_match(r'(\d+[/.\\])', line):
                #     add_line = False
                if is_match(r'(\d+[^a-zA-Z0-9\s\p{P}ıöüşğ\'])', line):
                    continue
                if is_match(r'(^[\d| ]*$)', line):
                    continue
                if len(line) < 3:
                    continue
                if is_match(r'(hotmail|gmail|outlook|com)', line):
                    continue

                new_poem += line + '\n'
            new_poem = new_poem.rstrip()
            new_poem += '<s>'
            if len(new_poem) > 45:
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
