import os
from dotenv import load_dotenv
from flask import Blueprint, Flask

load_dotenv()
app = Flask(__name__)


@app.route('/')
def hello_world():
    print(app.url_map)
    return 'Hello, World!'

