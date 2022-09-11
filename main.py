import os
from dotenv import load_dotenv
from flask import Flask
from ftx.rest.client import FtxClient

load_dotenv()
app = Flask(__name__)

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")


@app.route('/')
def main():
    ftx = FtxClient(api_key, api_secret)
    balances = ftx.get_balances()
    print(balances)
    return 'Success'
