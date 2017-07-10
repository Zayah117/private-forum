from flask import Flask
from flask import render_template, request, redirect, url_for, flash

from sqlalchemy import create_engine
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
	items = session.query(Post).all()
	return render_template('test-post.html', items=items)
