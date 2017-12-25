# From the flask package, import the Flask Class (upper-case)
# From the flask package, import the jsonify method (lower-case)
# From the flask package, import the request method - not plural, plural is a different method (lower-case)
from flask import Flask, jsonify, request

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
	# "request" is the request that was made to this endpoint
	# get_jjson() method returns the JSON that was passed to us by caller, namely the name of the store they'd like to create
	print ("test")
	request_data = request.get_json();
	print (request_data);
	new_store = {
		'name': request_data['name'],
		'items': []
	}
	stores.append(new_store)
	# return the newly-created store so that the caller knows we successfully created new store
	return jsonify(new_store)

# GET /store/<string:name>
# <string:name> is flask syntax for making a parameter available to the function
@app.route('/store/<string:name>')
def get_store(name):
	for store in stores:
		if store['name'] == name:
			return jsonify(store)
	return jsonify({'message': 'store not found'})

# GET /store
@app.route('/store')
def get_stores():
	# jsonify takes a dictionary, and our stores data structure is actually a list
	# add a key to make the list a dictionary
	return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_store(name):
	request_data = request.get_json();
	for store in stores:
		if store['name'] == name:
			new_item = {
				'name': request_data['name'],
				'price': request_data['price']
			}
			store['items'].append(new_item);
			return jsonify(store);
	return jsonify({'message': 'store not found'})



# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
	for store in stores:
		if store['name'] == name:
			return jsonify({'items': store['items']})
	return jsonify({'message': 'store not found'})


app.run(port=5000)











