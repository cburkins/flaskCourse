import sqlite3


# Create class User with a few properties
class UserModel:
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

