
import sqlite3

from db import db

# Create class User with a few properties, also extend (inhertit from) db.Model (which is SQLAlchmey)
class ItemModel(db.Model):
	# SQLAclhemy database table for this model
	__tablename__ = 'items'
	# SQLAlchemy database columns
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision=2))

	def __init__(self, name, price):
		self.name = name
		self.price = price

	def json(self):
		return {'name': self.name, 'price': self.price}

	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor();

		query = "SELECT * from items where name=?"
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		connection.close();
		if row:
			# return an object of type ItemModel object (itself), passing the needed attributes
			# calls the class's init() method
			# could also use unpacking, in other words, cls(*row)
			return cls(row[0], row[1])



	def insert(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "INSERT INTO items VALUES (?, ?)"
		cursor.execute(query, (self.name, self.price))

		connection.commit()
		connection.close()	


	def update(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "UPDATE items SET price=? WHERE name=?"
		cursor.execute(query, (self.price, self.name))

		connection.commit()
		connection.close()		

