import unittest

from flask import json

from openapi_server.models.get_api200_response import GetApi200Response  # noqa: E501
from openapi_server.models.get_index200_response import GetIndex200Response  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_api(self):
        """Test case for get_api

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_index(self):
        """Test case for get_index

        Health check endpoint
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
