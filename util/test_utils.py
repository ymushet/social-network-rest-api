import random
import string
from unittest.mock import patch

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from post.models import Post, Like
from user.models import CustomUser

METHOD_GET = 'GET'
METHOD_PUT = 'PUT'
METHOD_PATCH = 'PATCH'
METHOD_DELETE = 'DELETE'
METHOD_POST = 'POST'


def gen_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def gen_random_email():
    return gen_random_string(10) + '@mail.com'


def create_random_user():
    email = gen_random_email()
    with patch('user.models.clearbit.Enrichment.find') as cl:
        cl.return_value = None
        user = CustomUser.objects.create(email=email)
    return user


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


def create_random_post(author_id=None):
    if author_id is None:
        author_id = create_random_user().id
    return Post.objects.create(author_id=author_id,
                               content=gen_random_string(10))


def create_random_like(post_id=None):
    user = create_random_user()
    if post_id is None:
        post_id = create_random_post().id

    return Like.objects.create(user=user, post_id=post_id)


def skip_if_not_allowed(method):
    def decorator(f):
        def wrapper(self, *args, **kwargs):
            if method not in self.RESPONSE_CODES.keys():
                self.skipTest('Method not allowed')
            else:
                f(self, *args, **kwargs)

        return wrapper

    return decorator


class BaseListViewTest(APITestCase):
    URL = 'override me'
    RESPONSE_CODES = {'method': 'response code'}
    # create dict with serializers classes
    SERIALIZERS_DICT = {'override with request_method': 'and serializer_class'}
    POST_DATA = {}
    GET_DATA = {}
    OBJECT_CLASS = None
    OBJECT = None
    CONTEXT = {}

    @classmethod
    def setUpTestData(cls):
        """Load initial data for the TestCase."""
        cls.base_user = create_random_user()
        cls._access_token, cls._refresh_token = get_tokens_for_user(cls.base_user)

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self._access_token)

    @skip_if_not_allowed(METHOD_GET)
    def test_get(self):
        response = self.client.get(self.URL, self.GET_DATA)
        serializer_class = self.SERIALIZERS_DICT[METHOD_GET]
        queryset = self.OBJECT_CLASS.objects.filter(id=self.OBJECT.id)
        serializer = serializer_class(queryset, many=True, context=self.CONTEXT)
        self.assertEqual(response.status_code, self.RESPONSE_CODES.get(METHOD_GET))
        self.assertEqual(response.json(), serializer.data)

    @skip_if_not_allowed(METHOD_POST)
    def test_post(self):
        response = self.client.post(self.URL, self.POST_DATA)
        id = response.json().get('id')
        self.assertEqual(response.status_code, self.RESPONSE_CODES.get(METHOD_POST))
        self.assertTrue(self.OBJECT_CLASS.objects.filter(id=id).exists())


class BaseDetailViewTest(APITestCase):
    URL = 'override me'
    RESPONSE_CODES = {'override': 'me'}
    # create dict with serializers classes
    SERIALIZERS_DICT = {'request_method': 'serializer_class'}
    PATCH_DATA = {}
    PUT_DATA = {}
    GET_DATA = {}
    OBJECT_CLASS = None
    OBJECT = None
    CONTEXT = {}

    @classmethod
    def setUpTestData(cls):
        """Load initial data for the TestCase."""
        cls.base_user = create_random_user()
        cls._access_token, cls._refresh_token = get_tokens_for_user(cls.base_user)

    def setUp(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self._access_token)

    @skip_if_not_allowed(METHOD_GET)
    def test_get(self):
        response = self.client.get(self.URL,
                                   data=self.GET_DATA)
        serializer_class = self.SERIALIZERS_DICT[METHOD_GET]
        serializer = serializer_class(self.OBJECT, context=self.CONTEXT)
        self.assertEqual(response.status_code, self.RESPONSE_CODES.get(METHOD_GET))
        self.assertEqual(response.json(), serializer.data)

    @skip_if_not_allowed(METHOD_PATCH)
    def test_put(self):
        response = self.client.patch(self.URL, self.PUT_DATA)
        self.OBJECT.refresh_from_db()
        serializer_class = self.SERIALIZERS_DICT[METHOD_PUT]
        serializer = serializer_class(self.OBJECT, context=self.CONTEXT)
        self.assertEqual(response.status_code, self.RESPONSE_CODES.get(METHOD_PUT))
        self.assertEqual(response.json(), serializer.data)

    @skip_if_not_allowed(METHOD_PUT)
    def test_patch(self):
        for k, v in self.PATCH_DATA.items():
            response = self.client.patch(self.URL, {k: v})
            self.assertEqual(response.json().get(k), v)
            self.assertEqual(response.status_code, self.RESPONSE_CODES.get(METHOD_PATCH))

    @skip_if_not_allowed(METHOD_DELETE)
    def test_delete(self):
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, self.RESPONSE_CODES.get(METHOD_DELETE))
        self.assertFalse(self.OBJECT_CLASS.objects.filter(id=self.OBJECT.id).exists())
