from django.contrib.auth.models import User
from django.test import TestCase
from marshmallow import pprint

from example_app.models import Tag, Post
from example_app.rss_integration import EntrySchema
from example_app.serializers import PostSchema
from lib.integration.rss.classes import RSSGrabber

REDDIT_RSS_ENDPOINT = 'https://www.reddit.com/r/news/.rss'
HABRAHABR_RSS_ENDPOINT = 'https://habrahabr.ru/rss/hubs/all/'


class RSSTestCase(TestCase):

    def test_get_feeds(self):
        grabber = RSSGrabber(url=REDDIT_RSS_ENDPOINT)
        data = grabber.load_data()

        schema = EntrySchema()
        result = schema.dump(data['entries'], many=True)

        for entry in result.data:
            # tags
            tags = []
            for tag_data in entry['tags']:
                tag, _ = Tag.objects.get_or_create(**tag_data)
                tags.append(tag)

            # author
            author, _ = User.objects.get_or_create(username=entry['author'])

            kwargs = entry.copy()
            kwargs['author'] = author
            del kwargs['tags']

            post = Post.objects.create(**kwargs)
            post.tags.set(tags)
