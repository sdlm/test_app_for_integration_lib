from django.contrib.auth.models import User
from rest_framework import serializers

from example_app.models import Tag, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', )


class TagSerializer(serializers.ModelSerializer):
    term = serializers.CharField(source='name')

    class Meta:
        model = Tag
        fields = ('term', )


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    tags = TagSerializer(many=True)
    title = serializers.CharField()
    summary = serializers.CharField(source='text')
    link = serializers.URLField(source='url')

    class Meta:
        model = Post
        fields = ('author', 'tags', 'title', 'summary', 'link', )

    def create_tags(self, tags_data):
        return [Tag.objects.get_or_create(**tag_data)[0] for tag_data in tags_data]

    def get_or_create_author(self, username):
        return User.objects.get_or_create(username=username)[0]

    def create(self, validated_data) -> Post:
        tags = self.create_tags(validated_data['tags'])
        del validated_data['tags']

        validated_data['author'] = self.get_or_create_author(username=validated_data['author'])

        instance = Post.objects.create(**validated_data)

        instance.tags.set(tags)

        return instance
