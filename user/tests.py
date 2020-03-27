from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from util.test_utils import gen_random_email, gen_random_string
from .models import CustomUser


class TestRegistration(APITestCase):

    def setUp(self):
        self.url = reverse('register-list')
        self.email = gen_random_email()
        self.password = self.password2 = gen_random_string(10)
        self.data = {'email': self.email,
                     'password': self.password,
                     'password2': self.password2}

    @patch('user.models.clearbit.Enrichment.find')
    @patch('user.serializers.RegisterCustomUserSerializer.validate_email')
    def test_create_account(self, mock_validate_email, mock_clearbit_enrichment):
        mock_validate_email.return_value = self.email
        mock_clearbit_enrichment.return_value = None
        response = self.client.post(self.url, self.data, frormat='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email=self.email).exists())

    @patch('user.models.clearbit.Enrichment.find')
    @patch('user.serializers.RegisterCustomUserSerializer.validate_email')
    def test_create_account_errors(self, mock_validate_email, mock_clearbit_enrichment):
        mock_validate_email.return_value = self.email
        mock_clearbit_enrichment.return_value = None
        response = self.client.post(self.url, {}, frormat='json')
        errors = {'email': ['This field is required.'],
                  'password': ['This field is required.'],
                  'password2': ['This field is required.']}
        self.assertEqual(response.json(), errors)
