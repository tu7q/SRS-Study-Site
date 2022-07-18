# WebApp/MicrosoftAuthentication/tests.py

# Django testing tools
from django.test import TestCase
from django.test import Client

# App settings
# from django.conf import settings
from . import settings as s

# Library to mock the python requests library
from unittest.mock import Mock, patch

# import unittest

# App info to test
from . import utils

import msal

# Create your tests here.
class TestMSAL(TestCase):
    def setUp(self) -> None:
        pass

    def test_login(self) -> None:
        pass

    def test_callback(self) -> None:
        pass

    def test_logout(self) -> None:
        pass

    def test_load_cache(self) -> None:
        client = Client()
        session = client.session
        session[""] = "value"
        session.save()

        cache = utils.load_cache(session)
        # test cache properties

    def test_save_cache(self) -> None:
        client = Client()
        session = client.session
        session[""] = "value"
        session.save()

        cache = msal.SerializableTokenCache()

        utils.save_cache(session, cache=cache)
        # test session cache stuff

    def test_clear_cache(self) -> None:
        client = Client()
        session = client.session
        session[""] = "value"
        session.save()

        utils.clear_cache(session)

    def test_get_msal_app(self) -> None:
        pass
        # utils.get_msal_app(None)

    def test_get_sign_in_flow(self) -> None:
        pass
        # flow = utils.get_sign_in_flow()

    def test_get_token_from_code(self) -> None:
        # client = Client()
        # utils.get_token_from_code()
        pass

    def test_get_user(self) -> None:
        access_token = "FAKE_ACCESS_TOKEN"
        token = {"access_token": access_token}

        # Note: from requests import status_codes != utils.requests.status_codes
        # Not fun.

        # normal response
        with patch("MicrosoftAuthentication.utils.requests") as mock_requests:
            mock_requests.get.return_value = mock_response = Mock()
            mock_response.status_code = utils.requests.status_codes.codes.ok
            mock_response.json.return_value = {"Fake Data": None}

            user = utils.get_user(token)

            self.assertNotEqual(user, {})
            mock_requests.get.assert_called_once_with(
                url=f"{s.GRAPH_URL}/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

        # bad request
        with patch("MicrosoftAuthentication.utils.requests") as mock_requests:
            mock_requests.get.return_value = mock_response = Mock()
            mock_response.status_code = utils.requests.status_codes.codes.server_error
            mock_response.json.return_value = {}

            user = utils.get_user(token)

            self.assertEqual(user, {})
            mock_requests.get.assert_called_once_with(
                url=f"{s.GRAPH_URL}/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

    def test_store_user(self) -> None:
        client = Client()
        session = client.session
        session[""] = "value"
        session.save()

        user = {}

        utils.store_user(session, user)

    def test_logout_url(self) -> None:
        # not testable
        pass

    def test_is_authenticated(self) -> None:
        client = Client()
        session = client.session
        session[""] = "value"
        session.save()

        utils.is_authenticated(session)

    def tearDown(self) -> None:
        pass
