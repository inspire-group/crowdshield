from datetime import datetime

from bs4 import BeautifulSoup
from coala_utils.decorators import generate_ordering

'''
from sqlalchemy.ext.declarative import declarative_base
import sys
DATA_PATH = '../../DataNew'
sys.path.append(DATA_PATH)
import DataObjects

Base = declarative_base()

class Tweet(Base):
    #Only add tweets with lang='en'

    __tablename__ = 'tweets'
    id = Column(String, primary_key=True)
    sender = Column(String)
    text = Column(Text)
    timestamp = Column(DateTime)

    @classmethod
    def from_soup(cls, tweet):
        return cls(
            sender=tweet.find('span', 'username').text[1:],
            id=str(tweet['data-item-id']),
            timestamp=datetime.utcfromtimestamp(
                int(tweet.find('span', '_timestamp')['data-time'])).date(),
            text=tweet.find('p', 'tweet-text').text or "",
        )

    @classmethod
    def from_html(cls, html):
        soup = BeautifulSoup(html, "lxml")
        tweets = soup.find_all('li', 'js-stream-item')
        if tweets:
            for tweet in tweets:
                try:
                    yield cls.from_soup(tweet)
                except AttributeError:
                    pass  # Incomplete info? Discard!

'''

#@generate_ordering('timestamp', 'id', 'sender', 'text')
class Tweet:
    def __init__(self, sender, id, timestamp, text):
        self.sender = sender
        self.id = id
        self.timestamp = timestamp
        self.text = text

    @classmethod
    def from_soup(cls, tweet):
        return cls(
            sender=tweet.find('span', 'username').text[1:],
            id=str(tweet['data-item-id']),
            timestamp=datetime.utcfromtimestamp(
                int(tweet.find('span', '_timestamp')['data-time'])),
            text=tweet.find('p', 'tweet-text').text or "",
        )

    @classmethod
    def from_html(cls, html):
        soup = BeautifulSoup(html, "lxml")
        tweets = soup.find_all('li', 'js-stream-item')
        if tweets:
            for tweet in tweets:
                try:
                    yield cls.from_soup(tweet)
                except AttributeError:
                    pass  # Incomplete info? Discard!
                except TypeError:
                    pass  # In case of NoneType issues

'''
@generate_ordering('timestamp', 'id', 'text', 'user', 'replies', 'retweets', 'likes')
class Tweet:
    def __init__(self, user, fullname, id, url, timestamp, text, replies, retweets, likes):
        self.user = user
        self.fullname = fullname
        self.id = id
        self.url = url
        self.timestamp = timestamp
        self.text = text
        self.replies = replies
        self.retweets = retweets
        self.likes = likes

    @classmethod
    def from_soup(cls, tweet):
        return cls(
            user=tweet.find('span', 'username').text[1:],
            fullname=tweet.find('strong', 'fullname').text,
            id=tweet['data-item-id'],
            url = tweet.find('div', 'tweet')['data-permalink-path'],
            timestamp=datetime.utcfromtimestamp(
                int(tweet.find('span', '_timestamp')['data-time'])),
            text=tweet.find('p', 'tweet-text').text or "",
            replies = tweet.find(
                'span', 'ProfileTweet-action--reply u-hiddenVisually').find(
                    'span', 'ProfileTweet-actionCount')['data-tweet-stat-count'] or '0',
            retweets = tweet.find(
                'span', 'ProfileTweet-action--retweet u-hiddenVisually').find(
                    'span', 'ProfileTweet-actionCount')['data-tweet-stat-count'] or '0',
            likes = tweet.find(
                'span', 'ProfileTweet-action--favorite u-hiddenVisually').find(
                    'span', 'ProfileTweet-actionCount')['data-tweet-stat-count'] or '0',
        )

    @classmethod
    def from_html(cls, html):
        soup = BeautifulSoup(html, "lxml")
        tweets = soup.find_all('li', 'js-stream-item')
        if tweets:
            for tweet in tweets:
                try:
                    yield cls.from_soup(tweet)
                except AttributeError:
                    pass  # Incomplete info? Discard!
'''
