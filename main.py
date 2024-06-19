from database import DataBase
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import bcrypt



class HttpHandler(BaseHTTPRequestHandler):

    def set_headers(self):
        self.send_header(keyword="countent-type", value="application/json")
        self.end_headers()


    def create_salt(self) -> str:
        return bcrypt.gensalt(rounds=12)


    def hash_pass(self, password:str):
        salt = self.create_salt()
        return bcrypt.hashpw(password, salt)


    def do_GET(self):

        if self.path == "/":
            self.send_response(200)
            self.set_headers()
            response = BytesIO()
            response.write(b"home")
            self.wfile.write(response.getvalue())

        elif self.path == "/Regester":
            self.send_response(200)
            self.set_headers()
            response = BytesIO()
            response.write(b"regester")
            self.wfile.write(response.getvalue())

        else:
            self.send_error(404)


    def do_POST(self):

        if self.path == "/Regester":
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

            db = DataBase(db_name="users.db")
            db.create(table="users", col=post_dict)
            db.insert(table="users", values=post_dict)

            response = BytesIO()
            response.write(b"done")
            self.wfile.write(response.getvalue())


if __name__ == "__main__":
     httpd = HTTPServer(("localhost", 8000), HttpHandler)
     httpd.serve_forever()


