from flask import Flask
from app.service import onstart

app = Flask(__name__)
app.debug = True

onstart()

from app import routes
