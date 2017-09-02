#!/bin/bash -e

# Due to the limited load balancing algorithm used by gunicorn, 
# it is not possible to use more than one worker process when using 
# this web server. 

# Activate VirtualEnvironment
source venv/bin/activate

# Set the environment
MODULE=app
APP=app
HOST=0.0.0.0
PORT=5000
NAME=DXSPOTS
WORKERS=1
WORKERTYPE=eventlet
TIMEOUT=120
PIDFILE=${NAME}.pid

# Run web server with app in foreground
exec gunicorn $1 ${MODULE}:${APP} \
--name $NAME \
--bind=$HOST:$PORT \
--pid=$PIDFILE \
--workers $WORKERS \
--worker-class $WORKERTYPE

# Alternative options 
# --timeout $TIMEOUT 
# --log-level=debug 

# De-Activate virtual environment
# While the execution is in background this is not used anymore
deactivate

exit 0
