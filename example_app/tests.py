from pprint import pprint

import feedparser
from django.conf import settings
from django.test import TestCase

import lib.grabber.grabber as grabber


class RSSTestCase(TestCase):

    def test_RSSEntriesGrabber(self):
        
        grabber = grabber.RSSEntriesGrabber()
        
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
