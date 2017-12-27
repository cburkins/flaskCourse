
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
	def get(self, name):
		for item in items:
			if item['name'] == name:
				# flask_restful automatically jsonifies our dictionary
				return item;
		# Return a helpful message (in JSON) along with a 404 status code
		return {'item': None}, 404	

	def post(self, name):
		# Side effect, throws error if content-type isn't set to JSON
		data = request.get_json();
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

