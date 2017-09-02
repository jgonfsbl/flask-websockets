"""
Developed by Jonathan Gonzalez, EA1HET, on September 2017
"""
##
# This is the microservice's main application.
#
# This application is initialized as a flask application. Flask is a powerfull microframework.
# The configuration is loaded upon initialization and a variable is read (FLASK_CONFIG) from
# the dotenv file (.env).
#
# If it is defined, then, the configured value will be applied as application configuration,
# but, if it is not defined on the dotenv file, then the default configuration mode will be
# applied, that is, development mode (dev). This way is pretty simple change from development
# mode to production mode, or even test mode, without touching the code.
#
##

import os
from threading import Lock
from flask import Flask, session, request, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
import config

# Eventlet suppport for gUnicorn has been added via PIP. This can also be None to autoselect
# best posible aync mode from packages installed
async_mode = None

app = Flask(__name__)  # pylint: disable=invalid-name
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


__configName__ = os.environ.get('FLASK_CONFIG', 'Prod')
app.config.from_object(getattr(config, __configName__.title() + 'Config'))


def background_thread():
    """
    Send server generated events to clients. Infinite loop.
    """
    count = 0
    while True:
        socketio.sleep(10)
        count += 1


@app.route('/', methods=['GET'])
def index():
    """
    This is a dummy function to put to work the '/' namespace
    :return: A message (text/plain)
    """
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('connect', namespace='/dxspots')
def ws_connect():
    """
    Try to connect in any of the possible aync manners (thread, eventlet or gevent).
    :return: An open WebSocket
    """
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('ws_response', {'data': 'Trying to connect', 'count': 0})


@socketio.on('disconnect_request', namespace='/dxspots')
def ws_disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('ws_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('disconnect', namespace='/dxspots')
def ws_disconnect():
    """
    Closes a WebSocket
    :return: None / Log message
    """
    print('Client disconnected', request.sid)


@socketio.on('ws_ping', namespace='/dxspots')
def ws_ping_pong():
    """
    Dummy function to Send/Receive over WebSocket
    :return: A round-trip time measure in miliseconds
    """
    emit('ws_pong')


@socketio.on('ws_event', namespace='/dxspots')
def ws_single_event(message):
    """
    Get a message sent from client browser and send it back over WebSocket
    :param message: A text string coming from a HTML form painted on client's browser
    :return: Same text string received
    """
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('ws_response',
         {'data': message['data'], 'count': session['receive_count']})


if __name__ == '__main__':
    socketio.run(app)
