import bcrypt


class Hashing:
    def __init__(self):
        pass


    def _create_salt(self) -> str:
        return bcrypt.gensalt(rounds=12)


    def hash_pass(self, password:str):
        salt = self._create_salt()
        encode_password = password.encode()
        hash_password = bcrypt.hashpw(encode_password, salt)
        return hash_password.decode()
