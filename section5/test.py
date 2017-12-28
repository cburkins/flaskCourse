# built into python
import sqlite3

# Create the database file
connection = sqlite3.connect('data.db')

# Give ourselves access to the database
cursor = connection.cursor()

# Create query to create schema of the table
create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table);

# tuple
user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user);

users = [
	(2, 'rolf', 'asdf'),
	(3, 'anne', 'xyz')
]
cursor.executemany(insert_query, users);

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
	print(row)

connection.commit();
connection.close();
