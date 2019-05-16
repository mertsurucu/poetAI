import utils

# from ngram_builder.ngram import Ngram
# import ngram_builder
from ngram import Ngram


def train(text_path, out_path):
    txt = utils.load_doc(text_path)
    trigram = Ngram(2)
    trigram.train_all(txt.split('\n'))
    trigram.make_smoothed()
    trigram.save_model(out_path)


path = "./clean_poems/category_3.txt"
out_path = "./models/category_3/category_3_bigram_model.pkl"
train(path, out_path)

# lm = Ngram.load_model("trigram_model.pickle")
# a = lm.perplexity("Birkaç damla sevinç gözyaşı,")













