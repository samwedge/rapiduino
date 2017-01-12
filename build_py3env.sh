#!/bin/bash
virtualenv -p /usr/bin/python3 py3env
source py3env/bin/activate
pip install -r requirements.txt