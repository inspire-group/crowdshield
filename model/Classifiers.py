from gensim.models import Word2Vec
from sklearn.linear_model import SGDClassifier

import sys
PREPROCESS_PATH = '../lib/twitter-preprocess'
sys.path.append(PREPROCESS_PATH)
from twitter-preprocess import tokenize


'''
import numpy as np

with open("glove.6B.50d.txt", "rb") as lines:
    w2v = {line.split()[0]: np.array(map(float, line.split()[1:]))
           for line in lines}

import gensim
# let X be a list of tokenized texts (i.e. list of lists of tokens)
model = gensim.models.Word2Vec(X, size=100)
w2v = dict(zip(model.wv.index2word, model.wv.syn0))
'''

def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)

class Classifier(object):
	def __init__(self):
		pass

	# From ELE397 classifier
	def load_train_data(self, file_path):
		reader = csv.reader(open(file_path,"rb"),delimiter=delimiter)
	    rows = []
	    for row in reader:
	        rows.append(row)
		labels  = array([int(x[0]) for x in rows])
		train  = [x[1] for x in rows]
		return labels, train

	def feature_extract(self, tweets):
		preproc_tweets = map(lambda t: tokenize(t), tweets)
		model = Word2Vec(preproc_tweets)
		word2vec = dict(zip(model.wv.index2word, model.wv.syn0))
		dim = len(word2vec.itervalues().next())
		mean_embeds = np.array([
				        np.mean([self.word2vec[w] for w in words if w in self.word2vec]
				                or [np.zeros(self.dim)], axis=0)
				        for words in tweets
				    ])

	def vectorize_data_point(self, data_point):
		words = data_point
		wvs = map(lambda w: word2vec[w] if w in word2vec, words)
		mean_embed = np.mean(wvs or np.zeros(self.dim), axis=0)

	def vectorize_data(self, data):
		mean_embeds = map(lambda x: self.vectorize_data_point(x), data)

	def classify(self):
		clf = SGDClassifier()
		for x, y in data:
			clf.partial_fit(x, y)

	def evaluate(self):
		pass


class MeanEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = len(word2vec.itervalues().next())

    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])


class TfidfEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.word2weight = None
        self.dim = len(word2vec.itervalues().next())

    def fit(self, X, y):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
                np.mean([self.word2vec[w] * self.word2weight[w]
                         for w in words if w in self.word2vec] or
                        [np.zeros(self.dim)], axis=0)
                for words in X
            ])

''''''''''''
''''''''''''

def main():
	pass

if __name__ == '__main__':
	main()
