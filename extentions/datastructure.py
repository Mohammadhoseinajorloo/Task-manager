"""
In this file we are trying to defin our data stractures specifically.
"""
from enum import Enum


class Method(Enum):
    """Method datastructur

    Args:
        Enum (_type_): _description_
    """
    GET     = 1
    HEAD    = 2
    POST    = 3
    PUT     = 4
    DELETE  = 5
    CONNECT = 6
    OPTIONS = 7
    TRACE   = 8
    PATCH   = 9


class ResponseConfig:
    
    def __init__(self, headers=None, content_type=None):
        """datastructure for controle responses

        Args:
            headers (_type_, optional): _description_. Defaults to None.
            content_type (_type_, optional): _description_. Defaults to None.
        """
        self.headers = dict() if headers is None else headers
        if type(self.headers) != dict:
            raise ValueError("headers must be a dict")
        self.content_type = content_type
        if self.content_type is not None and type(self.content_type) != str:
            raise ValueError("content_type must be a string")
