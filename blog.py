from flask import Flask, render_template, request, session, \
	flash, redirect, url_for, g
from functools import wraps
import sqlite3


# Config
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = """\x11`=\x0e\xff\\\x96\xf9G+S\x8ba;\xa8RXx\xb5\xde\xc95ly"""
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

# Tests wether the session is logged in
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

# Pages
"""
All html uses template.html to construct the page
"""
# Login
@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or \
			request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			return redirect(url_for('main'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))


@app.route('/main')
@login_required
def main():
	g.db = connect_db()
	cur = g.db.execute('select * from posts')
	posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
	g.db.close()
	return render_template('main.html', posts=posts)

@app.route('/add', methods=['POST'])
@login_required
def add():
	title = request.form['title']
	post = request.form['post']
	if not title or not post:
		flash("All fields are required. Please try again.")
		return redirect(url_for('main'))
	else:
		g.db = connect_db()
		g.db.execute('insert into posts(title, post) values (?, ?)',
			[request.form['title'], request.form['post']])
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted!')
		return redirect(url_for('main'))

if __name__ == '__main__':
	app.run(debug=True)


