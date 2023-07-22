import os
import requests

from flask import Flask

# # ORIGINAL CODE
app = Flask(__name__, instance_relative_config=True)

if __name__ == "__main__":
    app.run('0.0.0.0', debug=True, port=8000, ssl_context='adhoc')


from .bin_day import app
