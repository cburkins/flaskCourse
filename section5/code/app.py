	
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

# Our own package
from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

# Initialize the jwt object, creates /auth endpoint
jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):

	# Parser belongs to the class, not any particular item (instance)
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float, 
		required=True,
		help="This field cannot be left blank, silly."
	)

	# GET
	@jwt_required()
	def get(self, name):

		# filter() will loop through items, returning the list of items where function is true, returns a filter object, not a list
		# You can either call list() for the whole list, or next() for just the 1st item
		# We're only expecting one item, so next() works great
		# None is the default value if there's nothing in the filter object
		item = next(filter(lambda x: x['name'] == name, items), None)
		# Return a helpful message (in JSON) along with a 404 status code
		return {'item': None}, 200 if item else 404	

	# POST
	def post(self, name):
		# error control first, make sure the item doesn't already exist
		if next(filter(lambda x: x['name'] == name, items), None):
			return {'message': "An item with name '{}' already exists.".format(name) }, 400

		# Use a class method to get/verify given arguments
		data = Item.parser.parse_args()

		# Add the item
		item = {'name': name, 'price': data['price']}
		items.append(item);
		# flask_restful automatically jsonifies our dictionary
		# Also return 201 (created)
		return item, 201;

	# PUT
	def put(self, name):
		# Use a class method to get/verify given arguments
		data = Item.parser.parse_args()

		item = next(filter(lambda x: x['name'] == name, items), None)
		if item is None:
			item = {'name': name, 'price': data['price']}
			items.append(item)
		else:
			# Use update() method of dictionary
			item.update(data)
		return item;

	# DELETE
	def delete(self, name):
		# Tell python that we're not trying to declar a local variable, we want to use the global variable
		global items;
		# Find all elements except for one
		items = list(filter(lambda x: x['name'] != name, items))
		return {'message': 'Item deleted'}, 200


class ItemList(Resource):
	def get(self):
			return {'items': items}


# http://127.0.0.1/item/<name>  (GET/POST for single items)
api.add_resource(Item, '/item/<string:name>');
# http://127.0.0.1/items  (GET list all items)
api.add_resource(ItemList, '/items')


#app.run(port=5000)
app.run(port=5000, debug=True)

