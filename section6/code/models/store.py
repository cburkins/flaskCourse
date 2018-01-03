from db import db

# Create class User with a few properties, also extend (inhertit from) db.Model (which is SQLAlchmey)
class StoreModel(db.Model):
	# SQLAclhemy database table for this model
	__tablename__ = 'stores'
	# SQLAlchemy database columns
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	# Use SQLAlchemy to create a Backreference.  Inform SQLAlchemy that there's a relationship.  
	# It will go look in ItemModel to find the relationship definition 
	items = db.relationship('ItemModel')

	def __init__(self, name):
		self.name = name

	def json(self):
		# self.items is populated by the DB Backreference defined above
		#return {'name': self.name, 'items': self.items}
		return {'name': self.name, 'items': [item.json() for item in self.items]}


	@classmethod
	def find_by_name(cls, name):
		# Remember, cls = StoreModel
		return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

	def save_to_db(self):
		# SQLAlchemy can write objects directly to the DB
		# If the id exists, does an update, otherwise, does an insert
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
