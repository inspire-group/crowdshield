from DataLoaders import DataLoader
from Preprocessors import Preprocessor
from FeatureExtractors import FeatureExtractor

import sys
DATA_PATH = '../lib/data'
sys.path.append(DATA_PATH)
import DataUtils

from gensim.models import Word2Vec
import numpy as np


def old():
	utid = 'BetsyDeVos-201611'
	dl = DataLoader()
	tweets = dl.load_data(utid)

def main():
	glove_path = 'glove.twitter.27B/glove.twitter.27B.25d.txt'
	with open(glove_path, 'rb') as lines:
		w2v = {line.split()[0]: np.array(map(float, line.split()[1:]))
				for line in lines}
	print w2v

if __name__ == '__main__':
	main()
