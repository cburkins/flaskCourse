

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

### Other stuff

- within Cygwin
- pip3 install flask

### Running it

- Within Cygwin
- python3 app.py
- Should say:

```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Section 4

- Within Cygwin
- pip3 install virtualenv
- virtualenv venv --python=python3
- source venv/bin/activate

Testing and leaving the virtualenv

- python -V (should show you version 3)
- deactivate 
- python -V (will likely show you version 2)
- source venv/bin/activate
- python -V (will show you version 3 again)

Build out rest of virtualenv

NOTE: you no longer need pip3


- pip install Flask-RESTful  (uh-oh, pip cannot handled spaces in the path to the env)

Try this instead

-  python venv/bin/pip install Flask-RESTful

Ah, turns out unix scripts cannot have a space in the shebang path

To check out what's installed

- python venv/bin/pip freeze
