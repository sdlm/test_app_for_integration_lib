from django.contrib.auth.models import User
from marshmallow import Schema, fields, post_load

from example_app.models import Tag, Post


class EntryUserSchema(Schema):
    name = fields.String(attribute='username')

    @post_load
    def make_object(self, data):
        return User.objects.get_or_create(**data)[0]


class EntryTagSchema(Schema):
    term = fields.String(attribute='name')

    @post_load
    def make_object(self, data):
        return Tag.objects.get_or_create(**data)[0]


class EntrySchema(Schema):
    title = fields.String()
    summary = fields.String(attribute='text')
    link = fields.Url(attribute='url')

    author = fields.Nested(EntryUserSchema)
    tags = fields.Nested(EntryTagSchema, many=True)

    @post_load
    def make_object(self, data):
        qs = Post.objects.filter(url=data['url'])
        instance = qs.first()
        if instance:
            del data['url']
            tags = data.pop('tags')
            instance.tags.set(tags)
            return qs.update(**data)

        tags = data.pop('tags')
        instance = Post.objects.get_or_create(**data)[0]
        instance.tags.set(tags)
        return instance
