#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata
import json
import os
import codecs
import unicodedata


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






