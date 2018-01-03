from db import db

# Create class User with a few properties, also extend (inhertit from) db.Model (which is SQLAlchmey)
class ItemModel(db.Model):
	# SQLAclhemy database table for this model
	__tablename__ = 'items'
	# SQLAlchemy database columns
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision=2))

	# SQLAlchemy call to create a relationship from ItemModel (items table) to StoreModel (stores table)
	# The field type (db.Integer) must match related column (in stores table) exactly
	# Items that are linked to a store prevents the store from being deleted
	store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
	store = db.relationship('StoreModel')

	def __init__(self, name, price, store_id):
		self.name = name
		self.price = price
		self.store_id = store_id

	def json(self):
		# return {'name': self.name, 'price': self.price}
		return {'name': self.name, 'price': self.price, 'store_id': self.store_id}

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
