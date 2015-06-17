from flask import Flask, render_template, request, session, \
	flash, redirect, url_for, g
import sqlite3

# Config
DATABASE = 'blog.db' # database
app = Flask(__name__) # Sends to class EG.Flask(blog.py)
app.config.from_object(__name__) # Flask module looks for upercase config
# In this case its parsing itself and setting the DATABASE s blog.db

# Database connection
def connect_db():
	"""
	Connects to the app config and retrieves DATABASE to connect to
	with sqlite3.
	"""
	return sqlite3.connect(app.config['DATABASE'])

# Pages
"""
All html uses template.html to construct the page
"""

@app.route('/')
def login():
	return render_template('login.html')

@app.route('/main')
def main():
	return render_template('main.html')



if __name__ == '__main__':
	app.run(debug=True)


