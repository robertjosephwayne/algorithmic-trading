import os
from dotenv import load_dotenv
import pandas as pd
from connectors.ftx.rest.client import FtxClient
from connectors.ftx.websocket.client import FtxWebSocketClient
import tkinter as tk
import logging
import pprint

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

load_dotenv()
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

if __name__ == '__main__':

    ftx = FtxClient(api_key, api_secret)
    websocket = FtxWebSocketClient(api_key, api_secret)
    result = websocket.get_ticker('BTC-PERP')
    while True:
        btc_perp = websocket.get_ticker('BTC-PERP')
        print(btc_perp)

