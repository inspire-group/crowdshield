from DataObjects import create_engine, create_tables, Tweet, UserTrendTweet, UserTrendTweetLabel
from Database import Database
from DataUtils import DataUtils

import gensim


def recreate_uttl_table():
	'''
	DANGER - Do Not Use This Method Unless You Know What You Are Doing
	'''
	DB_URL = "sqlite:///db.sqlite"
	engine = create_engine(DB_URL, echo=True)
	UserTrendTweetLabel.__table__.drop(engine)
	UserTrendTweetLabel.__table__.create(engine)


def collect_all_tweets():
	db = Database()
	db.start_session()
	#trends = ['201602', '201603', '201604']
	try:
		for trend in trends:
			trend_id = trend.id
			db.populateUserTrendTweetsAndTweetsTable(trend_id)
	finally:
		db.close_session()


def add_all_sample_tweets():
	sample_size = 100
	du = DataUtils()
	du.start_session()
	try:
		usertrends = du.get_usertrends()
		usertrend_ids = map(lambda u: u.usertrend_id, usertrends)
		for uid in usertrend_ids:
			if du.has_usertrend_for_uttl(uid):
				continue
			num_tweets = du.get_num_tweets(uid)
			if num_tweets < 1000:
				continue
			sample_tweet_ids = du.get_sample_tweet_ids(uid, sample_size)
			tweets = du.get_tweets(sample_tweet_ids)
			uttls = map(lambda tweet: UserTrendTweetLabel(
										usertrend_id=uid,
										tweet_id=tweet.id,
										text=tweet.text),
						tweets)
			du.add_usertrendtweetlabels(uttls)
	finally:
		du.close_session()


def main():
	du = DataUtils()
	du.start_session()
	usertrends = []
	try:
		usertrends = du.get_usertrends()
		for ut in usertrends:
			usertrend_id = ut.usertrend_id
			ntwts = du.get_num_tweets(usertrend_id)
			print ut.usertrend_id, ntwts
	finally: du.close_session()


if __name__ == '__main__':

	#add_all_sample_tweets()
	main()
