# Command to run:  & C:/Users/felip/Downloads/minecraft-admin/API/.venv/Scripts/python.exe -m flask --app c:/Users/felip/Downloads/minecraft-admin/API/main.py run
# VS Code Notes: Change the python interpreter to .venv(64/32)\Scripts\python (ctrl _+ shift + p -> select clear python interpreter)
import sys
import os
import site

# Help: https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory

# Testing virtual environments paths for any CPU Artitecture and Operating Systems
# User may have a 32 bit or 64 bit python installation
# This program will be dynamically adapt to the user's python installation architecture
# Ideal for server deployments where the architecture is unknown

# Virtual environment paths
if not (os.path.isdir(os.getcwd() + '\..\.venv_64\LIB\site-packages')):
    if not (os.path.isdir(os.getcwd() + '\..\.venv_32\LIB\site-packages')):
        print("No virtual environment found. Please create a virtual environment first.")
        sys.exit(1)
    else:
        sys.path.append(os.getcwd() + '\..\.venv_32\LIB\site-packages')
else:
    sys.path.append(os.getcwd() + '\..\.venv_64\LIB\site-packages')
print(os.getcwd() + '/API/.venv/LIB/site-packages')
#os.system('pause')

# Check if Flask is installed in the virtual environment
try:
    from flask import Flask, render_template
except ImportError:
    print("Flask is not installed in the virtual environment. Please install Flask and try again.")
    sys.exit(1)

# To run this file
# py -m flask --app __init__.py run
# Activate the virtual environment first and flask will use the packages from the virtual environment
# Help: https://stackoverflow.com/questions/31002890/how-to-reference-a-html-template-from-a-different-directory-in-python-flask
# Help: https://stackoverflow.com/questions/22259847/application-not-picking-up-css-file-flask-python

# Test HTML templates via flask
app = Flask(__name__,template_folder='templates')
@app.route('/')
def home():
    return render_template('server-list-layout.html')
    #return render_template('base.html')
    #return '<h1>Welcome to the Minecraft Server Admin API</h1>'

