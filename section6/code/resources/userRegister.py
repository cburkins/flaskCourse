import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

# Because this inherits from Resource, it can become an endpoint
# Check in app.py, this class will be used in "add_resource" method  
class UserRegister(Resource):

	# Using the Flask-RESTful request parsing library, create an instance of RequestParser 
	parser = reqparse.RequestParser()
	# Require the username parameter
	parser.add_argument('username',
		type=str, 
		required=True, 
		help="This field cannot be blank."
	)
	# Require the password parameter
	parser.add_argument('password',
		type=str, 
		required=True, 
		help="This field cannot be blank."
	)


	def post(self):

		# Get the request body
		data = UserRegister.parser.parse_args()

		# Verify that new requested new username doesn't already exist
		if UserModel.find_by_username(data['username']):
			return {"message": "A user with that username already exists"}, 400

		# Same, user = UserModel(data['username'], data['password'])
		# This format is called unpacking, it's important that the parser enforces how many properties are in dictionary
		#user = UserModel(**data)
		# Create a disabled user (admin needs to enable this user later)
		user = UserModel(data['username'], data['password'], 0)

		user.save_to_db()

		# return message to requester along with 201 (created)
		return {"message": "User created successfully."}, 201

# ------------------------------------------------------------------------------------------

class UserList(Resource):
	def get(self):
		return {'allusers': list(map(lambda x: x.json(), UserModel.query.all()))}

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
