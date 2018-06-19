import json

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker
from grabber import RSSEntriesGrabber

from example_app.constants import ENTRIES_FILE_PATH
from example_app.fork_serializers import DjangoUserSchema, DjangoEntrySchema
from example_app.models import Post, Tag

REDDIT_RSS_ENDPOINT = 'https://www.reddit.com/r/news/.rss'
HABRAHABR_RSS_ENDPOINT = 'https://habrahabr.ru/rss/hubs/all/'


class GrabberTests(TestCase):

    def test_grabber(self):
        entries = get_entries(from_dump=False)
        self.assertTrue(isinstance(entries, list))


class SchemaTests(TestCase):

    def test_basic(self):
        fake = Faker()
        schema = DjangoUserSchema()
        name = fake.user_name()
        schema.load({'name': name})
        self.assertTrue(User.objects.filter(username=name).exists())

    def test_schema(self):
        entries = get_entries()
        names = self.collect_author_names(entries)
        entries = self.represent_author_as_dict(entries)
        load_entries(entries)
        self.assertEqual(Post.objects.count(), len(entries))
        self.assertEqual(set(User.objects.values_list('username', flat=True)), names)

    def test_m2m_relation(self):
        entry = get_fake_entry(tags_count=5)
        tag_names = {x['term'] for x in entry['tags']}
        load_entries([entry])
        self.assertEqual(set(Tag.objects.values_list('name', flat=True)), tag_names)

    def test_fk_relation(self):
        entry = get_fake_entry()
        load_entries([entry])
        name = entry['author']['name']
        self.assertTrue(User.objects.filter(username=name).exists())

    def test_update(self):
        url = get_fake_url()
        post = create_fake_post(url=url)

        entry = get_fake_entry(link=url, tags_count=2)

        load_entries([entry])

        post.refresh_from_db()
        self.compare_post_and_entry(post, entry)

    def compare_post_and_entry(self, post, entry):
        self.assertEqual(post.title, entry['title'])
        self.assertEqual(post.text, entry['summary'])
        user = User.objects.get(username=entry['author']['name'])
        self.assertEqual(post.author, user)
        self.assertEqual(
            set(post.tags.values_list('name', flat=True)),
            {x['term'] for x in entry['tags']}
        )

    def collect_author_names(self, entries):
        return {entry['author'] for entry in entries}

    def represent_author_as_dict(self, entries):
        results = list(entries)
        for entry in results:
            entry['author'] = {'name': entry['author']}
        return results


class DuplicatesTests(TestCase):

    def test_duplicate_authors(self):
        entry_1, entry_2 = get_two_fake_entries(duplicate_field='author')
        load_entries(entries=[entry_1, entry_2])
        self.assertEqual(User.objects.count(), 1)
        name = entry_1['author']['name']
        self.assertTrue(User.objects.filter(username=name).exists())

    def test_duplicate_tags(self):
        entry_1, entry_2 = get_two_fake_entries(duplicate_field='tags')
        load_entries(entries=[entry_1, entry_2])
        self.assertEqual(Tag.objects.count(), 1)
        tag_name = entry_1['tags'][0]['term']
        self.assertTrue(Tag.objects.filter(name=tag_name).exists())

    def test_duplicate_unique_field(self):
        entry_1, entry_2 = get_two_fake_entries(duplicate_field='link')
        load_entries(entries=[entry_1, entry_2])
        self.assertEqual(Post.objects.count(), 1)
        url = entry_1['link']
        self.assertTrue(Post.objects.filter(url=url).exists())


def load_entries(entries):
    schema = DjangoEntrySchema()
    for entry in entries:
        schema.load(entry)


def get_entries(from_dump=True):
    if from_dump:
        with open(ENTRIES_FILE_PATH, 'r') as json_file:
            return json.load(json_file)
    grabber = RSSEntriesGrabber(url=settings.REDDIT_RSS_ENDPOINT)
    return grabber.load_data()


def get_two_fake_entries(duplicate_field: str = None):
    entry_1, entry_2 = get_fake_entry(), get_fake_entry()
    if not duplicate_field:
        return entry_1, entry_2
    entry_2[duplicate_field] = entry_1[duplicate_field]
    return entry_1, entry_2


def get_fake_entry(tags_count: int = 1, link: str = None) -> dict:
    fake = Faker()
    return {
        'title': fake.sentence(),
        'summary': fake.text(),
        'author': {'name': fake.user_name()},
        'tags': [{'term': fake.word()} for _ in range(tags_count)],
        'link': link or fake.url()
    }


def get_fake_url() -> str:
    fake = Faker()
    return fake.url()


def create_fake_post(url: str = None) -> Post:
    fake = Faker()
    post = Post.objects.create(
        title=fake.sentence(),
        text=fake.text(),
        author=User.objects.create(username=fake.user_name()),
        url=url or fake.url(),
    )
    post.tags.set([Tag.objects.create(name=fake.word())])
    return post
