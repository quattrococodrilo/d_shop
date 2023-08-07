import sys
from pprint import pprint
from typing import Any

from django.test import Client, RequestFactory
from django.test.testcases import unittest
from faker import Faker

# from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import AbstractUser, User
# from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 # force_authenticate)


def dd(printable: Any) -> None:
    pprint(printable)
    # sys.exit()


class FlyTestCaseBase:
    def setUp(self) -> None:
        super().setUp()
        self.fake: Faker = Faker()

    def fake_add_provider(self, provider: str) -> None:
        self.fake.add_provider(provider)


class FlyTestCase(FlyTestCaseBase, unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.request_factory: RequestFactory = RequestFactory()


# class FlyTestCaseAPI(FlyTestCaseBase, APITestCase):
#     def setUp(self) -> None:
#         super().setUp()
#         self.client = APIClient()
#         self.request_factory = APIRequestFactory()

#     def force_authenticate(
#         self, request, user: AbstractBaseUser | AbstractUser | User, token: str = ""
#     ):
#         if token:
#             return force_authenticate(request=request, user=user, token=token)
#         return force_authenticate(request=request, user=user)
