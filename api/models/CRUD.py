import psycopg2
import psycopg2.extras
from ..schema import parameters


def commit(command):
    """insert, delete, update database"""
    try:
        conn = None
        conn = psycopg2.connect(**parameters)
        cursor = conn.cursor()
        cursor.execute(command)
        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()


def readAll(command):
    """select many items from database"""
    try:
        conn = None
        conn = psycopg2.connect(**parameters)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(command)
        results = None
        results = cursor.fetchall()
        cursor.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()


def readOne(command):
    """select one item from database"""
    try:
        conn = None
        conn = psycopg2.connect(**parameters)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(command)
        result = None
        result = cursor.fetchone()
        cursor.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
