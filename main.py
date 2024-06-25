from database import DataBase
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from config import ROUTES
import bcrypt
import os



class HttpHandler(BaseHTTPRequestHandler):

    def set_headers(self) -> None:
        self.send_header(keyword="Content-type", value="text/css")
        self.end_headers()
        return 


    def create_salt(self) -> str:
        return bcrypt.gensalt(rounds=12)


    def hash_pass(self, password:str):
        salt = self.create_salt()
        return bcrypt.hashpw(password, salt)


    def translate_path(self, path:str) -> str:
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

       
    def do_GET(self):
        global root

        path = self.translate_path(self.path)
    
        # Set header with content type
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Open the file, read bytes, serve
        with open(path[1:], 'rb') as file:
            self.wfile.write(file.read())


    def do_POST(self):

        if self.path == "/register":
            self.send_response(200)
            self.set_headers()

            content_lenght = int(self.headers["Content-Length"])
            post_data_bytes = self.rfile.read(content_lenght)

            post_data_str = post_data_bytes.decode("UTF-8")

            post_data_split = post_data_str.split("&")

            post_dict = {}

            for item in post_data_split:
                key = item.split("=")[0]
                value = item.split("=")[1]
                post_dict[key] = value


            encode_password = post_dict["password"].encode()
            hashed_password = self.hash_pass(encode_password)
            decode_password = hashed_password.decode()
            post_dict["password"] = decode_password

            columns_dict = {"id": "INT  PRIMARY KEY NOT NULL AUTO_INCREMENT",
                            "name": "VARCHAR(64)",
                            "password": "VARCHAR(64)"}

            db = DataBase()
            db.create(table="users", col=columns_dict)
            db.insert(table="users", values=post_dict)

            response = BytesIO()
            response.write(b"done")
            self.wfile.write(response.getvalue())



def run(server_class=HTTPServer, handler_class=HttpHandler, port=8001 ):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
    