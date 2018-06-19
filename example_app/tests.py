from django.conf import settings
from django.test import TestCase

from grabber import RSSEntriesGrabber


class RSSTestCase(TestCase):

    def test_RSSEntriesGrabber(self):
        grabber = RSSEntriesGrabber(url=settings.REDDIT_RSS_ENDPOINT)
        entries = grabber.load_data()
        self.assertTrue(isinstance(entries, list))

