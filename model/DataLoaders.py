import sqlite3

import sys
DATA_PATH = '../data'
sys.path.append(DATA_PATH)
from DataUtils import DataUtils
from DataObjects import UserTrendTweetLabel


def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)


class DataLoader(object):

	def __init__(self, usertrend_id=None):
		DB_NAME = "sqlite:///../data/db.sqlite"
		self.du = DataUtils(DB_NAME)
		#self.utid = usertrend_id

	def get_sample_tweets_from_usertrendid(usertrend_id, sample_size=1000):
		tweet_ids = du.get_sample_tweet_ids(usertrend_id, sample_size)
		tweets = self.du.get_tweets_from_tweetids(tweet_ids)
		return tweets


	def label_generator(self, usertrend_id, sample_size=1000, limit=150):

		du = self.du
		du.start_session()

		if du.has_usertrend_for_uttl(usertrend_id):
			print "{} already has tweet labels".format(usertrend_id)
			return

		usertrend = du.get_usertrend(usertrend_id)
		user_id = usertrend.user_id
 		user = du.get_user(user_id)
		bio = user.bio
		headlines = usertrend.related_queries

		#user_id = remove_non_ascii(user_id)
		#bio = remove_non_ascii(bio)
		#headlines = remove_non_ascii(headlines)

		label_question = 'Would the following tweets offend to the mentioned user: {}\n\n \
						  For context, here is the user\'s bio:\n\n \
						  {}\n\n \
						  Here are the headlines surrounding the user during the time of the tweet:\n \
						  {}\n\n'.decode(sys.stdin.encoding).format(user_id, bio, headlines)

		print label_question

		tweet_ids = du.get_sample_tweet_ids(usertrend_id, sample_size)

		if len(tweet_ids) == 0:
			print "{} has less than 1000 tweets".format(usertrend_id)
			return

		tweets = du.get_tweets_from_tweetids(tweet_ids)
		tweet_iter = iter(tweets)

		label_map = {'y': 1, 'n': 0, 'u': 2}
		tweet_labels = []
		while(len(tweet_labels) < limit and tweet_iter):
			tweet = tweet_iter.next()
			text = tweet.text
			text = remove_non_ascii(text)
			resp = raw_input(text + '\n')
			print
			while resp not in label_map:
				print "Please enter 'y': yes, 'n': no, 'u': unsure"
				resp = raw_input(text + '\n')
				print
			label = label_map[resp]
			if label == 0 or label == 1:
				tweet_label = UserTrendTweetLabel(usertrend_id=usertrend_id, tweet_id=tweet.id, text=tweet.text, label=label)
				tweet_labels.append(label)
			print len(tweet_labels)

		du.add_usertrendtweetlabels(tweet_labels)
		du.close_session()


	def load_data(self, usertrend_id):
		du = self.du
		du.start_session()
		utid = self.utid
		tweet_texts = []
		try:
			tweet_texts = du.get_tweet_texts_from_usertrendid(utid)
		finally:
			du.close_session()
		return tweet_texts

def main(args):
	utid = 'BetsyDeVos-201611'
	dl = DataLoader()
	dl.label_generator(utid)
	#tweets = dl.load_data()

if __name__ == '__main__':
	main(sys.argv)
