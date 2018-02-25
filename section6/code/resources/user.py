import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel



class User(Resource):





	# Parser belongs to the class, not any particular item (instance)
	parser = reqparse.RequestParser()
	parser.add_argument('enabled',
		type=int, 
		required=True,
		help="This field cannot be left blank, silly."
	)


	# - - - - - - - - - - - - - - 
	# GET
	# @jwt_required() requires a valid JWT token to be present in the request
	def get(self, username):

		# this is a class method; however, we can still call it via self
		user = UserModel.find_by_username(username);		

		if user:
			# item is an ItemModel object (not a dictionary), so convert to json
			return user.json()
		# Item wasn't found, return a helpful message (in JSON) along with a 404 status code
		return {'message': 'Item not found'}, 404


	# - - - - - - - - - - - - - - 
	# PUT
	def put(self, username):
	
		# Use a class method to get/verify given arguments
		data = User.parser.parse_args()
	
		# try to retrieve a pre-existing item from the DB
		user = UserModel.find_by_username(username)

		if user is None:
			# Item was not found in DB, so create a new Object using the given price
			# Optionally, could use unpacking so would be ItemModel(name, **data)
			return {'message': 'username not found'}, 400
		else:
			# Item WAS found in DB, so modify it's price
			user.enabled = data['enabled']

		# Write the object back to the DB
		user.save_to_db()

		return user.json();
# --------------------------------------------------------------------------------------------




# Because this inherits from Resource, it can become an endpoint
# Check in app.py, this class will be used in "add_resource" method  
class UserList(Resource):
	def get(self):
		return {'allusers': list(map(lambda x: x.json(), UserModel.query.all()))}

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
