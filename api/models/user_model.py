from passlib.hash import pbkdf2_sha256 as sha256
from . import CRUD


class User():
    """constructor class for user"""

    def __init__(self, first_name, last_name, email, tel, password, dl_path="", car_reg=""):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.tel = tel
        self.password = password
        self.dl_path = dl_path
        self.car_reg = car_reg

    @staticmethod
    def hash_password(password):
        return sha256.hash(password)

    @staticmethod
    def verify_password(password, hash):
        return sha256.verify(password, hash)

    def create_user(self):
        query = """
                    INSERT INTO users (first_name, last_name, email, tel, password, dl_path, car_reg)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}','{5}','{}','{6}')
                """.format(self.first_name, self.last_name, self.email, self.tel, self.password, self.dl_path, self.car_reg)
        CRUD.commit(query)

    @staticmethod
    def find_by_email(email):
        query = "SELECT id, email, tel, name, password FROM users WHERE email = '{0}'".format(
            email)
        user = CRUD.readOne(query)
        return user

    @staticmethod
    def is_driver(user_id):
        query = "SELECT name, dl_path, car_reg FROM users WHERE id = {0}".format(
            user_id)

        driver = CRUD.readOne(query)
        return driver
