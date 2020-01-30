from flask import Flask, abort, request
from flask_restplus import Resource, fields, Model, Api
from flask_jwt_extended import (jwt_required, get_raw_jwt)

from ..models import user_model, ride_model
from .helpers import required_input, validate_email, validate_json

app = Flask(__name__)
api = Api(app)


class CreateRide(Resource):
    @jwt_required
    def post(self):
        """Creates a ride if user has already added car and a driver's license"""
        validate_json()
        required_input("location", 422)
        required_input("destination", 422)
        required_input("departure", 422)

        data = request.get_json()

        # extract user_id from token
        user_id = get_raw_jwt()['identity']['id']
        location = data['location']
        destination = data['destination']
        departure = data['departure']
        ride = ride_model.Ride(user_id, location, destination, departure)

        # check if user has added car and driver's license
        is_driver = user_model.User.is_driver(user_id)
        if not is_driver or not is_driver["dl_path"] or not is_driver["car_reg"]:
            abort(401, "Add your driver's license and car to ride")
        else:
            if ride.get_ride_by_driver(user_id):
                # Abort if driver has an active ride
                abort(401, "You already have an incomplete ride")
            ride.create_ride()
            driver_name = is_driver['first_name']+" "+is_driver['last_name']
            car_reg = is_driver['car_reg']
            return {
                "status": "success",
                "driver": driver_name,
                "car": car_reg,
                "location": location,
                "departure": departure,
            }, 201
