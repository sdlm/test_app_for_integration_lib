from pprint import pprint

import feedparser
from django.conf import settings
from django.test import TestCase


class RSSTestCase(TestCase):

    def test_get_feeds(self):
        print('=' * 50)
        print('=' * 50)
        print('HABRAHABR_RSS:')
        response = feedparser.parse(settings.HABRAHABR_RSS_ENDPOINT)
        pprint(response)
        print('=' * 50)
        print('=' * 50)
        print('REDDIT_RSS_ENDPOINT:')
        response = feedparser.parse(settings.REDDIT_RSS_ENDPOINT)
        pprint(response)
