import connexion
from typing import Dict
from typing import Tuple
from typing import Union

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
from openapi_server import util


def delete_api_users_by_id(id):  # noqa: E501
    """Delete a user

     # noqa: E501

    :param id: 
    :type id: dict | bytes

    :rtype: Union[DeleteApiUsersById200Response, Tuple[DeleteApiUsersById200Response, int], Tuple[DeleteApiUsersById200Response, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        id =  GetApiUsersByIdIdParameter.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_api_users():  # noqa: E501
    """Get all users (Admin Only)

     # noqa: E501


    :rtype: Union[GetApiUsersOffset200Response, Tuple[GetApiUsersOffset200Response, int], Tuple[GetApiUsersOffset200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_api_users_by_id(id):  # noqa: E501
    """Get user by ID

     # noqa: E501

    :param id: 
    :type id: dict | bytes

    :rtype: Union[PostApiUsers201Response, Tuple[PostApiUsers201Response, int], Tuple[PostApiUsers201Response, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        id =  GetApiUsersByIdIdParameter.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_api_users_cursor(cursor, limit):  # noqa: E501
    """User pagination cursor-based

     # noqa: E501

    :param cursor: 
    :type cursor: 
    :param limit: 
    :type limit: 

    :rtype: Union[GetApiUsersOffset200Response, Tuple[GetApiUsersOffset200Response, int], Tuple[GetApiUsersOffset200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_api_users_me():  # noqa: E501
    """Get current authenticated user

     # noqa: E501


    :rtype: Union[GetApiUsersMe200Response, Tuple[GetApiUsersMe200Response, int], Tuple[GetApiUsersMe200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_api_users_offset(offset, limit):  # noqa: E501
    """User pagination offset/limit

     # noqa: E501

    :param offset: 
    :type offset: 
    :param limit: 
    :type limit: 

    :rtype: Union[GetApiUsersOffset200Response, Tuple[GetApiUsersOffset200Response, int], Tuple[GetApiUsersOffset200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_api_users_page(page, per_page):  # noqa: E501
    """User pagination page-based

     # noqa: E501

    :param page: 
    :type page: 
    :param per_page: 
    :type per_page: 

    :rtype: Union[GetApiUsersOffset200Response, Tuple[GetApiUsersOffset200Response, int], Tuple[GetApiUsersOffset200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def patch_api_users_by_id(id, body):  # noqa: E501
    """Partially update a user account information

     # noqa: E501

    :param id: 
    :type id: dict | bytes
    :param patch_api_users_by_id_request: 
    :type patch_api_users_by_id_request: dict | bytes

    :rtype: Union[PostApiUsers201Response, Tuple[PostApiUsers201Response, int], Tuple[PostApiUsers201Response, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        id =  GetApiUsersByIdIdParameter.from_dict(connexion.request.get_json())  # noqa: E501
    patch_api_users_by_id_request = body
    if connexion.request.is_json:
        patch_api_users_by_id_request = PatchApiUsersByIdRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def patch_api_users_by_id_addresses_by_address_id(id, address_id, body):  # noqa: E501
    """Update an existing address for a user

     # noqa: E501

    :param id: 
    :type id: dict | bytes
    :param address_id: 
    :type address_id: dict | bytes
    :param patch_api_users_by_id_addresses_by_address_id_request: 
    :type patch_api_users_by_id_addresses_by_address_id_request: dict | bytes

    :rtype: Union[PostApiUsersByIdAddresses201Response, Tuple[PostApiUsersByIdAddresses201Response, int], Tuple[PostApiUsersByIdAddresses201Response, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        id =  GetApiUsersByIdIdParameter.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        address_id =  GetApiUsersByIdIdParameter.from_dict(connexion.request.get_json())  # noqa: E501
    patch_api_users_by_id_addresses_by_address_id_request = body
    if connexion.request.is_json:
        patch_api_users_by_id_addresses_by_address_id_request = PatchApiUsersByIdAddressesByAddressIdRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def post_api_users(body):  # noqa: E501
    """Register a new user

     # noqa: E501

    :param post_api_users_request: 
    :type post_api_users_request: dict | bytes

    :rtype: Union[PostApiUsers201Response, Tuple[PostApiUsers201Response, int], Tuple[PostApiUsers201Response, int, Dict[str, str]]
    """
    post_api_users_request = body
    if connexion.request.is_json:
        post_api_users_request = PostApiUsersRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def post_api_users_by_id_addresses(id, body):  # noqa: E501
    """Add a new address for a user

     # noqa: E501

    :param id: 
    :type id: dict | bytes
    :param post_api_users_by_id_addresses_request: 
    :type post_api_users_by_id_addresses_request: dict | bytes

    :rtype: Union[PostApiUsersByIdAddresses201Response, Tuple[PostApiUsersByIdAddresses201Response, int], Tuple[PostApiUsersByIdAddresses201Response, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        id =  GetApiUsersByIdIdParameter.from_dict(connexion.request.get_json())  # noqa: E501
    post_api_users_by_id_addresses_request = body
    if connexion.request.is_json:
        post_api_users_by_id_addresses_request = PostApiUsersByIdAddressesRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
