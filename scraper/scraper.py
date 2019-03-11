#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import get
# from bs4 import BeautifulSoup
import time
import re
import urllib
import json
import os

global_id = 0
global_poems = {}





def get_poems_in_a_topic_page(topic, topic_poems_dict, raw_html):
    global global_id
    urls = get_links_in_topic_page(raw_html)
    poems = []
    i = 0
    for u in urls:
        poem, strr = get_poem_in_devamini_oku(topic, main_url + u)
        topic_poems_dict[global_id] = poem
        global_id += 1
        # poems.append(poem)
        # f = open(str(i)+".txt", "w+")
        # f.write(strr)
        # f.close()
        i += 1
        print(i)
    # return poems


def get_poem_in_devamini_oku(topic, url):
    raw_html = urllib.urlopen(url).read()
    poem = get_poem(raw_html)
    author = get_author(raw_html)
    title = get_title(raw_html)

    str = '{"topic": "' + topic + '","author": "' + author + '","title": "'+title+'","poem": "' + poem + '"}'
    # return str
    poem_dict = {'topic': topic,
                 'author': author,
                 'title': title,
                 'poem': poem}
    return poem_dict, str


def get_poem(raw_html):
    poem_ptrn = '"pd-text">.*?(?s).*?</div>'
    res = re.search(poem_ptrn, raw_html, re.UNICODE).group()
    kitalar = re.findall('<p>.*?(?s).*?</p>', res)
    poem = ""
    for kita in kitalar:
        kita = kita.replace('<br/>', '')
        kita = kita.replace('<p>', '')
        kita = kita.replace('</p>', '')
        kita = kita.strip()
        kita += '\n\n'
        poem += kita
    return poem.strip()


def get_author(raw_html):
    poem_ptrn = '"pb-title">(.*?(?s).*?).*?(?s).*?<h2>(.*?)</h2>.*?(?s).*?</div>'
    author = re.search(poem_ptrn, raw_html).group(2)
    return author


def get_title(raw_html):
    poem_ptrn = '"pd-title-a">(.*?(?s).*?).*?(?s).*?<h3>(.*?)</h3>.*?(?s).*?</div>'
    title = re.search(poem_ptrn, raw_html).group(2)
    return title


def get_links_in_topic_page(raw_html):
    urls = []
    ptrn = '"more-button btn" href=".*?"'
    rgx = re.compile(ptrn)
    x = rgx.findall(raw_html)
    ptrn_href = 'href="'
    for str in x[:-1]:
        a = re.search(ptrn_href, str)
        urls.append(str[a.span()[1]:-1])

    return urls


def get_topic_name_url_pair(url='https://www.antoloji.com/siir/konulari/'):
    raw_html = urllib.urlopen(topic_list_url).read()
    poem_ptrn = '<div class="subject-list-full box populer">(.*?(?s).*?)</ul>.*?(?s).*?</div>'
    title = re.search(poem_ptrn, raw_html)
    lst = re.findall('<li>.*?(?s).*?</li>', title.group(1))
    pair = []
    for i in lst:
        url = re.search('href="(.*?)">', i).group(1)
        topic_name = re.search('</i>(.*?)</a>', i).group(1)
        pair.append((topic_name, url))
    return pair


def get_poems_by_topic(pair):
    topic_name, topic_url = pair
    print("1----", topic_name)
    raw_html = urllib.urlopen(main_url + topic_url).read()
    poems = []
    i = 0
    all_topic_time = time.time()
    topic_poems_dict = {}
    while True:
        s = time.time()
        # poems.append(get_poems_in_a_topic_page(topic_name, raw_html))
        get_poems_in_a_topic_page(topic_name, topic_poems_dict, raw_html)
        if i>1:
            break
        if not has_next_page(raw_html):
            break
        raw_html = get_next_page(raw_html)
        i += 1
        print("*page:", str(i), str(time.time()-s))
    print("All topic time:", str(time.time()-all_topic_time))
    save_poems(topic_name, topic_poems_dict)


def get_all_poems():
    pairs = get_topic_name_url_pair()

    for i in range(len(pairs)):
        get_poems_by_topic(pairs[i])


def save_poems(topic_name, poems):
    if not os.path.exists("../data/" + topic_name):
        os.mkdir("../data/" + topic_name)
    poem_to_json(topic_name, poems)


def poem_to_json(topic_name, poems):
    data = open("../data/" + topic_name + '/' + topic_name + '.json', 'wb')
    json.dump(poems, data, ensure_ascii=False)
    data.close()


def has_next_page(raw_html):
    res = re.search('<li class="disabled PagedList-skipToNext">', raw_html)
    if res == None:
        return True
    return False


def get_next_page(raw_html):
    res = re.search('<li class="PagedList-skipToNext">(.*?(?s).*?)</li>', raw_html).group(1)
    url = re.search('href="(.*?)"', res)
    return urllib.urlopen(main_url + url.group(1)).read()


main_url = 'https://www.antoloji.com'
topic_list_url = 'https://www.antoloji.com/siir/konulari/'


get_all_poems()
