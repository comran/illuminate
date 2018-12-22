from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import json
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lettherebelight!'
socketio = SocketIO(app)

@socketio.on('connect')
def connect():
    print "someone connected"

if __name__ == '__main__':
    socketio.run(app)
