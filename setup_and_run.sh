#!/bin/bash

# Create the virtual environment
python -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=run
export FLASK_ENV=development

# Run the Flask application
flask run --reload