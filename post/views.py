from django.core.exceptions import ValidationError
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Post, Like
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, LikeSerializer


class PostViewSet(viewsets.ModelViewSet):
    """"
    Viewset for Post model
    """
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly
    ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(methods=['POST'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated],
            url_path='like',
            url_name='like')
    def like(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound({'post': 'does not exist'})
        like = post.like_post(user_id=request.user.id)
        serializer = LikeSerializer(like)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    @action(methods=['PATCH'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated],
            url_path='unlike',
            url_name='unlike')
    def unlike(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound({'post': 'does not exist'})
        post.unlike_post(user_id=request.user.id)
        return Response(status=status.HTTP_200_OK)


class LikeListView(generics.ListAPIView):
    """"
    Return List of Likes of a specified post.
    (only liked=True is returned)
    """
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        if post_id is None:
            raise ValidationError({'post_id': 'parameter required'})
        return Like.objects.filter(post_id=post_id)
