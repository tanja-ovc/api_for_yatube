from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post

from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.StringRelatedField(
        read_only=True, default='0'
    )

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Подписка уже существует.'
            )
        ]

    def validate_following(self, value):
        request = self.context['request']
        if value.id == request.user.id:
            raise serializers.ValidationError(
                'Подписка на самого себя невозможна.'
            )
        return value
