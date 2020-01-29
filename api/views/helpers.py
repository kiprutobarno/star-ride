import re
from flask import request, abort, jsonify, make_response


def validate_json():
    """validates if input is in JSON format"""
    if not request.is_json:
        abort(400, "request should be in JSON format")


def validate_email(email):
    """validates if email is in email format"""
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        abort(400, 'Invalid email format')


def required_input(data_input, status_code):
    """check for required fields"""
    if not data_input in request.get_json():
        abort(status_code, "field {0} is required".format(data_input))


def optional_input(data_input, status_code):
    """puts empty field in optional inputs"""
    if not data_input in request.get_json():
        data = request.get_json()
        data[data_input] = ""


def validate_required(request):
    """Validates key-value pairs of request dictionary body"""

    keys = ['first_name', 'last_name', 'email',
            'password', 'car_reg', 'dl_path']
    for key in keys:
        if key not in request.json:
            abort(400, "{0} field is required".format(key))


def blanks(data):
    blanks = []
    for key, value in data.items():
        if value == "":
            blanks.append(key)
    return blanks


def check_for_blanks(data):
    spaces = []
    spaces = blanks(data)
    for blank in spaces:
        return abort(400, "{} cannot be blank".format(blank))


def check_data_type(data):
    for key, value in data.items():
        if not isinstance(value, str):
            return abort(400, "A {} must be a String".format(key))
        
