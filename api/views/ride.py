from flask import Flask, abort, request
from flask_restplus import Resource, fields, Model, Api
from flask_jwt_extended import (jwt_required, get_raw_jwt)

from ..models import user_model, ride_model
from .helpers import required_input, validate_email, validate_json
from .request import driver_required

app = Flask(__name__)
api = Api(app)


class Ride(Resource):
    @jwt_required
    def post(self):
        """Creates a ride if user has already added car and a driver's license"""
        validate_json()
        required_input("location", 422)
        required_input("destination", 422)
        required_input("departure", 422)
        required_input("capacity", 422)

        data = request.get_json()

        # extract user_id from token
        user_id = get_raw_jwt()['identity']['id']
        location = data['location']
        destination = data['destination']
        departure = data['departure']
        capacity = data['capacity']
        ride = ride_model.Ride(
            user_id, location, destination, departure, capacity)

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
                "capacity": capacity
            }, 201

    @jwt_required
    def get(self):
        """fetches all existing rides"""
        rides = ride_model.Ride.get_rides()

        if not rides:
            return {
                "message": "no rides available"
            }, 404
        rides_list = []
        for ride in rides:
            driver = user_model.User.is_driver(ride['user_id'])
            rides_list.append({
                "id": ride['id'],
                "driver": driver['first_name']+" "+driver['last_name'],
                "location": ride['location'],
                "departure": ride['departure'],
                "capacity": ride['capacity'],
                "passengers": ride['passengers']
            })
        return {"status": "success", "rides": rides_list}, 200
        # return {
        #     "status": "success",
        #     "rides": rides
        # }, 200

    """GET /rides/<ride_id>
       Fetches the details of a specific ride based on ride id
    """


class RideDetails(Resource):
    """GET /rides/<ride_id>
       Fetches the details of a specific ride based on ride id
    """
    @jwt_required
    def get(self, ride_id):
        ride = ride_model.Ride.get_ride_by_id(ride_id)

        if not ride:
            abort(404, "No ride with id {} found".format(ride_id))
        driver = user_model.User.is_driver(ride['user_id'])
        driver_name = driver['first_name']+" "+driver['last_name']
        car_reg = driver['car_reg']
        return {
            "status": "success",
            "driver": driver_name,
            "car": car_reg,
            "ride": ride
        }, 200


class CompleteRide(Resource):
    @driver_required
    def post(self, ride_id):
        """Changes complete to true to reflect ride is successful"""
        ride = ride_model.Ride.get_ride_by_id(ride_id)
        if not ride:
            abort(404, "No ride with id {} found".format(ride_id))
        if ride['user_id'] != get_raw_jwt()['identity']['id']:
            # prevent aliens from completing someone's ride
            abort(401, "Unauthorized action!")
        ride_to_complete = ride_model.Ride(
            ride['user_id'], ride['location'], ride['destination'], ride['departure'], ride['capacity'])

        ride_to_complete.passengers = ride["passengers"]
        ride_to_complete.complete_ride(ride_id)
        return {
            "status": "success",
            "ride": ride
        }, 200
