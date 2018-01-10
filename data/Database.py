from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import exists
from sqlalchemy import and_

import urllib
import datetime
from dateutil import parser, relativedelta
from time import time

from DataObjects import Trend, User, UserTrend, UserTrendTweet, Tweet
from ScraperUtils import TrendUtils, UserUtils, UserTrendUtils

import sys
PYTRENDS_PATH = '../lib/pytrends'
sys.path.append(PYTRENDS_PATH)
from pytrends.request import TrendReq

TWITTERSCRAPER_PATH = '../lib/twitterscraper'
sys.path.append(TWITTERSCRAPER_PATH)
from twitterscraper.query import query_tweets, query_tweets_once

#from query import query_tweets

class Database(object):

	############################################################################
	# Database Setup Methods
	############################################################################

	def __init__(self):
		DB_NAME = "sqlite:///db.sqlite"
		self.engine = create_engine(DB_NAME, echo=False)

	def start_session(self):
		engine = self.engine
		Session = sessionmaker()
		Session.configure(bind=engine)
		self.session = Session()

	def close_session(self):
		self.session.close()

	############################################################################
	# Populate Methods
	############################################################################

	def populateTrendsTable(self):
		# create session
		years = ['2016']
		months = ['01', '02', '03', '04', '05', '06',
				  '07', '08', '09', '10', '11', '12']
		self.session
		year = years[0]
		for month in months:
			trend_id = '{}{}'.format(year, month)
			trend_id_exists = session.query(exists().where(Trend.id==trend_id)).scalar()
			if trend_id_exists:
				continue
			start_day = '01'
			start_date = datetime.date(int(year), int(month), int(start_day))
			trend_url = TrendUtils().getTrendURL(trend_id)
			row = Trend(id=trend_id, start_date=start_date, trend_url=trend_url)
			session.add(row)
		session.commit()


	def populateUsersTable(self):
		'''
		Check that user is alive
		Check that user has a twitter username
		Check that the username is not already in the database
		Check that the user has a bio
		'''
		session = self.session
		trends = session.query(Trend).all()
		for trend in trends:
			trend_url = trend.trend_url
			user_ids, wiki_urls, explore_urls = UserUtils().get_trend_infos(trend_url)
			if not (len(user_ids) == len(wiki_urls) == len(explore_urls) == 10):
				continue
			for i in range(10):
				user_id = user_ids[i]
				user_id_exists = session.query(exists().where(User.id==user_id)).scalar()
				if user_id_exists:
					continue
				wiki_url = wiki_urls[i]
				bio = UserUtils().get_bio(wiki_url)
				if not bio:
					continue
				twitter_name = UserUtils().get_twitter_name(user_id)
				if not twitter_name:
					continue
				explore_url = explore_urls[i]
				row = User(id=user_id, twitter_name=twitter_name, bio=bio, wiki_url=wiki_url, explore_url=explore_url)
				session.add(row)
			session.commit()


	def populateUserTrendsTable(self):
		session = self.session
		trends = session.query(Trend).all()
		for trend in trends:
			trend_id = trend.id
			timeframe = UserTrendUtils().getTimeFrame(trend)
			pytrend = TrendReq()

			trend_url = trend.trend_url
			user_ids, wiki_urls, explore_urls = UserTrendUtils().getUserTrendInfos(trend_url)
			if not (len(user_ids) == len(wiki_urls) == len(explore_urls) == 10):
				continue

			for i in range(10):
				user_id = user_ids[i]
				user_id_exists = session.query(exists().where(User.id==user_id)).scalar()
				if not user_id_exists:
					continue
				usertrend_exists = session.query(UserTrend).filter_by(user_id=user_id, trend_id=trend_id).exists()
				usertrend_exists = session.query(usertrend_exists).scalar()
				if usertrend_exists:
					continue
				pytrend.build_payload(kw_list=[user_id], timeframe=timeframe, geo='US')
				'''
				TODO: Remove this code
				related_queries = UserTrendUtils().getRelatedQueries(user_id, pytrend)
				if not related_queries:
					continue
				'''
				peak_day, timeseries = UserTrendUtils().getPeakDayAndTimeSeries(user_id, pytrend)
				user = session.query(User).get(user_id)
				twitter_name = user.twitter_name
				usertrend_id = "{}-{}".format(twitter_name, trend_id)
				explore_trend_url = explore_urls[i]
				row = UserTrend(user_id=user_id, trend_id=trend_id, usertrend_id=usertrend_id, peak_day=peak_day,
								interest_over_time=timeseries, related_queries=related_queries, tweets_over_time="",
								explore_trend_url=explore_trend_url)
				session.add(row)
			session.commit()


	def populateUserTrendTweetsAndTweetsTable(self, trend_id):
		'''
		Params: trend - we will query by trend to do this in a more controlled manner
		'''
		session = self.session
		trend = session.query(Trend).get(trend_id)
		usertrends = session.query(UserTrend).filter_by(trend_id=trend.id).all()
		for usertrend in usertrends:

			usertrend_id = usertrend.usertrend_id
			usertrendtweet_populated = session.query(UserTrendTweet).filter_by(usertrend_id=usertrend_id).exists()
			usertrendtweet_populated = session.query(usertrendtweet_populated).scalar()
			if usertrendtweet_populated:
				continue

			user_id = usertrend.user_id
			user = session.query(User).get(user_id)
			twitter_name = user.twitter_name
			#query = "%40{}".format(twitter_name) # Make sure we only read in English tweets
			peak_day = usertrend.peak_day
			next_day = peak_day + relativedelta.relativedelta(days=1)
			query = 'to:{} since:{} until:{}'.format(twitter_name, peak_day, next_day)
			print "\n##################### Scraping {} #######################".format(query)
			time0 = time()
			tweets = query_tweets_once(query=query)
			#tweets = query_tweets(query=query, begindate=peak_day, enddate=next_day, poolsize=4)
			collect_time = time() - time0
			print "##################### Collected {} tweets in {} seconds #######################".format(len(tweets), collect_time)

			for tweet in tweets:
				tweet_id = tweet.id
				tweet_exists = session.query(Tweet).filter_by(id=tweet.id).exists()
				tweet_exists = session.query(tweet_exists).scalar()
				tweet = Tweet(id=tweet.id, sender=tweet.sender, timestamp=tweet.timestamp, text=tweet.text)
				if not tweet_exists:
					session.add(tweet)

				usertrendtweet_exists = session.query(UserTrendTweet).filter_by(usertrend_id=usertrend_id, tweet_id=tweet_id).exists()
				usertrendtweet_exists = session.query(usertrendtweet_exists).scalar()
				if not usertrendtweet_exists:
					usertrendtweet = UserTrendTweet(usertrend_id=usertrend_id, tweet_id=tweet_id)
					session.add(usertrendtweet)
			session.commit()


	def populateUserTrendTweetLabelsTable(self, usertrend_id):
		'''
		Params: trend - we will query by trend to do this in a more controlled manner
		'''
		session = self.session
		usertrendtweet_count = session.query(UserTrendTweet).filter_by(usertrend_id=usertrend_id).count()
		if usertrendtweet_count < 1000:
			return

		tweets = session.query(UserTrendTweet).filter_by(usertrend_id=usertrend_id).all()
		for tweet in tweets:
			tweet_id = tweet.id
			tweet_exists = session.query(Tweet).filter_by(id=tweet.id).exists()
			tweet_exists = session.query(tweet_exists).scalar()
			tweet = Tweet(id=tweet.id, sender=tweet.sender, timestamp=tweet.timestamp, text=tweet.text)
			if not tweet_exists:
				session.add(tweet)

			usertrendtweetlabel_exists = session.query(UserTrendTweet).filter_by(usertrend_id=usertrend_id, tweet_id=tweet_id).exists()
			usertrendtweetlabel_exists = session.query(usertrendtweet_exists).scalar()
			if not usertrendtweet_exists:
				usertrendtweet = UserTrendTweet(usertrend_id=usertrend_id, tweet_id=tweet_id)
				session.add(usertrendtweet)
		session.commit()


	def updateUserTrend(self):
		'''
		Params: usertrend - we will query by usertrend to do this in a more controlled manner
		'''
		session = self.session
		usertrends = session.query(UserTrend).all()
		for ut in usertrends:
			user_id = ut.user_id
			peak_day = ut.peak_day
			headlines = UserTrendUtils().getHeadlines(user_id, peak_day)
			ut.headlines = headlines
			session.commit()


	def getTweetTimeline(self, usertrend_id):
		# TODO: In the works
		return
		'''
		Params: trend - we will query by trend to do this in a more controlled manner
		'''
		session = self.session
		usertrend = session.query(UserTrend).get(usertrend_id)
		peak_day = usertrend.peak_day
		next_day = peak_day + relativedelta.relativedelta(days=1)
		query = 'to:{} since:{} until:{}'.format(twitter_name, peak_day, next_day)
		print "\n##################### Scraping {} #######################".format(query)
		time0 = time()
		tweets = query_tweet_count(query=query)
		collect_time = time() - time0
		print "##################### Collected {} tweets in {} seconds #######################".format(len(tweets), collect_time)


	def testQuery(self):
		session = self.session
		'''
		tweets = session.query(Tweet).all()
		for trend in tweets[:10]:
			print trend.id
			print trend.usertrend_tweets
		'''
		trends = session.query(Trend).all()
		for trend in trends:
			print trend.id
			print trend.usertrends


def main():
	db = Database()
	db.start_session()
	try: db.updateUserTrend()
	finally: db.close_session()


if __name__ == '__main__':
	main()
