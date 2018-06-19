import json

from django.conf import settings
from django.test import TestCase
from grabber import RSSEntriesGrabber

from example_app.constants import ENTRIES_FILE_PATH
from example_app.models import Post
from example_app.serializers import PostSerializer


class RSSTests(TestCase):

    def get_entries(self, from_dump=True):
        if from_dump:
            with open(ENTRIES_FILE_PATH, 'r') as json_file:
                return json.load(json_file)
        grabber = RSSEntriesGrabber(url=settings.REDDIT_RSS_ENDPOINT)
        return grabber.load_data()

    def test_RSSEntriesGrabber(self):
        entries = self.get_entries(from_dump=False)
        self.assertTrue(isinstance(entries, list))

    def test_DRFSerializer(self):
        self.assertFalse(Post.objects.exists())
        entries = self.get_entries()
        serializer = PostSerializer(data=entries, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertTrue(Post.objects.exists())
