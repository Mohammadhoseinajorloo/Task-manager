from config import HOST, NAME_DB, USER, PASSWORD
import mysql.connector


class DataBase:

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(DataBase)
            return cls.instance
        return cls.instance


    def __init__(self):
        self.cnx = mysql.connector.connect(
            host=HOST,
            database=NAME_DB,
            user=USER,
            password=PASSWORD
        )
        self.cursor = self.cnx.cursor()


    def __createing_query(self, dic:dict) -> str:

        query = ""
        i = 0
        for k, v in dic.items():
            if i < len(dic) - 1:
                query += f"{k} {v},"
                i += 1
            else:
                query += f"{k} {v}"

        return query


    def __inserting_query(self, dic:dict) -> str:

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
        query = self.__createing_query(col)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table}({query})")
        self.cnx.commit()
        return


    def insert(self, table:str, values:dict):
        columns, values = self.__inserting_query(values)
        self.cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")
        self.cnx.commit()
        return

    def __del__(self):
        self.cnx.close()