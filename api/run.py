import os
from flask import Flask
from .schema import create_tables

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


create_tables()
