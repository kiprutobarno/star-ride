from flask import Flask, abort, request
from flask_restplus import Resource, Model, Api
from flask_jwt_extended import (jwt_required, get_raw_jwt)

from ..models import ride_model, request_model, user_model
from .helpers import required_input, validate_email, validate_json

app = Flask(__name__)
api = Api(app)


class RideRequest(Resource):
    @jwt_required
    def post(self, ride_id):
        validate_json()
        required_input("pickup", 400)
        required_input("dropoff", 400)

        data = request.get_json()
        ride = ride_model.Ride.get_ride_by_id(ride_id)
        ride_details = user_model.User.is_driver(ride['user_id'])
        if not ride:
            return {"message": "ride doesnt exist"}, 404
        passenger_id = get_raw_jwt()['identity']['id']
        passenger = user_model.User.is_driver(passenger_id)
        user_ride = ride_model.Ride.get_ride_by_driver(passenger_id)
        if user_ride is not None:
            return {"message": "You cannot request your own ride"}, 400
        pickup = data['pickup']
        dropoff = data["dropoff"]

        ride_request = request_model.Request(
            ride_id, passenger_id, pickup, dropoff)

        ride_request.create_request()
        return {
            "status": "request sent",
            "passenger": passenger['first_name']+" "+passenger['last_name'],
            "pickup": pickup,
            "dropoff": dropoff,
            "car": ride_details['car_reg'],
            "driver": ride_details['first_name']+" "+ride_details['last_name'],
            "request_status": ride_request.status
        }, 201


class ProcessRequest(Resource):
    @jwt_required
    def put(self, ride_id, request_id):
        """ Changes the status of the ride <ride_id> request <request_id> to reflect "accepted" or "rejected"
        """
        required_input("request_status", 400)
        user_id = get_raw_jwt()['identity']["id"]
        ride = ride_model.Ride.get_ride_by_driver(user_id)
        if not ride or str(ride["id"]) != ride_id:
            abort(404, "Page not found")

        data = request.get_json()
        status = data['request_status']
        request_model.Request.process_request(status, request_id, ride_id)
        return {
            "status": "success",
            "request_status": status
        }, 200
