from flask import Flask, abort, json, request
from flask_restplus import Resource, fields, Model, Api
from ..models import user_model
from .helpers import validate_json, validate_email, check_for_blanks, check_data_type, validate_required
app = Flask(__name__)
api = Api(app)


class Register(Resource):
    def post(self):
        """creates a new user"""
        data = request.get_json()
        validate_json()
        validate_required(request)

        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        tel = data['tel']
        password = data['password']
        dl_path = data['dl_path']
        car_reg = data['car_reg']

        check_for_blanks(data)
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
            # user = user_model.User.find_by_email(email)
            # payload = {
            #     "id": user['id'],
            #     "email": user['email'],
            #     "tel": user['tel'],
            #     "first_name": user['first_name'],
            #     "last_name": user['last_name']
            # }
            return {
                "status": "success",
                "message": "{} registered".format(data['email'])
            }, 201
