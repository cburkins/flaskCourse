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
		# Remember, cls = ItemModel
		return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

	def save_to_db(self):
		# SQLAlchemy can write objects directly to the DB
		# If the id exists, does an update, otherwise, does an insert
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
