from django.http import HttpRequest
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request

from util.test_utils import (BaseListViewTest, BaseDetailViewTest,
                             METHOD_GET, METHOD_POST, METHOD_PATCH, METHOD_PUT,
                             METHOD_DELETE, create_random_post, create_random_like,
                             gen_random_string)
from .models import Like, Post
from .serializers import LikeSerializer, PostSerializer


class LikeListViewTest(BaseListViewTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.URL = reverse('like-list')
        cls.RESPONSE_CODES = {
            METHOD_GET: status.HTTP_200_OK
        }
        cls.SERIALIZERS_DICT = {
            METHOD_GET: LikeSerializer
        }
        cls.GET_DATA = {
            'post_id': create_random_post().id,
        }
        cls.OBJECT_CLASS = Like
        cls.OBJECT = create_random_like(post_id=cls.GET_DATA['post_id'])


class PostListView(BaseListViewTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.URL = reverse('post-list')
        cls.RESPONSE_CODES = {
            METHOD_GET: status.HTTP_200_OK,
            METHOD_POST: status.HTTP_201_CREATED
        }
        cls.SERIALIZERS_DICT = {
            METHOD_GET: PostSerializer,
            METHOD_POST: PostSerializer
        }
        cls.OBJECT_CLASS = Post
        cls.OBJECT = create_random_post()
        cls.POST_DATA = {
            'content': gen_random_string(10)
        }


class PostDetailView(BaseDetailViewTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.OBJECT_CLASS = Post
        cls.OBJECT = create_random_post(author_id=cls.base_user.id)
        cls.URL = reverse('post-detail', kwargs={'pk': cls.OBJECT.id})
        cls.RESPONSE_CODES = {
            METHOD_GET: status.HTTP_200_OK,
            METHOD_PATCH: status.HTTP_200_OK,
            METHOD_PUT: status.HTTP_200_OK,
            METHOD_DELETE: status.HTTP_204_NO_CONTENT
        }
        cls.SERIALIZERS_DICT = {
            METHOD_GET: PostSerializer,
            METHOD_PATCH: PostSerializer,
            METHOD_PUT: PostSerializer,
            METHOD_DELETE: PostSerializer,
        }
        cls.PUT_DATA = {
            'content': gen_random_string(10)
        }
        cls.PATCH_DATA = {
            'content': gen_random_string(10)
        }
        request = HttpRequest()
        request.user = cls.base_user
        cls.CONTEXT = {'request': Request(request)}

    def test_patch(self):
        super().test_patch()
        self.OBJECT.refresh_from_db()
        self.assertTrue(self.OBJECT.edited)

    def test_like_action(self):
        self.OBJECT = create_random_post(author_id=self.base_user.id)
        self.URL = reverse('post-like', kwargs={'pk': self.OBJECT.id})
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(
            user=self.base_user, post=self.OBJECT
        ).exists())

    def test_unlike_action(self):
        self.OBJECT = create_random_post(author_id=self.base_user.id)
        like = Like.objects.create(user=self.base_user, post=self.OBJECT)
        self.URL = reverse('post-unlike', kwargs={'pk': self.OBJECT.id})
        response = self.client.patch(self.URL)
        like.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(like.liked)
