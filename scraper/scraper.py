from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import re


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def get_poems_in_a_page(html):
    poems = []

    for box in html.find_all("div", attrs={"class": "category-poem box"}):
        url = box.find_all('a')[-1].get('href')
        print(main_url+url)
        get_poem_in_devamini_oku(main_url+url)


def get_poem_in_devamini_oku(url):
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')


main_url = 'https://www.antoloji.com'
raw_html = simple_get('https://www.antoloji.com/aci/siirleri/')

import time
s = time.time()
# html = BeautifulSoup(raw_html, 'html.parser')
# print(time.time()-s)
#
# s = time.time()

txt = raw_html.decode("utf-8")
ptrn = '"more-button btn" href=".*?">'
rgx = re.compile(ptrn)
x = rgx.findall(txt)
print(time.time()-s)
#
# get_poems_in_a_page(html)