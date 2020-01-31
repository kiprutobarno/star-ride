from flask import Flask, abort, json, request
from flask_restplus import Resource, fields, Model, Api
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_raw_jwt)
from ..models import user_model, token_model
from .helpers import validate_json, validate_email, check_for_blanks, check_data_type, validate_required, required_input, optional_input
app = Flask(__name__)
api = Api(app)


class Register(Resource):
    def post(self):
        """creates a new user"""
        data = request.get_json()
        validate_json()
        required_input("first_name", 400)
        required_input("last_name", 400)
        required_input("email", 400)
        required_input("tel", 400)
        required_input("password", 400)
        optional_input("car_reg")
        optional_input("dl_path")

        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        tel = data['tel']
        password = data['password']
        dl_path = data['dl_path']
        car_reg = data['car_reg']

        # check_for_blanks(data)
        check_data_type(data)
        validate_email(email)

        new_user = user_model.User(first_name,
                                   last_name,
                                   email,
                                   tel,
                                   user_model.User.hash_password(password),
                                   dl_path,
                                   car_reg)

        user_exists = user_model.User.find_by_email(email)
        if user_exists:
            abort(409, 'An account with email {} already exists'.format(new_user.email))
        else:
            new_user.create_user()
            return {
                "status": "success",
                "message": "{} registered".format(data['email'])
            }, 201


class Login(Resource):
    def post(self):
        """Endpoint verifies user based on email and password"""
        validate_json()
        required_input("email", 400)
        required_input("password", 400)

        data = request.get_json()
        email = data['email']
        password = data['password']

        check_for_blanks(data)
        check_data_type(data)
        validate_email(email)

        user_exists = user_model.User.find_by_email(email)
        if not user_exists:
            abort(404, 'User {} does not exist, please register'.format(email))

        password_hash = user_exists['password']
        username = user_exists['first_name']

        if user_model.User.verify_password(password, password_hash):
            payload = {
                "id": user_exists['id'],
                "email": user_exists['email']
            }
            access_token = create_access_token(identity=payload)
            return {
                "status": "success",
                "message": "{} logged in".format(username),
                "token": access_token
            }, 200

        else:
            return {
                "status": "fail",
                "message": "wrong password",
            }, 400


class Logout(Resource):
    @jwt_required
    def post(self):
        """logs out user by adding current token to revoked token list"""
        jti = get_raw_jwt()['jti']
        token = token_model.Token(jti)
        token.revoke_token()

        return {'message': 'Access revoked and logged out!'}, 201
