#!/bin/bash

# - bind on 9234 port
# - sapwn 5 worker process
# - set request timeout as 10 seconds
# - will be restarted automatically
# - preload before fork resource to work.
gunicorn -p gunicorn.pid --preload --bind 0.0.0.0:$TW_PORT --timeout=10 --workers=5 -k gevent run:api