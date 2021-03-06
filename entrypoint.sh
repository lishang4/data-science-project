#!/bin/bash

# - bind on 9234 port
# - sapwn 5 worker process
# - set request timeout as 10 seconds
# - will be restarted automatically
# - preload before fork resource to worker.
gunicorn -p gunicorn.pid --preload --bind 0.0.0.0:9234 --timeout=120 --workers=1 --threads=9 -k gevent run:api
