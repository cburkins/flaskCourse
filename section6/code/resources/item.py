
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
			item.save_to_db()
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
		# try to retrieve a pre-existing item from the DB
		item = ItemModel.find_by_name(name)

		if item is None:
			# Item was not found in DB, so create a new Object using the given price
			item = ItemModel(name, data['price'])
		else:
			# Item WAS found in DB, so modify it's price
			item.price = data['price']

		# Write the object back to the DB
		item.save_to_db()

		return item.json();

	# - - - - - - - - - - - - - - 
	# DELETE
	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message': 'Item deleted'}, 200

# --------------------------------------------------------------------------------------------

class ItemList(Resource):
	def get(self):
		# Both of these work
		return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
		#return {'items': [item.json() for item in ItemModel.query.all()]}

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
