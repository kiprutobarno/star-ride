from . import CRUD


class Ride():
    """Instantiates the user_id, location, destination and time of departure"""

    def __init__(self, user_id, location, destination, departure):
        self.user_id = user_id,
        self.location = location
        self.destination = destination
        self.departure = departure
        self.passengers = []

    def create_ride(self):
        """creates a new ride"""
        query = """INSERT INTO rides(user_id, location, destination, departure) VALUES ('{}','{}','{}','{}')""".format(
            self.user_id, self.location, self.destination, self.departure)
        CRUD.commit(query)

    @staticmethod
    def get_rides():
        """Gets all existing incomplete rides"""
        query = "SELECT * FROM rides"
        rides = CRUD.readAll(query)
        return rides

    @staticmethod
    def get_ride_by_id(ride_id):
        """Gets details of a particular incomplete ride by ride id"""
        query = "SELECT * FROM rides WHERE id='{}'".format(ride_id)
        ride = CRUD.readOne(query)
        return ride

    @staticmethod
    def get_ride_by_driver(driver_id):
        """"Get incomplete rides of a particular driver id"""
        query = "SELECT * FROM rides WHERE user_id='{}'".format(driver_id)
        ride = CRUD.readOne(query)
        return ride

    def complete_ride(self, ride_id):
        """ Creates a ride  in the completed rides table
            Deletes the ride from rides table
        """

        queries = [
            """
            INSERT INTO complete_rides(ride_id, driver_id, location, destination, departure, passengers)
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""".format(ride_id, self.user_id, self.location, self.destination, self.departure, self.passengers),
            """DELETE FROM rides where id='{}'""".format(ride_id)
        ]
        for query in queries:
            CRUD.commit(query)
