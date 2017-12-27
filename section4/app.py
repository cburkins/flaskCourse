
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
	def get(self, name):

		# filter() will loop through items, returning the list of items where function is true, returns a filter object, not a list
		# You can either call list() for the whole list, or next() for just the 1st item
		# We're only expecting one item, so next() works great
		# None is the default value if there's nothing in the filter object
		item = next(filter(lambda x: x['name'] == name, items), None)
		# Return a helpful message (in JSON) along with a 404 status code
		return {'item': None}, 200 if item else 404	

	def post(self, name):
		# error control, make sure the item doesn't already exist
		if next(filter(lambda x: x['name'] == name, items), None):
			return {'message': "An item with name '{}' already exists.".format(name) }, 400

		# Side effect, throws error if content-type isn't set to JSON
		data = request.get_json();
		# Add the item
		item = {'name': name, 'price': data['price']}
		items.append(item);
		# flask_restful automatically jsonifies our dictionary
		# Also return 201 (created)
		return item, 201;

class ItemList(Resource):
	def get(self):
			return {'items': items}


# http://127.0.0.1/item/<name>  (GET/POST for single items)
api.add_resource(Item, '/item/<string:name>');
# http://127.0.0.1/items  (GET list all items)
api.add_resource(ItemList, '/items')


#app.run(port=5000)
app.run(port=5000, debug=True)

