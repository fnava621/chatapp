from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit, BaseNamespace
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')
ws = SocketIO(app)

last_messages = []


@app.route('/')
def hello_world():
    return render_template('index.html')


@ws.on('connect', namespace='/chat')
def enter_chat():
    emit('connect', 'Hello!!!')
    for x in last_messages:
        emit('message', x)


@ws.on('send_message', namespace='/chat')
def handle_message(data):
    res = {
        'message': data['message'],
        'username': data['username'],
        'dateTime': datetime.utcnow().isoformat() + 'Z'
    }
    emit('message', res, namespace='/chat', broadcast=True)
    if len(res) > 100:
        last_messages.pop(0)
    last_messages.append(res)


if __name__ == '__main__':
    ws.run(app, host='0.0.0.0', port=3001)
