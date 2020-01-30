from . import CRUD


class RevokedTokens():
    def __init__(self, token):
        self.token = token

    def revoke_token(self):
        """insert token into revoked_tokens table in database"""
        query = "INSERT INTO revoked_tokens (tokens) VALUES ('{}')".format(
            self.token)
        CRUD.commit(query)

    @staticmethod
    def is_revoked(jti):
        """select token based on token jti"""
        query = "SELECT tokens FROM revoked_tokens WHERE tokens='{}'".format(
            jti)
        tokens = CRUD.readAll(query)
        return tokens
