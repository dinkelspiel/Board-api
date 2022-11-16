from flask import Flask, render_template, request, Response, send_file
import mysql.connector
import json, time, uuid
from markupsafe import escape
from flask_cors import CORS
from grammar import grammar
from staticpages import staticpages
from board import board
from user import user

app = Flask(__name__)
app.register_blueprint(grammar)
app.register_blueprint(staticpages)
app.register_blueprint(board)
app.register_blueprint(user)
CORS(app)

# posts = []
# posts = json.loads(open("data.json", "r").read())
    
app.run(host="192.168.144.6", port="8080")
