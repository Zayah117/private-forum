from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask import session as session_info

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from database_setup import Base, User, Post

import requests
from functools import wraps

app = Flask(__name__, static_url_path='/static/*')

my_file = open("secret_key.txt", "r")
my_key = my_file.read()
my_file.close()

app.config['SECRET_KEY'] = my_key

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'username' not in session_info:
			return redirect(url_for('login', next=request.url))
		return f(*args, **kwargs)
	return decorated_function

@app.route('/')
def hello_world():
	return render_template('front.html')

@app.route('/test')
def post_test():
	items = session.query(Post).order_by(desc(Post.created_date)).all()
	users = session.query(User).all()
	return render_template('test-post.html', items=items, users=users)

@app.route('/newpost', methods=['GET', 'POST'])
@login_required
def new_post():
	if request.method == 'POST':
		new_post = Post(user_id=session_info['user_id'], title=request.form['title'], content=request.form['content'])
		session.add(new_post)
		session.commit()
		return redirect(url_for('post_test'))
	else:
		return render_template('newpost.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		new_user = User(name=request.form['username'], password_hash=request.form['password'])
		session.add(new_user)
		session.commit()
		return redirect(url_for('post_test'))
	else:
		return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		try:
			user = session.query(User).filter(User.name == request.form['username']).filter(User.password_hash == request.form['password']).one()
		except MultipleResultsFound:
			user = None
		except NoResultFound:
			user = None
		if user:
			session_info['username'] = user.name
			session_info['user_id'] = user.id
			return redirect(url_for('post_test'))
		else:
			return redirect(url_for('login'))
		# return str(session_info['username'])
	else:
		return render_template('login.html')

@app.route('/logout')
def logout():
	del session_info['username']
	del session_info['user_id']
	return "You have logged out."