#!/bin/bash

echo "instalando virtualenv..."
pip install virtualenv

virtualenv venv
source venv/bin/activate

pip install -r requirements.txt

deactivate

