from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json(), 200
		return {'message': 'Store not found'}, 404

	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message': "A Store with name '{}' already exists.".format(name)}, 400

		# Store doesn't exist yet, so we can create a new one
		store = StoreModel(name)
		print ("Created store");
		try: 
			store.save_to_db()
		except:
			return {'message': "Error occurred while saving store"}, 500

		return store.json(), 201


	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			store.delete_from_db()
		return {"message": 'Store deleted'}


class StoreList(Resource):
	def get(self):
		# List comprehension
		return {'stores': [store.json() for store in StoreModel.query.all()]}
