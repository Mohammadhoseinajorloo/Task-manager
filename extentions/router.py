import os
from config import ROUTES


class Router:

    def __init__(self):
        pass


    def translate_path(self, path: str) -> str:
        '''
        Translate Path
            This function self.path http.server input and for ROUTES list in config
            file path existes in list generate new path and return for open file read
            and display in browser and web server in localhost.
            ** NOTE:
                configuration ROUTES list in config file and insert routes in web serve in project.
            parameters:
                1. path :(StrPath) -> "/" or "/page"
                    Paths that are usually taken from the object itself
            output:
                path: (StrPath) -> "/templates/index.html"
                Path for render html page in web server
        '''
        global root

        # look up routes and get root directory
        for patt, rootDir in ROUTES:
            if path.startswith(patt):
                path = path[:len(patt)]
                root = rootDir

        # new path
        return os.path.join(path, root)