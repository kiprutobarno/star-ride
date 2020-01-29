import psycopg2
from .config import dbConfig

parameters = dbConfig()


def create_tables():
    """create users, rides, requests, complete_rides and revoked_tokens table"""
    commands = [
        """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            tel VARCHAR(255),
            password VARCHAR(255) NOT NULL,
            dl_path VARCHAR(255),
            car_reg VARCHAR(255)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rides (
            id SERIAL PRIMARY KEY,
            user_id integer NOT NULL,
            location VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            departure VARCHAR(255) NOT NULL,
            passengers VARCHAR(255)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS requests (
            id SERIAL PRIMARY KEY,
            ride_id integer NOT NULL,
            passenger_id integer NOT NULL,
            pickup VARCHAR(255) NOT NULL,
            dropoff VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS complete_rides (
            id SERIAL PRIMARY KEY,
            ride_id integer NOT NULL,
            driver_id integer NOT NULL,
            location VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            departure VARCHAR(255) NOT NULL,
            passengers VARCHAR(255)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS revoked_tokens (
            id SERIAL PRIMARY KEY,
            tokens VARCHAR(255) NOT NULL
        )
        """
    ]

    try:
        conn = None
        conn = psycopg2.connect(**parameters)
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError)as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
    