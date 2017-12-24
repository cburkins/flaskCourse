# From the flask package, import the Flask Class (upper-case)
# From the flask package, import teh jsonify method (lower-case)
from flask import Flask, jsonify

# Create a flask object using a unique name
app = Flask(__name__)

# function name can be anything, just needs to be unique
# http://127.0.0.1:5000/hello
@app.route('/hello')
def home():
	return "Hello, world!"
stores = [
	{
		'name': 'My Wonderful Store',
		'items': [
			{
			'name': 'My Item',
			'price': 15.99
			}
		]
	}
]

# POST - used to receive data (since we're the server)
# GET - used to send data back 



# POST /store data: {name:}
# By default, @app.route decorator does a GET request, and browsers only do GET requests
@app.route('/store', methods=['POST'])
def create_store():
	return "create_store()"

# GET /store/<string:name>
# <string:name> is flask syntax for making a parameter available to the function
@app.route('/store/<string:name>')
def get_store(name):
	return "get_store(%s)" % (name)

# GET /store
@app.route('/store')
def get_stores():
	# jsonify takes a dictionary, and our stores data structure is actually a list
	# add a key to make the list a dictionary
	return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_store(name):
	pass

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
	pass

app.run(port=5000)