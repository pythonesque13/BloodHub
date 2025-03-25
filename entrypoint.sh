#!/bin/bash

# Start FastAPI in the background
uvicorn api.predict:app --host 0.0.0.0 --port 8000 &

# Start Dash application
python app.py