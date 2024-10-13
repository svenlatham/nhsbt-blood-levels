#!/bin/bash
set -e # Stop if there are errors!
pip install pandas plotly jinja2
python ./create-page.py
cd docs
python3 -m http.server