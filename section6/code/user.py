import sqlite3
from flask_restful import Resource, reqparse

# Create class User with a few properties
class User:
	def __init__(self, _id, username, password):
		# Using _id because id is special within Python
		self.id = _id;
		self.username = username
		self.password = password

	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE username=?"
		# Arguments to execute must always be a tuple
		result = cursor.execute(query, (username,))
		row = result.fetchone()
		if row: 
			# same as User(row[0], row[1], row[2]) 
			# @classmethod means we don't have to hardcode the name of the Class in here
			user = cls(row[0], row[1], row[2])
		else:
			user = None

		connection.close()
		return user


	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE id=?"
		# Arguments to execute must always be a tuple
		result = cursor.execute(query, (_id,))
		row = result.fetchone()
		if row: 
			# same as User(row[0], row[1], row[2]) 
			# @classmethod means we don't have to hardcode the name of the Class in here
			user = cls(row[0], row[1], row[2])
		else:
			user = None

		connection.close()
		return user


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
		if User.find_by_username(data['username']):
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