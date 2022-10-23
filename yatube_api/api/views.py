from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer,
                          FollowSerializer,
                          GroupSerializer,
                          PostSerializer)
from posts.models import Group, Post


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
    search_fields = ('following__username', 'user__username',)

    def get_queryset(self):
        user = self.request.user
        return user.follow.all()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class GroupAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class PostAPIView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
