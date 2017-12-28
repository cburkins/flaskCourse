

### Resources

- cygwin on Windows 10
- python 3 (installed via Cygwin installer)


### Installing Cygwin and Python3

- Re-run the cygwin install
- NOTE: if you haven't run Cygwin in a while, it upgrades lots/all packages
- Select mirror
- in the Package selector, select "Category" (much easier to read)
- Type "python3", and select the interpreter
- Type "pip3", and select the pip installer


### Accessing this code (for the class)

- https://github.com/schoolofcode-me/rest-api-sections/tree/master/section3


### Section 3 (using Cygwin, no virtualenv)

**Prep**

- Within Cygwin
- pip3 install flask


**Running it**

- (within Cygwin) python3 app.py
- Should say:

```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```


### Section 4 (Flask-RESTful and virtualenv)

**Installing virtualenv**
- Within Cygwin
- pip3 install virtualenv

**Creating virtualenv for Section 4**
- virtualenv venv --python=python3

**Testing and leaving the virtualenv**

- source venv/bin/activate
- python -V (should show you version 3)
- deactivate 
- python -V (will likely show you version 2)

**Installing libraries in the virtualenv**

- source venv/bin/activate
- python -V (will show you version 3 again)
- python venv/bin/pip install Flask-RESTful
- python venv/bin/pip install Flask-JWT


NOTE: you no longer need pip3
NOTE: turns out unix scripts cannot have a space in the shebang path, so "pip install Flask-RESTful" will fail 

### Section 5

**Creating virtualenv for Section 5**

- virtualenv venv --python=python3
- source venv/bin/activate
- python venv/bin/pip install Flask-RESTful Flask-JWT  (also installs Flask)


### Section 6

**Creating virtualenv for Section 5**
- virtualenv venv --python=python3
- source venv/bin/activate
- python venv/bin/pip install Flask-RESTful Flask-JWT Flask-SQLAlchemy (also installs Flask)


### Other commands



- python venv/bin/pip freeze
