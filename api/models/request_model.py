from . import CRUD


class Request():
    def __init__(self, ride_id, passenger_id, pickup, dropoff, status="pending"):
        self.ride_id = ride_id
        self.passenger_id = passenger_id
        self.pickup = pickup
        self.dropoff = dropoff
        self.status = status

    def create_request(self):
        query = """
            INSERT INTO requests(ride_id, passenger_id, pickup, dropoff, status) 
            VALUES ({}, {}, '{}', '{}', '{}')""".format(self.ride_id, self.passenger_id, self.pickup, self.dropoff, self.status)
        CRUD.commit(query)

    @staticmethod
    def get_ride_requests(ride_id):
        query = """SELECT id, passenger_id, pickup, dropoff, status FROM requests WHERE ride_id={}""".format(
            ride_id)

        return CRUD.readAll(query)

    @staticmethod
    def get_passenger_request(passenger_id, ride_id):
        query = """SELECT pickup, dropoff, status FROM requests WHERE passenger_id={} ride_id={}""".format(
            passenger_id, ride_id)
        return CRUD.readOne(query)

    @staticmethod
    def process_request(status, request_id, ride_id):
        query = """UPDATE requests SET status='{}' WHERE id={} and ride_id={}""".format(
            status, request_id, ride_id)
        CRUD.commit(query)
