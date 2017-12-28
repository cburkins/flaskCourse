	
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta


# Our own package
from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList


app = Flask(__name__)
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

	#app.run(port=5000)
	app.run(port=5000, debug=True)

