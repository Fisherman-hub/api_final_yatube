from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from .permissions import ReadOnly, IsOwnerOrReadOnly
from .serializers import CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
from posts.models import Follow, Group, Post


class CommentAPIView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def get_queryset(self):
        pk = self.kwargs['post_id']
        post = get_object_or_404(Post, id=pk)
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(
            author=self.request.user,
            post=post
        )


class FollowAPIView(viewsets.ModelViewSet):

    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following',)

    def get_queryset(self):
        user = self.request.user
        return user.follow.all()

    def perform_create(self, serializer):
        serializer.save(
            following=self.request.user
        )


class GroupAPIView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def create(self, serializer):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PostAPIView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
