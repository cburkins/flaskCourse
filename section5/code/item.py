
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


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

		# this is a class method; however, we can still call it via self
		item = self.find_by_name(name);		

		if item:
			return item
		# Item wasn't found, return a helpful message (in JSON) along with a 404 status code
		return {'message': 'Item not found'}, 404


	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor();

		query = "SELECT * from items where name=?"
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		connection.close();
		if row:
			return {'item': {'name': row[0], 'price': row[1]}}


	# POST
	def post(self, name):
		# error control first, make sure the item doesn't already exist
		# class method, so we can call via self.find_by_name() or Item.find_by_name()
		if self.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name) }, 400

		# Use a class method to get/verify given arguments
		data = Item.parser.parse_args()

		# Add the item
		item = {'name': name, 'price': data['price']}

		try:
			self.insert(item)
		except:
			return {"message": "An error occurred inserting the item."}, 500  # 500 = Internal Server Error

		# flask_restful automatically jsonifies our dictionary
		# Also return 201 (created)
		return item, 201;


	@classmethod
	def insert(cls, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "INSERT INTO items VALUES (?, ?)"
		cursor.execute(query, (item['name'], item['price']))

		connection.commit()
		connection.close()	

	# PUT
	def put(self, name):
		# Use a class method to get/verify given arguments
		data = Item.parser.parse_args()

		item = self.find_by_name(name)
		updated_item = {'name': name, 'price': data['price']}

		if item is None:
			try:
				self.insert(updated_item)
			except:
				return {"message": "An error occurred inserting the item."}, 500
		else:
			try:
				self.update(updated_item)
			except:
				return {"message": "An error occurred inserting the item."}, 500

		return updated_item;

	@classmethod
	def update(cls, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "UPDATE items SET price=? WHERE name=?"
		cursor.execute(query, (item['price'], item['name']))

		connection.commit()
		connection.close()		

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
