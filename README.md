# Simple Todo List

Welcome! This is a simple todo list application with user accounts and basic features.

## Setup and usage:

### Initial Setup:

- Start a virtual environment: `virtualenv env && source env/bin/activate`
- Install requirements: `pip install -r requirements.txt`
- Set up the database:
	- `flask db init`
	- `flask db migrate`
	- `flask db upgrade`

### Usage:

- Start the application: `flask run`
- Go to `127.0.0.1:5000/` in a web browser
