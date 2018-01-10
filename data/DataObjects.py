from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import inspect

#from sqlalchemy.orm import scored_session, sessionmaker
#from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import (
	Column,
	Integer,
	String,
	Text,
	Boolean,
	ForeignKey,
	Date,
	DateTime,
	Sequence,
	Float
)
import datetime


Base = declarative_base()


class Trend(Base):
	__tablename__ = 'trends'
	id = Column(String, primary_key=True)
	start_date = Column(Date)
	trend_url = Column(String)
	usertrends = relationship("UserTrend", backref="trends")


class User(Base):
	'''
	Only add users who are alive
	'''
	__tablename__ = 'users'
	id = Column(String, primary_key=True)
	twitter_name = Column(String)
	wiki_url = Column(String)
	bio = Column(String)
	explore_url = Column(String)
	usertrends = relationship("UserTrend", backref="users")


class UserTrend(Base):
	__tablename__ = 'usertrends'
	user_id = Column(String, ForeignKey('users.id'), primary_key=True)
	trend_id = Column(String, ForeignKey('trends.id'), primary_key=True)
	usertrend_id = Column(String, nullable=False, unique=True)
	peak_day = Column(Date)
	headlines = Column(String)
	interest_over_time = Column(String)
	tweets_over_time = Column(String)
	explore_trend_url = Column(String)
	usertrend_tweets = relationship("UserTrendTweet", backref="usertrends")


class Tweet(Base):
	'''
	Only add tweets with lang='en'
	'''
	__tablename__ = 'tweets'
	id = Column(String, primary_key=True)
	sender = Column(String)
	text = Column(Text)
	timestamp = Column(DateTime)
	usertrend_tweets = relationship("UserTrendTweet", backref="tweets")


class UserTrendTweet(Base):
	__tablename__ = 'usertrendtweets'
	usertrend_id = Column(String, ForeignKey('usertrends.usertrend_id'), primary_key=True)
	tweet_id = Column(String, ForeignKey('tweets.id'), primary_key=True)
	usertrendtweet_labels = relationship("UserTrendTweetLabel", backref="usertrendtweets")


class UserTrendTweetLabel(Base):
	__tablename__ = 'usertrendtweetlabels'
	usertrend_id = Column(String, primary_key=True)
	tweet_id = Column(String, primary_key=True)
	'''
	user_id = Column(String)
	user_bio = Column(String)
	tweet_url = Column(String)
	'''
	text = Column(Text)
	label = Column(Integer)
	__table_args__ = (ForeignKeyConstraint([usertrend_id, tweet_id],
                                           [UserTrendTweet.usertrend_id, UserTrendTweet.tweet_id]),
                      {})


def create_tables(DB_URL):
	engine = create_engine(DB_URL, echo=True)
	Base.metadata.create_all(bind=engine)
	# check tables exist
	ins = inspect(engine)
	for _t in ins.get_table_names():
		print _t
