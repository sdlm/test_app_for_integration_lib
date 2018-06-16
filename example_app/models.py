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
    url = models.CharField(max_length=512)
    created = models.DateField(null=True)
