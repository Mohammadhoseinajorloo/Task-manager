from database import DataBase
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import bcrypt



class HttpHandler(BaseHTTPRequestHandler):

    def set_headers(self):
        self.send_header(keyword="countent-type", value="text/css")
        self.end_headers()


    def create_salt(self) -> str:
        return bcrypt.gensalt(rounds=12)


    def hash_pass(self, password:str):
        salt = self.create_salt()
        return bcrypt.hashpw(password, salt)


    def do_GET(self):

        if self.path == "/":
            self.path = "/templates/index.html"
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
            self.set_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))


        elif self.path == "/Register":
            self.path = "/templates/register.html"
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
            self.set_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))

        else:
            self.send_error(404)


    def do_POST(self):

        if self.path == "/Register":
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

            post_dict["password"] = self.hash_pass(post_dict["password"].encode())
            post_dict["password"] = post_dict["password"].decode()

            columns_dict = {"id": "INT  PRIMARY KEY NOT NULL AUTO_INCREMENT",
                            "name": "VARCHAR(64)",
                            "password": "VARCHAR(64)"}

            db = DataBase()
            db.create(table="users", col=columns_dict)
            db.insert(table="users", values=post_dict)

            response = BytesIO()
            response.write(b"done")
            self.wfile.write(response.getvalue())


if __name__ == "__main__":
     httpd = HTTPServer(("localhost", 8000), HttpHandler)
     httpd.serve_forever()
