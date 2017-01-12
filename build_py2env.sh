#!/bin/bash
virtualenv -p /usr/bin/python2 py2env
source py2env/bin/activate
pip install -r requirements.txt