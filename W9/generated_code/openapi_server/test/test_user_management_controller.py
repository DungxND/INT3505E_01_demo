import unittest

from flask import json

from openapi_server.models.delete_api_users_by_id200_response import DeleteApiUsersById200Response  # noqa: E501
from openapi_server.models.get_api_users_by_id_id_parameter import GetApiUsersByIdIdParameter  # noqa: E501
from openapi_server.models.get_api_users_me200_response import GetApiUsersMe200Response  # noqa: E501
from openapi_server.models.get_api_users_offset200_response import GetApiUsersOffset200Response  # noqa: E501
from openapi_server.models.patch_api_users_by_id_addresses_by_address_id_request import PatchApiUsersByIdAddressesByAddressIdRequest  # noqa: E501
from openapi_server.models.patch_api_users_by_id_request import PatchApiUsersByIdRequest  # noqa: E501
from openapi_server.models.post_api_auth_login401_response import PostApiAuthLogin401Response  # noqa: E501
from openapi_server.models.post_api_users201_response import PostApiUsers201Response  # noqa: E501
from openapi_server.models.post_api_users_by_id_addresses201_response import PostApiUsersByIdAddresses201Response  # noqa: E501
from openapi_server.models.post_api_users_by_id_addresses_request import PostApiUsersByIdAddressesRequest  # noqa: E501
from openapi_server.models.post_api_users_request import PostApiUsersRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestUserManagementController(BaseTestCase):
    """UserManagementController integration test stubs"""

    def test_delete_api_users_by_id(self):
        """Test case for delete_api_users_by_id

        Delete a user
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/users/{id}'.format(id=openapi_server.GetApiUsersByIdIdParameter()),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_api_users(self):
        """Test case for get_api_users

        Get all users (Admin Only)
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/users/',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_api_users_by_id(self):
        """Test case for get_api_users_by_id

        Get user by ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/users/{id}'.format(id=openapi_server.GetApiUsersByIdIdParameter()),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_api_users_cursor(self):
        """Test case for get_api_users_cursor

        User pagination cursor-based
        """
        query_string = [('cursor', 0),
                        ('limit', 10)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/users/cursor',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_api_users_me(self):
        """Test case for get_api_users_me

        Get current authenticated user
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/users/me',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_api_users_offset(self):
        """Test case for get_api_users_offset

        User pagination offset/limit
        """
        query_string = [('offset', 0),
                        ('limit', 10)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/users/offset',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_api_users_page(self):
        """Test case for get_api_users_page

        User pagination page-based
        """
        query_string = [('page', 1),
                        ('per_page', 10)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/users/page',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("Connexion does not support multiple consumes. See https://github.com/zalando/connexion/pull/760")
    def test_patch_api_users_by_id(self):
        """Test case for patch_api_users_by_id

        Partially update a user account information
        """
        patch_api_users_by_id_request = openapi_server.PatchApiUsersByIdRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/users/{id}'.format(id=openapi_server.GetApiUsersByIdIdParameter()),
            method='PATCH',
            headers=headers,
            data=json.dumps(patch_api_users_by_id_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("Connexion does not support multiple consumes. See https://github.com/zalando/connexion/pull/760")
    def test_patch_api_users_by_id_addresses_by_address_id(self):
        """Test case for patch_api_users_by_id_addresses_by_address_id

        Update an existing address for a user
        """
        patch_api_users_by_id_addresses_by_address_id_request = openapi_server.PatchApiUsersByIdAddressesByAddressIdRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/users/{id}/addresses/{address_id}'.format(id=openapi_server.GetApiUsersByIdIdParameter(), address_id=openapi_server.GetApiUsersByIdIdParameter()),
            method='PATCH',
            headers=headers,
            data=json.dumps(patch_api_users_by_id_addresses_by_address_id_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("Connexion does not support multiple consumes. See https://github.com/zalando/connexion/pull/760")
    def test_post_api_users(self):
        """Test case for post_api_users

        Register a new user
        """
        post_api_users_request = openapi_server.PostApiUsersRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/users/',
            method='POST',
            headers=headers,
            data=json.dumps(post_api_users_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("Connexion does not support multiple consumes. See https://github.com/zalando/connexion/pull/760")
    def test_post_api_users_by_id_addresses(self):
        """Test case for post_api_users_by_id_addresses

        Add a new address for a user
        """
        post_api_users_by_id_addresses_request = openapi_server.PostApiUsersByIdAddressesRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/users/{id}/addresses'.format(id=openapi_server.GetApiUsersByIdIdParameter()),
            method='POST',
            headers=headers,
            data=json.dumps(post_api_users_by_id_addresses_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
