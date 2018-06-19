from django.contrib.auth.models import User
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from example_app.models import Tag, Post


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ('name', )


class TagSerializer(serializers.ModelSerializer):
    term = serializers.CharField(source='name')

    class Meta:
        model = Tag
        fields = ('term', )


class PostSerializer(WritableNestedModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True, required=False)
    title = serializers.CharField()
    summary = serializers.CharField(source='text')
    link = serializers.URLField(source='url')

    class Meta:
        model = Post
        fields = ('author', 'tags', 'title', 'summary', 'link', )

    def create(self, validated_data):
        username = validated_data['author']['username']
        user = User.objects.filter(username=username).first()
        if user:
            self.initial_data['author']['pk'] = user.pk
        return super().create(validated_data)
