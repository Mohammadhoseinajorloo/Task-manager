import sqlite3

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
