import textwrap

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Tag(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'(Tag: id={self.pk}, name={self.name})'


class Post(models.Model):
    title = models.CharField(max_length=512)
    text = models.TextField()
    author = models.ForeignKey(User, related_name='posts', on_delete=CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags')
    url = models.CharField(max_length=512, unique=True)
    hash = models.CharField(max_length=512,
                            unique=True,
                            default=None,
                            blank=True,
                            null=True)  # only for test second unique field
    created = models.DateField(null=True)

    @property
    def short_title(self):
        return textwrap.shorten(self.title, width=15, placeholder='...')

    def __str__(self):
        return f'(Post: id={self.pk}, title={self.short_title})'
