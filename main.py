import os
from dotenv import load_dotenv
from flask import Blueprint, Flask

load_dotenv()
app = Flask(__name__)


name = os.environ.get("NAME")

coinbase = Blueprint('coinbase', __name__, url_prefix='/coinbase')
accounts = Blueprint('accounts', __name__, url_prefix='/accounts')

coinbase.register_blueprint(accounts)
app.register_blueprint(coinbase)

@app.route('/')
def hello_world():
    print(app.url_map)
    return 'Hello, World!'

