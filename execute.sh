#!/bin/bash

# Create a virtual environment
python -m venv virtual_env

# Activate the virtual environment
source virtual_env/bin/activate

# Install the required packages
pip install -r requirements.txt

# Run streamlit
streamlit run rag_app.py