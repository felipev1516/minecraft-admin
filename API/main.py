# Command to run:  & C:/Users/felip/Downloads/minecraft-admin/API/.venv/Scripts/python.exe -m flask --app c:/Users/felip/Downloads/minecraft-admin/API/main.py run
import sys
import os
import site
# Help: https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
#print(os.getcwd() + '\API\.venv\LIB\site-packages')

sys.path.append(os.getcwd() + '\API\.venv\LIB\site-packages')

# Change the python interpreter to .venv\Scripts\python (ctrl _+ shift + p -> select clear python interpreter in VS code)
from flask import Flask

#print("Hello, World!")
app = Flask(__name__)
@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"