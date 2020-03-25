from rest_framework import viewsets
from rest_framework import permissions
from .models import Post
from .serializers import PostSerializer
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    """"
    Viewset for Post model
    """
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        kwargs['author'] = request.user
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        kwargs['author'] = request.user
        return super().update(request, *args, **kwargs)
