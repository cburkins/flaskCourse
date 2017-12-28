import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

# Because this inherits from Resource, it can become an endpoint
class UserRegister(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str, 
		required=True, 
		help="This field cannot be blank."
	)
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

		# Open the database
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		# 1st argument (in the tuple) is NULL because that field (id) is auto-incrementing in the DB
		query = "INSERT INTO users VALUES (NULL, ?, ?)"
		cursor.execute(query, (data['username'], data['password']))

		connection.commit()
		connection.close()

		# return message to requester along with 201 (created)
		return {"message": "User created successfully."}, 201