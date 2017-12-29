	
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

# Our own package
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList


app = Flask(__name__)
# Tell SQLAlchemy location of DB, which is root folder of our project
# Fun, you can use other DB types, such as mySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Tell SQLAlchemy to turn off the Flask SQL Alchemy modification tracker, but does not turn off the underlying (non-Flask) SQL Alchemy tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

# Initialize the jwt object
# Set the endpoint to be /auth
app.config['JWT_AUTH_URL_RULE'] = '/auth'
# Set the token expiration time to 30 minutes
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
# create the jwt object
jwt = JWT(app, authenticate, identity)

# http://127.0.0.1/item/<name>  (GET/POST for single items)
api.add_resource(Item, '/item/<string:name>');
# http://127.0.0.1/items  (GET list all items)
api.add_resource(ItemList, '/items')
# http://127.0.0.1/register (POST to register a new user)
api.add_resource(UserRegister, '/register' )


# Check to see if we're the main program (not just imported)
if __name__ == '__main__':
	# this file was the file that was run.  
	# In other words, it WASN'T just imported, so we want to run our main

	# SQLAlchmey, putting it here prevents circular import
	from db import db
	db.init_app(app)

	#app.run(port=5000)
	app.run(port=5000, debug=True)

