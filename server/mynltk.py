# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 20:17:20 2018

@author: KALKAN
"""
punc = ["\"","$","%","\\","'","(",")","*","+",".","/",":",";","<","=",">","?",","]

def process_sentence(sentence):
    sentence = sentence.lower()
    sentence = seperate_punc(sentence)
    sentence = word_tokenize(sentence)
    s = [i for i in sentence if i!=""]
    return s


def word_tokenize(sentence):
    tokens = sentence.split(" ")
    for i in range(len(tokens)):
        tokens[i] = tokens[i].strip()
    return tokens


def seperate_punc(sentence):
    for i in punc:
        sentence = sentence.replace(i, " " + i + " ")
    sentence = sentence.replace(".", "")
    sentence = sentence.replace("\n", " ")
    sentence = sentence.replace("\r\n", " ")
    return sentence


def edit_punc(sentence):
    for i in punc:
        sentence = sentence.replace(" " + i, i)
    sentence += "."
    return sentence.capitalize()


def get_index_of(substr, txt):
    """
        returns index of end of substr
        for example txt="abcdefg", substr ="cde" returns 4 - index of 'e'
    """
    length = len(substr)
    for i in range(len(txt)):
        if substr==txt[i:i+length]:
            return i+length-1
    return None

def get_sentences(txt):
    """
        returns the sentences in a text (an email for this assignment)
    """
    sentences = []
    
    def get_sentence(txt):
        idx = getDotIndex(txt, ".?!")
        

        if txt=="":
            return
        if idx==None: # email is over
            sentences.append(txt.strip())
            return
        
        sent = txt[:idx].strip()
        sentences.append(sent)
        get_sentence(txt[idx+1:])
    
    get_sentence(txt)
    return sentences


def getDotIndex(string, delimiters):
    """ finds index of end of a sentence
    """
    for i in range(len(string)):
        if string[i] in delimiters:
            return i
    return None







