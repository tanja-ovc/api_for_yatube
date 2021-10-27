from rest_framework import filters
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, FollowSerializer
from .serializers import PostSerializer, GroupSerializer


class IsAuthorOrReadOnlyPermission:
    permission_classes = (IsAuthorOrReadOnly,)


class PostViewSet(IsAuthorOrReadOnlyPermission, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(IsAuthorOrReadOnlyPermission, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

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
        serializer.save(post_id=self.kwargs['post_id'],
                        author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class CreateOrGetListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    pass


class FollowViewSet(CreateOrGetListViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """
        Returns a list of all subscriptions of the current user.
        """
        queryset = Follow.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
