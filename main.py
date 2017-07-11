from flask import Flask
from flask import render_template, request, redirect, url_for, flash

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Post

import requests

app = Flask(__name__, static_url_path='/static/*')

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
def hello_world():
	return render_template('front.html')

@app.route('/test')
def post_test():
	items = session.query(Post).order_by(desc(Post.created_date)).all()
	return render_template('test-post.html', items=items)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
	if request.method == 'POST':
		newPost = Post(user_id=1, title=request.form['title'], content=request.form['content'])
		session.add(newPost)
		session.commit()
		return redirect(url_for('post_test'))
	else:
		return render_template('newpost.html')
