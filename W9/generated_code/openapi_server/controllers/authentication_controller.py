import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.post_api_auth_login200_response import PostApiAuthLogin200Response  # noqa: E501
from openapi_server.models.post_api_auth_login401_response import PostApiAuthLogin401Response  # noqa: E501
from openapi_server.models.post_api_auth_login_request import PostApiAuthLoginRequest  # noqa: E501
from openapi_server.models.post_api_auth_logout200_response import PostApiAuthLogout200Response  # noqa: E501
from openapi_server import util


def post_api_auth_login(body):  # noqa: E501
    """Log in a user

     # noqa: E501

    :param post_api_auth_login_request: 
    :type post_api_auth_login_request: dict | bytes

    :rtype: Union[PostApiAuthLogin200Response, Tuple[PostApiAuthLogin200Response, int], Tuple[PostApiAuthLogin200Response, int, Dict[str, str]]
    """
    post_api_auth_login_request = body
    if connexion.request.is_json:
        post_api_auth_login_request = PostApiAuthLoginRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def post_api_auth_logout():  # noqa: E501
    """Log out the current user

     # noqa: E501


    :rtype: Union[PostApiAuthLogout200Response, Tuple[PostApiAuthLogout200Response, int], Tuple[PostApiAuthLogout200Response, int, Dict[str, str]]
    """
    return 'do some magic!'
