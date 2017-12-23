# From the flask package, import the Flask Class
from flask import Flask

# Gives the file a unique name ?
app = Flask(__name__)

# function name can be anything, just needs to be unique
@app.route('/')
def home():
	return "Hello, world!"

app.run(port=5000)