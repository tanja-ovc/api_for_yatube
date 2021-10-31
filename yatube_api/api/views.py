from posts.models import Comment, Group, Post
from rest_framework import filters, permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from .mixins import CreateOrGetListMixin
from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        """
        Returns either a list of all comments to a particular
        post or a certain comment to a particular post.
        """
        post_id = self.kwargs['post_id']

        get_object_or_404(Post, id=post_id)

        queryset = Comment.objects.filter(post__id=post_id)
        comment_id = self.request.query_params.get('comment_id')
        if comment_id is not None:
            queryset = queryset.filter(comment__id=comment_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post_id=self.kwargs['post_id'])


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class FollowViewSet(CreateOrGetListMixin):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """
        Returns a list of all subscriptions of the current user.
        """
        current_user = self.request.user
        queryset = current_user.follower.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
