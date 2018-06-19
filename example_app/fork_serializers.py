from django.contrib.auth.models import User
from marshmallow import fields

from example_app.models import Tag, Post
from marshmallow_fork.schema import DjangoModelSchema


class DjangoUserSchema(DjangoModelSchema):
    name = fields.String(attribute='username')

    class Meta:
        model = User


class DjangoTagSchema(DjangoModelSchema):
    term = fields.String(attribute='name')

    class Meta:
        model = Tag


class DjangoEntrySchema(DjangoModelSchema):
    title = fields.String()
    summary = fields.String(attribute='text')
    link = fields.Url(attribute='url')

    author = fields.Nested(DjangoUserSchema)
    tags = fields.Nested(DjangoTagSchema, many=True)

    class Meta:
        model = Post
