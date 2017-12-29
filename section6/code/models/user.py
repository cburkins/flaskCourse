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

	def __init__(self, username, password):
		# Using _id because id is special within Python
		# These two things need to exactly match the database columsn for them to be saved into the database
		self.username = username
		self.password = password

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def find_by_username(cls, username):
		# SQLAlchemy converts the DB row to a UserModel object
		return cls.query.filter_by(username=username).first()

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()


