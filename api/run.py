import os
from flask import Flask, Blueprint
from flask_restplus import Api, fields
from .schema import create_tables

from .views import auth

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app, description='Star Ride API endpoint')

create_tables()

"""Register user"""

user_namespace = api.namespace(
    "Users API", description="User registration APIs", path="/api/v1/auth")
user_namespace.add_resource(auth.Register, "/signup")
