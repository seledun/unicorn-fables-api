#!/bin/bash
python -m venv ./venv
venv/Scripts/activate
pip install -r requirements.txt
flask --app src/app run