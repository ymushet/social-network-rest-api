import logging

import requests
from django.core.exceptions import ValidationError
from rest_framework import status

from socialnetwork import settings

logging.getLogger(__name__)


class EmailVerifier:
    """"
    API to call hunter.co to verify given email
    Validation performed only with USE_EMAIL_VERIFIER=True
    """
    url = settings.HUNTER_API_EMAIL_VERIFIER_URL
    api_key = settings.HUNTER_API_KEY
    USE_EMAIL_VERIFIER = settings.USE_EMAIL_VERIFIER
    _is_valid = None
    errors = None
    data = {}
    raise_exception = False
    status_code = None

    def __init__(self, email):
        self.email = email

    @classmethod
    def _verify(cls, email):
        params = {'email': email,
                  'api_key': cls.api_key}
        resp = requests.get(cls.url, params=params)
        data = resp.json()
        cls._is_valid = False
        cls.status_code = resp.status_code
        if resp.status_code == status.HTTP_200_OK:
            if data['data']['result'] in ['deliverable', ]:
                cls._is_valid = True
            logging.info('[EMAIL VERIFIER]: Email {} verified result: {}'.format(email, data))
            cls.data = data.get('data')
        elif resp.status_code == status.HTTP_400_BAD_REQUEST:
            cls.errors = {'errors': data.get('errors')}
            logging.error('[ERROR]: Hunter bad request with email {} '
                          '[{}]'.format(email, cls.errors))
            if cls.raise_exception:
                raise ValidationError(cls.errors)
        else:
            cls.data = data.get('data')
            logging.error('[ERROR]: Hunter validation error with email {} '
                          '[{}]'.format(email, cls.data))

    def is_valid(self, raise_exception=None) -> bool:
        if self.USE_EMAIL_VERIFIER is False:
            return True
        self.raise_exception = raise_exception
        if self._is_valid is None:
            self._verify(self.email)
        return self._is_valid
