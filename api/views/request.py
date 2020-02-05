from flask import Flask, abort, request
from flask_restplus import Resource, Model, Api
from flask_jwt_extended import (
    jwt_required, get_raw_jwt, verify_jwt_in_request, get_jwt_claims)
from functools import wraps

from ..models import ride_model, request_model, user_model
from .helpers import required_input, validate_email, validate_json

app = Flask(__name__)
api = Api(app)


def driver_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if get_jwt_claims()['car_reg'] == "":
            abort(401, "Only drivers can access this endpoint!")
        return fn(*args, **kwargs)
    return wrapper


def passenger_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if get_jwt_claims()['car_reg'] != "":
            abort(401, "Only passengers can access this endpoint!")
        return fn(*args, **kwargs)
    return wrapper


class RideRequest(Resource):
    @jwt_required
    def get(self, ride_id):
        """Fetches all requests for <ride_id>"""
        user_id = get_raw_jwt()['identity']['id']
        ride = ride_model.Ride.get_ride_by_driver(user_id)
        if not ride or str(ride["id"]) != ride_id:
            abort(404, "no rides found")
        requests = request_model.Request.get_ride_requests(ride_id)
        request_list = []
        for request in requests:
            passenger = user_model.User.get_passenger(request['passenger_id'])
            request_list.append({
                "id": request['id'],
                "passenger": passenger['first_name']+" "+passenger['last_name'],
                "pickup": request['pickup'],
                "dropoff": request['dropoff'],
                "status": request['status']
            })
        return {"status": "success", "ride_requests": request_list}, 200

    @passenger_required
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
        passenger = user_model.User.get_passenger(passenger_id)
        pickup = data['pickup']
        dropoff = data["dropoff"]

        ride_request = request_model.Request(
            ride_id, passenger_id, pickup, dropoff)

        passengers = ride_model.Ride.get_passengers_no(ride_id)['passengers']
        if passengers < ride['capacity']:
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
        abort(400, "Capacity")


class ProcessRequest(Resource):
    @driver_required
    def get(self, ride_id):
        """Fetches all requests for <ride_id>"""
        user_id = get_raw_jwt()['identity']['id']
        ride = ride_model.Ride.get_ride_by_driver(user_id)
        if not ride or str(ride["id"]) != ride_id:
            abort(404, "no rides found")
        requests = request_model.Request.get_ride_requests(ride_id)
        request_list = []
        for request in requests:
            passenger = user_model.User.get_passenger(request['passenger_id'])
            request_list.append({
                "id": request['id'],
                "passenger": passenger['first_name']+" "+passenger['last_name'],
                "pickup": request['pickup'],
                "dropoff": request['dropoff'],
                "status": request['status']
            })

        return {"status": "success", "requests": request_list}, 200

    @driver_required
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
        passengers = ride_model.Ride.get_passengers_no(ride_id)['passengers']
        if passengers < ride['capacity']:
            ride_model.Ride.update_passengers(passengers+1, ride_id)
            new_passengers = ride_model.Ride.get_passengers_no(ride_id)[
                'passengers']
            return {
                "status": "success",
                "request_status": status,
                "passengers": new_passengers
            }, 200
        abort(400, "Capacity")


class RidePassengers(Resource):
    @jwt_required
    def get(self, ride_id):
        passengers = request_model.Request.get_passengers(ride_id)
        return {
            "status": "success",
            "passengers": passengers
        }, 200


class RidePassenger(Resource):
    @jwt_required
    def get(self, ride_id, passenger_id):
        passenger_details = user_model.User.get_passenger(passenger_id)
        return {
            "status": "success",
            "passenger": passenger_details['first_name']+" "+passenger_details['last_name']
        }, 200
