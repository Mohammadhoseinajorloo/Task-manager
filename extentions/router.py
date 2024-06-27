"""
In This file we trying handelign routing system in website.
"""
# import build in library python
import os
import re
from typing import (Sequence, Callable)

# import extentions module
from datastructure import (Method, ResponseConfig)


class Router:

    def __init__(self):
        self.listeners_dic = {}


    def add_request_listener(self, path:str, methods:Sequence[Method], listener:Callable, response_config:ResponseConfig=None):
        """add action for request methde

        Args:
            path (str): _description_
            methods (Sequence[Method]): _description_
            listener (Callable): _description_
            response_config (ResponseConfig, optional): _description_. Defaults to None.
        """
        path_params = re.findall("([^\/]+)", path)
        for parm in path_params:
            path = path.replace(r"([\S]+)", parm)
        if len(path_params) != 0:
            path = re.compile(path)
        if path in self.listeners_dic:
            for method in methods:
                self.listeners_dic[path][method] = listener, path_params, response_config
        else:
            self.listeners_dic[path] = {method: (listener, path_params, response_config) for method in methods}
    
    
    def route(self, path, methods=None, response_config=None):
        """This function is supposed to be used as a decoratior for routing our website.

        Args:
            path (_type_): _description_
            methods (_type_, optional): _description_. Defaults to None.
            response_config (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        if methods is None:
            methods = [m for m in Method]

        def converter(listener):
            self.add_request_listener(path, methods, listener, response_config)
            return listener

        return converter


    def get (self, path, response_config=None):
        """routing for get methode

        Args:
            path (_type_): _description_
            response_config (_type_, optional): _description_. Defaults to None.
        """
        return self.route(path, [Method.GET], response_config)
    

    def post(self, path, response_config=None):
        """routing for post method

        Args:
            path (_type_): _description_
            response_config (_type_, optional): _description_. Defaults to None.
        """
        return self.route(path, [Method.POST], response_config)


    def __repr__(self) -> str:
        """represent

        Returns:
            str: _description_
        """
        str = ""
        str += f"{self.listeners_dic}"
        return str