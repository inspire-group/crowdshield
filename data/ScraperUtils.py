from bs4 import BeautifulSoup
import re
import requests
import unicodedata
import urllib

import datetime
from dateutil import parser, relativedelta

#from twitterscraper.query import query_tweets, query_tweets_once


def get_soup(url):
	'''
	Params: Url to be scraped
	Returns: BeautifulSoup object if the url yields a successful page.
	If the url is not valid or there is an error with requesting the url,
	returns None.
	'''
	try:
		page = requests.get(url)
	except:
		return None
	if page.status_code == 404:
		return None
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup


class TrendUtils(object):

	def __init__(self):
		pass

	def getTrendURL(self, trend_id):
		trend_prefix = 'https://trends.google.com/trends/topcharts/widget'
		trend_params = {'cid': 'people', 'geo': 'US', 'date': None, 'vm': 'trendingchart'}
		trend_params['date'] = trend_id
		trend_url = trend_prefix + '?' + urllib.urlencode(trend_params)
		return trend_url


class UserUtils(object):

	def __init__(self):
		pass

	def remove_non_ascii(self, text):
	    return ''.join(i for i in text if ord(i)<128)

	def get_trend_infos(self, trend_url):
		'''
		Params: Url for the Google Trends top 10 people for a given year, month
		Returns: List of tuples of (person, wiki) where each person is listed in the
		Google Trends top 10 people and the wiki is the link to their Wikipedia
		article.
		'''
		soup = get_soup(trend_url)
		if not soup:
			return [], [], []
		class_people = 'widget-title-in-list'
		people_unicode = soup.find_all('span', class_=class_people)
		people = map(lambda person: person.get_text(), people_unicode)

		class_wiki = 'topcharts-detailedchart-entity-description-source'
		wiki_unicode = soup.find_all('a', class_=class_wiki)
		wikis = map(lambda wiki: wiki[u'href'], wiki_unicode)

		class_trend_explore = 'topcharts-detailedchart-entity-search'
		trend_unicode = soup.find_all('a', class_=class_trend_explore)
		trend_header = 'https://trends.google.com'
		trend_tails = map(lambda trend: trend[u'href'], trend_unicode)
		trend_tails = map(lambda trend_tail: re.sub(r'&.*','', trend_tail), trend_tails) #strip to only have user query
		explores = map(lambda trend_tail: "{}{}".format(trend_header, trend_tail), trend_tails)
		return people, wikis, explores
		

	def get_twitter_name(self, user_id):
		'''
		Params: (user_id) Name of the User
		Returns: The twitter username associated with a Google search of the User's name
		'''
		name = user_id
		name = unicodedata.normalize('NFKD', name).encode('ascii','ignore')
		google_prefix = 'https://google.com/search'
		google_params = {'q': name + ' ' + 'twitter'}
		google_url = google_prefix + '?' + urllib.urlencode(google_params)
		soup = get_soup(google_url)
		if not soup:
			return None
		cite = soup.find('cite')
		twitter_url = cite.get_text()
		soup = get_soup(twitter_url)
		if not soup:
			return None
	 	target = soup.find('b', class_='u-linkComplex-target')
		if not target:
			return None
		username = target.get_text()
		return username


	def get_bio(self, wiki_url):
		'''
		Params: Wikipedia link to the User
		Returns: The biography associated with the Wikipedia page of the User,
		given that the user is alive
		'''
		soup = get_soup(wiki_url)
		if not soup:
			return None

		def isalive():
			'''
			Returns: Boolean for whether or not the person is still alive based on
			Wikipedia link
			'''
			class_infobox = re.compile('infobox')
			infobox = soup.find('table', class_=class_infobox)
			if infobox == None:
				return False
			dead = False
			death_vocab = {'died', 'death'}
			for death_word in death_vocab:
				dead = dead or re.search(death_word, infobox.get_text(), re.IGNORECASE)
			alive = not dead
			return alive

		if not isalive():
			return None

		mw_parser_output = soup.find('div', class_='mw-parser-output')
		first_paragraph = mw_parser_output.find('p', recursive=False)
		bio = first_paragraph.get_text()
		#bio = remove_non_ascii(bio)
		return bio


class UserTrendUtils(object):

	def __init__(self):
		pass

	def getTimeFrame(self, trend):
		start_date = trend.start_date
		end_date = start_date + relativedelta.relativedelta(months=1)
		start_date_str = start_date.strftime("%Y-%m-%d")
		end_date_str = end_date.strftime("%Y-%m-%d")
		return "{} {}".format(start_date_str, end_date_str)


	def getPeakDayAndTimeSeries(self, user_id, pytrend):
		interest_over_time_df = pytrend.interest_over_time()
		df = interest_over_time_df[user_id]
		peak_day = df[df.values == 100].index.date[0]
		timeseries = str(list(df.values))
		return peak_day, timeseries


	def getRelatedQueries(self, user_id, pytrend):
		related_queries_dict = pytrend.related_queries()
		first_key = related_queries_dict.keys()[0]
		inner_dict = related_queries_dict[first_key]['top']
		if inner_dict is None:
			return None
		if 'query' not in inner_dict:
			return None
		related_queries_list = inner_dict['query'].values
		related_queries = str(related_queries_list[:5])
		return related_queries


	def getUserTrendInfos(self, trend_url):
		'''
		Params: Url for the Google Trends top 10 people for a given year, month
		Returns: List of tuples of (person, wiki) where each person is listed in the
		Google Trends top 10 people and the wiki is the link to their Wikipedia
		article.
		'''
		soup = get_soup(trend_url)
		if not soup:
			return [], []
		class_people = 'widget-title-in-list'
		people_unicode = soup.find_all('span', class_=class_people)
		people = map(lambda person: person.get_text(), people_unicode)

		class_wiki = 'topcharts-detailedchart-entity-description-source'
		wiki_unicode = soup.find_all('a', class_=class_wiki)
		wikis = map(lambda wiki: wiki[u'href'], wiki_unicode)

		class_trend_explore = 'topcharts-detailedchart-entity-search'
		trend_unicode = soup.find_all('a', class_=class_trend_explore)
		trend_header = 'https://trends.google.com'
		trend_tails = map(lambda trend: trend[u'href'], trend_unicode)
		explore_trends = map(lambda trend_tail: "{}{}".format(trend_header, trend_tail), trend_tails)
		return people, wikis, explore_trends

	def getHeadlines(self, user_id, peak_day):
		'''
		Params: (user_id) Name of the User
		Returns: The twitter username associated with a Google search of the User's name
		'''
		name = user_id
		name = unicodedata.normalize('NFKD', name).encode('ascii','ignore')
		date_str = peak_day.strftime("%B")
		google_prefix = 'https://google.com/search'
		google_params = {'q': name + ' ' + date_str}
		google_url = google_prefix + '?' + urllib.urlencode(google_params)
		soup = get_soup(google_url)
		if not soup:
			return None
		headers = soup.find_all('h3', class_='r')
		top5 = headers[:5]
		headlines = map(lambda h: unicodedata.normalize('NFKD', h.get_text()).encode('ascii','ignore'), top5)
		return str(headlines)

	def getTweetsOverTime(self):
		pass


def test():
	'''
	url = "https://google.com"
	soup = get_soup(url)
	print soup.prettify()
	'''
	peakday = datetime.date(2016, 1, 1)
	tweets = UserTrendTweetUtils().getPeakdayTweets('barackobama', peakday)
	print tweets

if __name__ == '__main__':
	test()