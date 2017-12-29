import sqlite3
from db import db

# Create class User with a few properties, also extend (inhertit from) db.Model (which is SQLAlchmey)
class UserModel(db.Model):
	# Tell SQLAlchemy the table name where these models will be stored
	__tablename__ = 'users'
	# Tell SQLAlchemy what columns will be in the table
	# primary_key tells SQLAlchemy that this column will contain unique values, and should be an index (self-incrementing?)
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	password = db.Column(db.String(80))

	def __init__(self, _id, username, password):
		# Using _id because id is special within Python
		# These three things need to exactly match the database columsn for them to be saved into the database
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

