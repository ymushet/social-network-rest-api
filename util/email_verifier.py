import requests
from django.core.exceptions import ValidationError
from rest_framework import status

from socialnetwork import settings


class EmailVerifier:
    """"
    API to call hunter.co to verify given email
    """
    url = settings.HUNTER_API_EMAIL_VERIFIER_URL
    api_key = settings.HUNTER_API_KEY
    _is_valid = None
    errors = None
    data = None
    raise_exception = False

    def __init__(self, email):
        self.email = email

    @classmethod
    def _verify(cls, email):
        params = {'email': email,
                  'api_key': cls.api_key}
        resp = requests.get(cls.url, params=params)
        data = resp.json()

        if resp.status_code == status.HTTP_200_OK:
            if data['data']['result'] in ['deliverable', ]:
                cls._is_valid = True
            cls.data = data.get('data')
        elif resp.status_code == status.HTTP_400_BAD_REQUEST:
            cls._is_valid = False
            cls.errors = {'errors': data.get('errors')}
            if cls.raise_exception:
                raise ValidationError(cls.errors)
        else:
            cls.data = data.get('data')
            cls._is_valid = False

    def is_valid(self, raise_exception=None) -> bool:
        self.raise_exception = raise_exception
        if self._is_valid is None:
            self._verify(self.email)
        return self._is_valid
