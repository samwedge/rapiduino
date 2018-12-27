#!/bin/bash

virtualenv -p python2 py2env
curl https://bootstrap.pypa.io/get-pip.py | py2env/bin/python
py2env/bin/pip install -r requirements.txt

virtualenv -p python3 py3env
curl https://bootstrap.pypa.io/get-pip.py | py3env/bin/python
py3env/bin/pip install -r requirements.txt
