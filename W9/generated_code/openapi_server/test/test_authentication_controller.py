import unittest

from flask import json

from openapi_server.models.post_api_auth_login200_response import PostApiAuthLogin200Response  # noqa: E501
from openapi_server.models.post_api_auth_login401_response import PostApiAuthLogin401Response  # noqa: E501
from openapi_server.models.post_api_auth_login_request import PostApiAuthLoginRequest  # noqa: E501
from openapi_server.models.post_api_auth_logout200_response import PostApiAuthLogout200Response  # noqa: E501
from openapi_server.test import BaseTestCase


class TestAuthenticationController(BaseTestCase):
    """AuthenticationController integration test stubs"""

    @unittest.skip("Connexion does not support multiple consumes. See https://github.com/zalando/connexion/pull/760")
    def test_post_api_auth_login(self):
        """Test case for post_api_auth_login

        Log in a user
        """
        post_api_auth_login_request = openapi_server.PostApiAuthLoginRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/auth/login',
            method='POST',
            headers=headers,
            data=json.dumps(post_api_auth_login_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_api_auth_logout(self):
        """Test case for post_api_auth_logout

        Log out the current user
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/auth/logout',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
