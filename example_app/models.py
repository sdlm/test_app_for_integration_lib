import textwrap

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Tag(models.Model):
    name = models.CharField(max_length=128)


class Post(models.Model):
    title = models.CharField(max_length=512)
    text = models.TextField()
    author = models.ForeignKey(User, related_name='posts', on_delete=CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags')
    url = models.CharField(max_length=512, unique=True)
    created = models.DateField(null=True)

    @property
    def short_title(self):
        return textwrap.shorten(self.title, width=15, placeholder='...')

    def __str__(self):
        return f'(Post: id={self.pk}, title={self.short_title})'
