# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 18:22:05 2018

@author: KALKAN
"""

import mynltk
import random
import math
import time
import pickle


class Ngram:
    
    def __init__(self, N=1):
        self.N = N
        self.freq = dict()
        self.name = str(N) + "-gram"
        
        self.smoothed = 0  # holds whether model is smoothed or not
        self.V = 0  # number of vocabulary size in (N-1)gram. 0 in the beginning
        self._smoothed_dict = dict()  # (N-1)gram dictionary for smoothing

    
    def train_all(self, sentences):
        """
            trains all sentences given.
            sentences: a list of all sentences to be trained.
        """
        start = time.time()
        print(self.name + " training start..")

        for sentence in sentences:
            self.train_a_sentence(sentence)

        print("%s training end in %.2f sn" % (self.name, time.time()-start))
        print("---------------------\n")
    

    def train_a_sentence(self, sentence):
        """
            trains a sentece. splits words
            and adds all to the dictionary by increasing frequencies.
        """
        tokens = mynltk.process_sentence(sentence)
        tokens = self._post_process(tokens) #adds <s> and </s>
        
        for i in range(len(tokens)-(self.N-1)):
            # 'pre' refers to (N-1) word before last word.
            pre = tuple(tokens[i:i+self.N-1])  # (N-1)word before last word.
                                               # e.g for 3gram. "natural language processing"
                                               # pre = ('natural', 'language')
                                               # last = 'processing'
            last = tokens[i + self.N-1]
            self._add_dict(pre, last)  # adds to the dictionary.
            
            if self.N!=1 and self.N!=2: # this is for smoothing
                pre = tuple(tokens[i:i+self.N-2])
                self._smoothed_dict[pre] = 1

    def _add_dict(self, pre, last):
        """
            for example: 
                pre = ("I","am")
                last = "good"
                adds frequency of "I am good"
                freq = {
                ...
                ("I", "am"):[{..., "good":44->45, ... }, 123->124]
                ...
                }
        """

        if pre in self.freq: # if 'pre' is in dict
            if last in self.freq[pre][0]: # if 'pre' is in dict and 'last' is after 'pre'
                self.freq[pre][0][last] += 1
            else: # if 'pre' is in dict but 'last' is not after 'pre'
                self.freq[pre][0][last] = 1            
        else: # if 'pre' is not in dict as key, initialize
            self.freq[pre] = [{}, 0]
            self.freq[pre][0][last] = 1
            
        self.freq[pre][1] += 1 # total counts of 'pre' is increased by 1.          


    def generate_txt(self, max_sentence=4):
        all_sentences = ""
        for i in range(max_sentence):
            sentence = self.generate_sentence(max_word=30)
            all_sentences += sentence + " "
        return all_sentences


    def generate_sentence(self, max_word=30):
        
        words = ["<s>" for _ in range(self.N-1)]  # adds '<s>' up to number of (N-1) 
                                                  # to the beginning
        
        count_word = 0  # holds number of words generated
        
        while True:
            t = random.random()  # threshold value generated random between [0, 1] 
            total_prob = 0
            
            pre = tuple(words[(-self.N+1):]) if self.N>=2 else tuple()
            
            if len(pre)>=1 and pre[-1] == "</s>": # len(pre)>=1 is necessary for unigram.
                break                             # because pre[-1] doesn't exist in unigram in the beginning.
            
            for last in self.freq[pre][0]:
                
                prob = self._probability(pre, last)  # e.g C(I,want,go)/C(I,want)
                                                     # pre: ('I', 'want')
                                                     # last: ('go',)
                total_prob += prob
                    
                if total_prob>=t:
                    words.append(last)
                    count_word+=1
                    break

            if count_word>=max_word:
                break
        
        sentence = " ".join([w for w in words if w!="<s>" and w!="</s>" ])
        
        return mynltk.edit_punc(sentence)

    def _probability(self, pre, last):
        
        
        pre_count = self.freq[pre][1] if pre in self.freq else 0  # e.g C(I, want)
        pre_last_count = self.freq[pre][0][last] if pre in self.freq and last in self.freq[pre][0] else 0 # C('I')
        prob = (pre_last_count + self.smoothed)/(pre_count + self.V)         
            
        return prob
    
    def prob_txt(self, txt, smooth=1):
        """
            adds all log prob of sentences
        """
        sentences = mynltk.get_sentences(txt)

        total_prob=1
        for i in sentences:
            total_prob += self.prob_a_sentence(i)
        
        return total_prob

    def prob_a_sentence(self, sentence):
        tokens = mynltk.process_sentence(sentence)  # clears and edit the sentence

        #tokens = self._post_process(tokens)  # adds special characters.

        prob = 0
        for i in range(len(tokens)-(self.N-1)):
            pre = tuple(tokens[i:i+self.N-1])
            last = tokens[i+self.N-1]
            
            pro = self._probability(pre, last)

            prob += math.log2(pro)

        return prob

    def perplexity(self, txt):
        """
            calculates perplexity of a text
        """
        perp = 0
        sentences = mynltk.get_sentences(txt)
        
        for i in sentences:            
            perp += self._perplexity(i)
            
        return perp

    def _perplexity(self, sentence):
        """
            calculates perplexity of a sentence
        """
        tokens = mynltk.process_sentence(sentence)
        n = len(tokens)
        prob = self.prob_a_sentence(sentence)
        if(n==0):
            return 1
        return pow(2, float(-1/n)*prob)

    def make_smoothed(self):
        start = time.time()
        print(self.name + " smoothing start..")

        for key in self.freq:
            for val in self.freq[key][0]:
                self.freq[key][0][val] += 1
                self.freq[key][1] += 1
        
        if self.N==1:
            self.V = len(self.freq[()][0])
        elif self.N==2:
            self.V = len(self.freq)
        else:
            self.V = len(self._smoothed_dict)
        self.smoothed = 1
        
        print("%s smoothing end in %.2f sn" % (self.name, time.time()-start))
        print("---------------------\n")
        self.name += "_smoothed"

    def _post_process(self, tokens):
        """
            adds "<s>" and "</s>" to the beginning and end
        """
        tokens.append("</s>")
        pre = ["<s>" for _ in range(self.N-1)]
        pre.extend(tokens)
        return pre
    
    def save_model(self, path):
        with open(path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load_model(path):
        file = open(path, "rb")
        model = pickle.load(file)
        file.close()
        return model
#
#
# import utils
# text_path = "../clean_combined_mutluluk_ask.txt"
# txt = utils.load_doc(text_path)
# trigram = Ngram(3)
# trigram.train_all(txt.split('\n'))
# trigram.make_smoothed()
# trigram.save_model("trigram_model.pickle")
#
