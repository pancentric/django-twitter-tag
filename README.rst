Django Twitter Tag
==================

This is the Pancentric fork of Django Twitter Tag. We added django-cacheback
and Celery so that users never have to wait for us to fetch new tweets -
fetching is done in a background task queue.


A django template tag to display user's recent tweets / search results.
Version 1.0 uses Twitter API 1.1.

Basic features are limiting numbers of displayed tweets, filtering out replies and retweets.
Library exposes each tweet ``json`` in template, adding extra attributes: ``html`` and ``datetime``.
First one makes urls, hashtags or twitter usernames clickable, juts like you expect them to be.
Last one provides python datetime object to ease output in templates.
Urls are expanded by default. Library handles twitter exceptions gracefully,
returning last successful response.

Usage
-----

* Load tag in your template like this::

    {% load twitter_tag %}


* Get user's (``futurecolors`` in example) most recent tweets and store them in ``tweets`` variable::

    {% get_tweets for "futurecolors" as tweets %}


* Now you have a list of tweets in your template context, which you can iterate over like this::

    <ul>
    {% for tweet in tweets %}
        <li>{{ tweet.html|safe }}</li>
    {% endfor %}
    </ul>

See how it looks like `on our site`_.

.. _on our site: http://futurecolors.ru/


Installation
------------

This app works with python 2.6, 2.7 and 3.3, Django 1.3-1.5.

Recommended way to install is pip::

  pip install -e git+https://github.com/pancentric/django-twitter-tag.git#egg=django-twitter-tag

We use Redis as our Celery message broker so you probably want to install the following::

  pip install django-celery-with-redis==3.0


Add ``twitter_tag`` to ``INSTALLED_APPS`` in settings.py::

    INSTALLED_APPS = (...
                      'cacheback',
                      'djcelery',
                      'twitter_tag',
                      ...
                     )

Configuration
-------------

Twitter `API 1.1`_ requires authentication for every request you make,
so you have to provide some credentials for oauth dance to work.
First, `create an application`_, second, request access token on newly created
app page. The `process of obtaining a token`_ is explained in detail in docs.

Here is an example of how your config might look like::

    # settings.py
    # Make sure to replace with your own values, theses are just made up

    # Your access token: Access token
    TWITTER_OAUTH_TOKEN = '91570701-BQMM5Ix9AJUC5JtM5Ix9DtwNAiaaYIYGN2CyPgduPVZKSX'
    # Your access token: Access token secret
    TWITTER_OAUTH_SECRET = 'hi1UiXm8rF4essN3HlaqMz7GoUvy3e4DsVkBAVsg4M'
    # OAuth settings: Consumer key
    TWITTER_CONSUMER_KEY = '3edIOec4uu00IGFxvQcwJe'
    # OAuth settings: Consumer secret
    TWITTER_CONSUMER_SECRET = 'YBD6GyFpvumNbNA218RAphszFnkifxR8K9h8Rdtq1A'

    TWITTER_CACHE_TIMEOUT = 300

    BROKER_URL = _get_env_variable('BROKER_URL', default='redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = BROKER_URL
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']


.. _API 1.1: https://dev.twitter.com/docs/api/1.1
.. _create an application: https://dev.twitter.com/apps
.. _process of obtaining a token: https://dev.twitter.com/docs/auth/tokens-devtwittercom
.. _django cache framework: https://docs.djangoproject.com/en/dev/topics/cache/

Examples
--------

You can specify number of tweets to show::

    {% get_tweets for "futurecolors" as tweets limit 10 %}


To filter out tweet replies (that start with @ char)::

    {% get_tweets for "futurecolors" as tweets exclude "replies" %}


To ignore native retweets::

    {% get_tweets for "futurecolors" as tweets exclude "retweets" %}


Or everything from above together::

    {% get_tweets for "futurecolors" as tweets exclude "replies, retweets" limit 10 %}


Search tag (experimental)
-------------------------

You can search for tweets::

    {% search_tweets for "python 3" as tweets limit 5 %}

Search api arguments are supported via key=value pairs::

    {% search_tweets for "python 3" as tweets lang='eu' result_type='popular' %}

Relevant `API docs for search`_.

.. _API docs for search: https://dev.twitter.com/docs/api/1.1/get/search/tweets

Caching
-------

There is no need to use any django cache template tags as suggested in the upstream
project's documentation. You will want to configure CACHES in settings.py to be
something like this so that the task jobs can put the results in the shared location::

    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': _get_env_variable('REDIS_LOCATION'),
            'OPTIONS': {
                'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            }
        }
    }

.. _rate limit: https://dev.twitter.com/docs/rate-limiting/1.1

Extra
-----

Tweet's properties
~~~~~~~~~~~~~~~~~~

get_tweets returns a list of tweets into context. Each tweets is a json dict, that has
exactly the same attributes, as stated in API 1.1 docs, describing `tweet json`_.
Tweet's created timestamp is converted to python object and is available in templates::

    {{ tweet.datetime|date:"D d M Y" }}

.. _tweet json: https://dev.twitter.com/docs/platform-objects/tweets

Tweet's html
~~~~~~~~~~~~

Tweet also has extra ``html`` property, which contains tweet, formatted for html output
with all needed links. Note, Twitter has `guidelines for developers`_ on how embeded tweets
should look like.

.. _guidelines for developers: https://dev.twitter.com/terms/display-requirements

Exception handling
~~~~~~~~~~~~~~~~~~

Any Twitter API exceptions like 'Over capacity' are silenced and logged.
Django cache is used internally to store last successful response in case `twitter is down`_.

.. _twitter is down: https://dev.twitter.com/docs/error-codes-responses

Going beyond
~~~~~~~~~~~~
Since version 1.0 you can create your own template tags for specific twitter queries,
not supported by this library. Simply inherit from ``twitter_tag.templatetags.twitter_tag.BaseTwitterTag``
and implement your own ``get_json`` method (tag syntax is contolled by django-classy-tags).

Development
-----------

To install `development version`_, use ``pip install django-twitter-tag==dev``

.. _development version: https://github.com/coagulant/django-twitter-tag/archive/dev.tar.gz#egg=django_twitter_tag-dev

Tests
-----

Run::

    DJANGO_SETTINGS_MODULE = twitter_tag.test_settings python setup.py test
