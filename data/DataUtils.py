from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import exists

import unicodedata
#import csv
import unicodecsv as csv

import numpy as np
from numpy.random import choice

from DataObjects import Trend, User, UserTrend, Tweet, UserTrendTweet, UserTrendTweetLabel


class DataUtils(object):

	############################################################################
	# Setup Methods
	############################################################################

	def __init__(self, DB_NAME):
		#DB_NAME = "sqlite:///db.sqlite" # Add database to current directory if not present
		self.engine = create_engine(DB_NAME, echo=False)
		self.session = None

	def start_session(self):
		engine = self.engine
		Session = sessionmaker()
		Session.configure(bind=engine)
		self.session = Session()

	def close_session(self):
		self.session.close()

	############################################################################
	# Add Methods
	############################################################################

	def add_usertrendtweetlabels(self, usertrendtweetlabels):
		session = self.session
		for uttl in usertrendtweetlabels:
			q = session.query(UserTrendTweetLabel).\
					filter_by(usertrend_id=uttl.usertrend_id,
					 		  tweet_id=uttl.tweet_id)
			q_exists = session.query(q.exists()).scalar()
			if q_exists:
				continue
			session.add(uttl)
		session.commit()

	############################################################################
	# Get Methods
	############################################################################

	def get_trends(self):
		session = self.session
		trends = session.query(Trend).all()
		return trends

	def get_bio(self, user_id):
		session = self.session
		user = session.query(User).get(user_id)
		return user.bio

	def get_related_queries(self, user_id, trend_id):
		session = self.session
		usertrend = session.query(UserTrend).get((user_id, trend_id))
		return usertrend.related_queries

	def get_sample_tweet_ids(self, usertrend_id, sample_size):
		session = self.session
		usertrendtweets = session.query(UserTrendTweet).filter_by(usertrend_id=usertrend_id).all()
		if len(usertrendtweets) < sample_size:
			sample_tweets = []
		else:
			sample_tweets = choice(usertrendtweets, size=sample_size, replace=False)
		sample_tweet_ids = map(lambda u: u.tweet_id, sample_tweets)
		return sample_tweet_ids

	def get_num_tweets(self, usertrend_id):
		session = self.session
		num_tweets = session.query(UserTrendTweet).filter_by(usertrend_id=usertrend_id).count()
		return num_tweets

	def get_tweets_from_usertrendid(self, usertrend_id):
		session = self.session
		#ut = session.query(UserTrend).filter_by(usertrend_id=usertrend_id)
		#ut.usertrend_tweets
		uttwts = session.query(UserTrendTweet).filter_by(usertrend_id=usertrend_id).all()
		uttwtids = map(lambda x: x.tweet_id, uttwts)
		tweets = self.get_tweets_from_tweetids(uttwtids)
		return tweets

	def get_tweets_from_tweetids(self, tweet_ids):
		session = self.session
		tweets = []
		for tweet_id in tweet_ids:
			tweet = session.query(Tweet).get(tweet_id)
			tweets.append(tweet)
		return tweets

	def get_user(self, user_id):
		session = self.session
		user = session.query(User).get(user_id)
		return user

	def get_usertrend(self, usertrend_id):
		session = self.session
		usertrend = session.query(UserTrend).filter_by(usertrend_id=usertrend_id)[0]
		return usertrend

	def get_usertrends(self):
		session = self.session
		usertrends = session.query(UserTrend).all()
		return usertrends
		'''
		for usertrend in usertrends:
			user_id = usertrend.user_id
			user_id = unicodedata.normalize('NFKD', user_id).encode('ascii','ignore')
			trend_id = usertrend.trend_id
			print "User: {}, Trend: {}".format(user_id, trend_id)
		'''
	'''
	def get_random_usertrend(self):
		session = self.session
		usertrends = session.query(UserTrend).all()
		return usertrends
	'''

	def get_userid(self, usertrend_id):
		session = self.session
		usertrend = session.query(UserTrend).filter_by(usertrend_id = usertrend_id)[0]
		return usertrend.user_id

	############################################################################
	# Has Methods
	############################################################################

	def has_usertrend_for_uttl(self, usertrend_id):
		session = self.session
		q = session.query(UserTrendTweetLabel).filter_by(usertrend_id = usertrend_id)
		q_exists = session.query(q.exists()).scalar()
		return q_exists

	############################################################################
	# Generate Methods
	############################################################################

	def generate_tweet_label_csv(self, usertrend_id, sample_size=None):
		user_id = self.get_userid(usertrend_id)
		if sample_size:
			tweet_ids = self.get_sample_tweet_ids(usertrend_id, sample_size)
		else:
			tweet_ids = self.get_tweet_ids(usertrend_id)
		csvfile_path = '{}_test.csv'.format(usertrend_id)
		tweet_url_header = "https://twitter.com/u/status/"
		with open(csvfile_path, 'w+') as csvfile:
			fieldnames = ['usertrend_id', 'tweet_id', 'user_id', 'tweet_url']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for tweet_id in tweet_ids:
				tweet_url = "{}{}".format(tweet_url_header, tweet_id)
				row = {'usertrend_id': usertrend_id, 'tweet_id':tweet_id, 'user_id':user_id, 'tweet_url':tweet_url}
				writer.writerow(row)


def main():
	pass

def test():
	usertrend = usertrends[62]
	user_id = usertrend.user_id
	print usertrend.peak_day
	print user_id
	print lu.get_bio(user_id)
	tweets = lu.get_sample_tweets(usertrend.usertrend_id)
	print
	print lu.get_related_queries(user_id, usertrend.trend_id)
	print
	for tweet in tweets:
		print tweet.text
		print


if __name__ == '__main__':
	main()
