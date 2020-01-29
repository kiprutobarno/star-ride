import os
from flask import Flask

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.route("/hello", methods=['GET'])
def hello():
    return "Hello, World"
