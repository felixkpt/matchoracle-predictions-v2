#!/bin/bash
# Activate the virtual environment
source /home/felix/Documents/Dev/python/matchoracle-predictions-v2/venv/bin/activate

# Set the working directory to where your app is located
cd /home/felix/Documents/Dev/python/matchoracle-predictions-v2

# Execute the uvicorn server
exec uvicorn app.main:app --host 127.0.0.1 --port 8085
