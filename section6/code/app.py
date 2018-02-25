	
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

# Our own packages
from security import authenticate, identity
# Import the flask_restful resource that we'll use to create flask endpoints
from resources.userRegister import UserRegister, UserList
from resources.user import User, UserList
from resources.item import Item, ItemList
from resources.store import Store, StoreList


# Running this application
# > python3 app.py
#
# You may need to start up your virtualenv with "source venv/bin/activate"

# Flask is a python microframework to build web application (acts as a webserver) 
# microframework means Flask is lean.  Doesn't make decisions for you (e.g. what database to use)

# Flask-RESTful is an extension for Flask that adds support for building REST APIs

# Flask-JWT adds based JWT features to the Flask application
# JWT is JSON Web Tokens, a secure way to exchange information between two parties
# Server provides JWT to client (e.g. client is logged in as user 'joe_smith')


# Create Flask web application
# If this file (app.py) was invoked as main program, __name__ = __main__  (we are main)
# if this file (app.py) was imported, then __name__ = the-module-name
app = Flask(__name__)

# Tell SQLAlchemy location of DB, which is root folder of our project
# Fun, you can use other DB types, such as mySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Tell SQLAlchemy to turn off the Flask SQL Alchemy modification tracker, but does not turn off the underlying (non-Flask) SQL Alchemy tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# secret_key is used to encrypt/decrypt all traffic to API
# If changed, this will invalidate all current sessions, but new sessions can be created
app.secret_key = 'jose3'

# From flask_restful, create API application
api = Api(app)

# Initialize the jwt object
# Set the endpoint to be /auth
app.config['JWT_AUTH_URL_RULE'] = '/auth'
# Set the token expiration time to 30 minutes
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# Create table before first request
# Decorator that registers a function to be run *before* the first user request to our app
@app.before_first_request
def create_tables():
	# SQL Alchemy function to create all the required database tables
	# Will only create tables/columns that it knows about.
	# In our case, we import resources, which in turn import models, which in turn have table/column definitions
	db.create_all()

# create the jwt object, registering our authentication and identity handlers (which we wrote)
# "app" is Flask application
# "authenticate" (from our own security class) is the authentication handler function
#    Receives two arguments, username and password, returns object representing an authenticated identity.
# "identity" (from our own security class) is the identity handler function
#    Receives JWT payload (from API call) and returns corresponding user object
jwt = JWT(app, authenticate, identity)

# Create endpoint
api.add_resource(Store, '/store/<string:name>')
# Create endpoint
api.add_resource(StoreList, '/stores')
# Create endpoint:   http://127.0.0.1/item/<name>  (GET/POST for single items)
api.add_resource(Item, '/item/<string:name>');
# Create endpoint:   http://127.0.0.1/items  (GET list all items)
api.add_resource(ItemList, '/items')
# Create endpoint:   http://127.0.0.1/register (POST to register a new user)
api.add_resource(UserRegister, '/register' )

api.add_resource(User, '/user/<string:username>');
api.add_resource(UserList, '/users');

# Check to see if we're the main program (not just imported)
if __name__ == '__main__':
	# this file was the file that was run.  
	# In other words, it WASN'T just imported, so we want to run our main

	# SQLAlchmey, putting it here prevents circular import
	from db import db
	db.init_app(app)

	#app.run(port=5000)
	app.run(port=5000, debug=True)

# ===================================================================================================
# ==================================== End ==========================================================
# ===================================================================================================
