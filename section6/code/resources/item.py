
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):

	# Parser belongs to the class, not any particular item (instance)
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float, 
		required=True,
		help="This field cannot be left blank, silly."
	)

	# - - - - - - - - - - - - - - 
	# GET
	@jwt_required()
	def get(self, name):

		# this is a class method; however, we can still call it via self
		item = ItemModel.find_by_name(name);		

		if item:
			# item is an ItemModel object (not a dictionary), so convert to json
			return item.json()
		# Item wasn't found, return a helpful message (in JSON) along with a 404 status code
		return {'message': 'Item not found'}, 404

	# - - - - - - - - - - - - - - 
	# POST
	def post(self, name):
		# error control first, make sure the item doesn't already exist
		# class method, so we can call via self.find_by_name() or Item.find_by_name()
		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name) }, 400

		# Use a class method to get/verify given arguments
		data = Item.parser.parse_args()

		# Add the item
		item = ItemModel(name, data['price'])

		try:
			item.insert()
		except:
			return {"message": "An error occurred inserting the item."}, 500  # 500 = Internal Server Error

		# flask_restful automatically jsonifies our dictionary
		# Also return 201 (created)
		return item.json(), 201;


	# - - - - - - - - - - - - - - 
	# PUT
	def put(self, name):
		# Use a class method to get/verify given arguments
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)
		updated_item =  ItemModel(name, data['price'])

		if item is None:
			try:
				updated_item.insert()
			except:
				return {"message": "An error occurred inserting the item."}, 500
		else:
			try:
				updated_item.update()
			except:
				return {"message": "An error occurred inserting the item."}, 500

		return updated_item.json();

	# - - - - - - - - - - - - - - 
	# DELETE
	def delete(self, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "DELETE FROM items WHERE name=?"
		cursor.execute(query, (name,))

		connection.commit()
		connection.close()	
	
		return {'message': 'Item deleted'}, 200

# --------------------------------------------------------------------------------------------

class ItemList(Resource):
	def get(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items"
		result = cursor.execute(query)

		items = []
		for row in result:
			items.append({'name': row[0], 'price': row[1]})

		connection.close()		

		return {'items': items}

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
