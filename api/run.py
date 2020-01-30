import os
from flask import Flask, Blueprint
from flask_restplus import Api, fields
from flask_jwt_extended import JWTManager
from .schema import create_tables

from .views import auth

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = "superpower"

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(app,
          authorizations=authorizations,
          security='apiKey',
          description='Star Ride API endpoint'
          )

create_tables()

"""Register user"""

user_namespace = api.namespace(
    "Users API", description="User registration APIs", path="/api/v1/auth")
user_namespace.add_resource(auth.Register, "/signup")
user_namespace.add_resource(auth.Login, "/login")
