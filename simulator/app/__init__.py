import os
from dotenv import load_dotenv
from flask import Flask, session

app = Flask(__name__)

load_dotenv()

app.secret_key = os.environ.get('FLASK_SECRET')

app.config.update(
    TEMPLATES_AUTO_RELOAD = True
)

from app import routes