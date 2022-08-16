import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()
app = Flask(__name__)


name = os.environ.get("NAME")

@app.route('/')
def hello_world():
    return 'Hello, World!'

