#!/bin/bash

python3 -m venv ./

source ./source/activate

python3 -m pip install -r requirements.txt

python3 Tools/yarGen/yarGen.py --update

mv ./db Tools/yarGen/

echo "Execute command (jupyter notebook)"