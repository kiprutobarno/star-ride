import os
from configparser import ConfigParser


def dbConfig(file="db.ini", section="postgresql"):
    # create parser
    parser = ConfigParser()

    # read file
    parser.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), file))

    # get section postgresql
    db = {}
    parameters = parser.items(section)
    for parameter in parameters:
        db[parameter[0]] = parameter[1]

    return db
