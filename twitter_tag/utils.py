from __future__ import unicode_literals
import re
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from cacheback.decorators import cacheback
from django.conf import settings
from django.core.cache import cache
from hashlib import md5
import json
from twitter import Twitter, OAuth, TwitterError


TWITTER_HASHTAG_URL = '<a href="https://twitter.com/search?q=%%23%s">#%s</a>'
TWITTER_USERNAME_URL = '<a href="https://twitter.com/%s">@%s</a>'

try:
    TWITTER_CACHE_TIMEOUT = settings.TWITTER_CACHE_TIMEOUT
except AttributeError:
    TWITTER_CACHE_TIMEOUT = 300


def urlize_tweet(tweet):
    """ Turn #hashtag and @username in a text to Twitter hyperlinks,
        similar to the ``urlize()`` function in Django.
    """
    text = tweet.get('html', tweet['text'])
    for hash in tweet['entities']['hashtags']:
        text = text.replace('#%s' % hash['text'], TWITTER_HASHTAG_URL % (quote(hash['text'].encode("utf-8")), hash['text']))
    for mention in tweet['entities']['user_mentions']:
        text = text.replace('@%s' % mention['screen_name'], TWITTER_USERNAME_URL % (quote(mention['screen_name']), mention['screen_name']))
    tweet['html'] = text
    return tweet


def expand_tweet_urls(tweet):
    """ Replace shortened URLs with long URLs in the twitter status, and add the "RT" flag.
        Should be used before urlize_tweet
    """
    if 'retweeted_status' in tweet:
        text = 'RT @{user}: {text}'.format(user=tweet['retweeted_status']['user']['screen_name'],
                                           text=tweet['retweeted_status']['text'])
        urls = tweet['retweeted_status']['entities']['urls']
    else:
        text = tweet['text']
        urls = tweet['entities']['urls']

    for url in urls:
        text = text.replace(url['url'], '<a href="%s">%s</a>' % (url['expanded_url'], url['display_url']))
    tweet['html'] = text
    return tweet


def get_twitter_object():
    return Twitter(auth=OAuth(settings.TWITTER_OAUTH_TOKEN,
                             settings.TWITTER_OAUTH_SECRET,
                             settings.TWITTER_CONSUMER_KEY,
                             settings.TWITTER_CONSUMER_SECRET))

@cacheback(lifetime=TWITTER_CACHE_TIMEOUT)
def get_user_tweets(**kwargs):
    '''
    Function moved out from UserTag.get_json so cacheback can call it.
    '''
    cache_key = 'django-twitter-tag:get_user_tweets:{}'.format(md5(json.dumps(kwargs, sort_keys=True)).hexdigest())
    if cache.get(cache_key):
        # Prevent hammering the API when rate limiting happens
        return
    cache.set(cache_key, True, TWITTER_CACHE_TIMEOUT)
    twitter = get_twitter_object()
    tweets = twitter.statuses.user_timeline(**kwargs)
    return [tweet for tweet in tweets]


@cacheback(lifetime=TWITTER_CACHE_TIMEOUT)
def get_search_tweets(**kwargs):
    '''
    Function moved out from SearchTag.get_json so cacheback can call it.
    '''
    cache_key = 'django-twitter-tag:get_search_tweets:{}'.format(md5(json.dumps(kwargs, sort_keys=True)).hexdigest())
    if cache.get(cache_key):
        # Prevent hammering the API when rate limiting happens
        return
    cache.set(cache_key, True, TWITTER_CACHE_TIMEOUT)
    twitter = get_twitter_object()
    tweets = twitter.search.tweets(**kwargs)['statuses']
    return [tweet for tweet in tweets]
