from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import sqlite3
import os

class DataBase:

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(DataBase)
            return cls.instance
        return cls.instance


    def __init__(self, db_name:str):
        self.name = db_name
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()


    def __convert_dict_query(self, dic:dict) -> str:

        keys = ""
        values = ""
        i = 0
        for k, v in dic.items():
            if i < len(dic) - 1:
                keys += f"{k},"
                values += f"'{v}',"
                i += 1
            else:
                keys += f"{k}"
                values += f"'{v}'"

        return keys, values


    def create(self, table:str, col:dict) -> None:
        columns , _ = self.__convert_dict_query(col)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table}({columns})")
        self.conn.commit()
        return



    def insert(self, table:str, values:dict):
        columns, values = self.__convert_dict_query(values)
        self.cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")
        self.conn.commit()
        return

    def __del__(self):
        self.conn.close()


class HttpHandler(BaseHTTPRequestHandler):

    def set_headers(self):
        self.send_header(keyword="countent-type", value="application/json")
        self.end_headers()


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

            db = DataBase(db_name="users.db")
            db.create(table="users", col=post_dict)
            db.insert(table="users", values=post_dict)

            response = BytesIO()
            response.write(b"done")
            self.wfile.write(response.getvalue())


if __name__ == "__main__":
     httpd = HTTPServer(("localhost", 8000), HttpHandler)
     httpd.serve_forever()


