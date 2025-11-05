import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.get_api200_response import GetApi200Response  # noqa: E501
from openapi_server.models.get_index200_response import GetIndex200Response  # noqa: E501
from openapi_server import util


def get_api():  # noqa: E501
    """get_api

     # noqa: E501


    :rtype: Union[GetApi200Response, Tuple[GetApi200Response, int], Tuple[GetApi200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_index():  # noqa: E501
    """Health check endpoint

     # noqa: E501


    :rtype: Union[GetIndex200Response, Tuple[GetIndex200Response, int], Tuple[GetIndex200Response, int, Dict[str, str]]
    """
    return 'do some magic!'
