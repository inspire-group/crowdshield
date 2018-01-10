from nltk import TweetTokenizer


class Preprocessor(object):

	def __init__(self, data):
		this.data = data
		self.tokenizer = TweetTokenizer()

	def tokenize(self):
		pass

	# See here:
	# https://ahmedbesbes.com/sentiment-analysis-on-twitter-using-word2vec-and-keras.html
	def tokenize_ahmed(self, tweet):
	    try:
	        tweet = unicode(tweet.decode('utf-8').lower())
	        tokens = tokenizer.tokenize(tweet)
	        tokens = filter(lambda t: not t.startswith('@'), tokens)
	        tokens = filter(lambda t: not t.startswith('#'), tokens)
	        tokens = filter(lambda t: not t.startswith('http'), tokens)
	        return tokens
	    except:
	        return 'NC'

def main():
	pass

if __name__ == '__main__':
	main()
