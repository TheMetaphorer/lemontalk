import flask
import json
import engine

from flask_socketio import SocketIO
from hashlib import sha512
from datetime import datetime
from os import urandom

app = flask.Flask(__name__)
socketio = SocketIO(app)
chat_stack = engine.ChatStack()
kotd_seed = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return flask.render_template('chat.html')

def generate_kotd():
    hashobj = sha512()
    hashobj.update(str(kotd_seed).encode('utf-8'))
    return hashobj.hexdigest()

@socketio.on("connected")
def disseminate_key():
    socketio.emit('nk', generate_kotd())

@socketio.on('message')
def listener(data):
    global kotd_seed
    data[0] = json.loads(data[0])
    data[1] = json.loads(data[1])
    chat_stack.push(data)
    deciphered = chat_stack.decrypt_top_stack().replace("'", '"')
    socketio.emit('update', json.loads(deciphered))
    kotd_seed = urandom(12)
    socketio.emit('nk', generate_kotd())
    return chat_stack.stack[0][0]


if __name__ == '__main__':
    app.jinja_env.globals.update(kotd=generate_kotd)
    socketio.run(app, debug=True, host='0.0.0.0')
