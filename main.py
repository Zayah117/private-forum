from flask import Flask
from flask import render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Post

app = Flask(__name__, static_url_path='/static/*')

@app.route('/')
def hello_world():
	return render_template('front.html')

@app.route('/test')
def post_test():
	return render_template('test-post.html', items=None)
